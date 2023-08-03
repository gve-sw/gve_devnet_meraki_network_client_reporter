""" Copyright (c) 2023 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
           https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""
import os.path
import datetime
from datetime import date
import csv
import requests
import meraki
import config
import os.path 


def append_column(networks,csv_file,custom_end_time):
    if custom_end_time == None:
        custom_end_time = datetime.datetime.now()
    dashboard = meraki.DashboardAPI(api_key=config.meraki_api_key, print_console=False,output_log=False)
    # Read the CSV file
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)  # Convert the reader object to a list of rows

    # Append the new column header to the first row
    dt_string = custom_end_time.strftime("%d/%m/%Y")
    rows[0].append(dt_string)


    # Append the new data to each row
    for row in rows[1:]:
        network_id = row[1]
        unique_count, total_count = get_unique_clients(network_id,custom_end_time)
        row.append(total_count)

    # Write the updated data back to the CSV file
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

def get_unique_clients(network_id,end_time=None):
    url = f'https://api.meraki.com/api/v1/networks/{network_id}/wireless/clients/connectionStats'

    headers = {
        'X-Cisco-Meraki-API-Key': api_key,
        'Content-Type': 'application/json'
    }
    # Calculate the timestamps for the last 30 days
    if end_time is None:
        end_time = datetime.datetime.now()

    total_count = 0
    unique_clients = set()

    # Create a sliding window of 7 days within the last month
    window_end = end_time
    window_start = end_time - datetime.timedelta(days=7)
    while window_start >= end_time - datetime.timedelta(weeks=4):
        params = {
            't0': window_start.isoformat(),
            't1': window_end.isoformat()
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            for client_data in data:
                connection_stats = client_data.get('connectionStats', {})
                if connection_stats.get('success'):
                    total_count += 1
                    unique_clients.add(client_data['mac'])
        else:
            return None

        window_end = window_start
        window_start -= datetime.timedelta(days=7)

    return len(unique_clients), total_count

file_exists = os.path.exists('client_counts.csv')

# Replace YOUR_API_KEY and YOUR_NETWORK_ID with your Meraki API key and network ID, respectively.
api_key = config.meraki_api_key

# Specifying custom end_time
#custom_end_time = None
custom_end_time = datetime.datetime(2023, 8, 1)


# Define the Meraki API endpoints to query network information.
url_base = 'https://api.meraki.com/api/v1'
url_networks = url_base + '/organizations/{}/networks'.format(config.org_id)

# Define the headers to use for the API requests.
headers = {
    'X-Cisco-Meraki-API-Key': api_key,
    'Content-Type': 'application/json'
}

# Get a list of networks associated with the specified organization.
response = requests.get(url_networks, headers=headers)
networks = response.json()

if file_exists == False:
    if custom_end_time == None:
        custom_end_time = datetime.datetime.now()

    with open('client_counts.csv', 'w', newline='') as csvfile:
        fieldnames = ['Network Name', 'Network ID',custom_end_time.strftime("%d/%m/%Y")]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for network in networks:
            unique_count, total_count = get_unique_clients(network['id'],custom_end_time)
            if unique_count is not None:
                writer.writerow({'Network Name': network['name'],'Network ID': network['id'],custom_end_time.strftime("%d/%m/%Y"): total_count})
            else:
                print(f"Failed to retrieve data for network '{network['name']}'")
    print("Data saved to client_counts.csv")
else:
    append_column(networks,config.file_path,custom_end_time)
    print('Column appended successfully!')
    