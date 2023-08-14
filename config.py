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

import datetime

# Specifying custom end_time will default to current day if None

#custom_end_time = None
custom_end_time = datetime.datetime(2023, 8, 1) # August 1 2023

meraki_api_key = ''
org_id = ''


# GOOGLE DRIVE INTEGRATION toggle True or False
G_DRIVE = True

# Follow README steps to create credentials json file
CLIENT_SECRET_FILE = 'client_secret.json'   # The path to the client secret json file you downloaded.
file_path = 'client_counts.csv'  # Replace with the path to the new CSV file you want to upload
google_folder_id = ''