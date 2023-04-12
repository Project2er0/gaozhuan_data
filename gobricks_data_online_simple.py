import csv
import pandas as pd
import requests
import concurrent.futures
import ssl

# Read the ids from the id_List.csv file with utf-8 encoding
url = 'https://raw.githubusercontent.com/Project0ne/gaozhuan_data/main/id_List.csv?token=GHSAT0AAAAAAB7RS2QEX7ZK5HXR6PU2AJJYZBWWU6A'
df = pd.read_csv(url, header=None)
ids = df[0].tolist()

# Define the fieldnames for the CSV file
fieldnames = ["id", "caption","price", "caption_en", "color_id",  "inventory" ]

def fetch_data(id):
    # URL to fetch data from
    url = f'https://gobricks.cn/frontend/v1/item/filter?product_id={id}&type=2&limit=96&offset=0'

    # Send a GET request to the URL and store the response
    response = requests.get(url, verify=False)

    # Extract only the fields that we want to write to the CSV file
    data = response.json()['rows']
    filtered_data = [{k: v for k, v in d.items() if k in fieldnames} for d in data]
    return filtered_data

with concurrent.futures.ThreadPoolExecutor() as executor:
    # Open a CSV file in append mode with utf-8 encoding and write the data to it
    with open("data.csv", "a", newline="", encoding="utf-8_sig") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # Only write the header if the file is empty
        if csvfile.tell() == 0:
            writer.writeheader()
        # Submit the requests to the executor and write the data to the CSV file
        for data in executor.map(fetch_data, ids):
            for d in data:
                writer.writerow(d)
