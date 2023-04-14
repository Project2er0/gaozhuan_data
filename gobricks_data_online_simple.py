import urllib3
urllib3.disable_warnings()

import csv
import pandas as pd
import requests
import concurrent.futures
import ssl
from tqdm import tqdm
import time

# Read the ids from the id_List.csv file with utf-8 encoding
url = 'https://gitee.com/Project0ne/cdn/raw/master/src/id_List.csv'
df = pd.read_csv(url, header=None)
ids = df[0].tolist()

# Define the fieldnames for the CSV file
fieldnames = ["id", "caption","price", "caption_en", "color_id",  "inventory" ]

# Generate a filename based on the current time
filename = "gobrick_data_" + time.strftime("%Y-%m-%d_%H-%M-%S") + ".csv"

def fetch_data(id):
    # URL to fetch data from
    url = f'https://gobricks.cn/frontend/v1/item/filter?product_id={id}&type=2&limit=96&offset=0'

    try:
        # Send a GET request to the URL and store the response
        response = requests.get(url, verify=False)
    except requests.exceptions.ProxyError as e:
        print("ProxyError occurred:", e)
        return []

    # Extract only the fields that we want to write to the CSV file
    data = response.json()['rows']
    filtered_data = [{k: v for k, v in d.items() if k in fieldnames} for d in data]
    
    # Update the progress bar
    pbar.update(1)
    
    return filtered_data

with concurrent.futures.ThreadPoolExecutor() as executor:
    # Open a CSV file in append mode with utf-8 encoding and write the data to it
    with open(filename, "a", newline="", encoding="utf-8_sig") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # Only write the header if the file is empty
        if csvfile.tell() == 0:
            writer.writeheader()
        
        # Initialize the progress bar
        pbar = tqdm(total=len(ids))
        
        # Submit the requests to the executor and write the data to the CSV file
        for data in executor.map(fetch_data, ids):
            for d in data:
                writer.writerow(d)
        
        # Close the progress bar
        pbar.close()
