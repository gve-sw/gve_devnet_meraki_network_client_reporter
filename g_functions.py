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

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import os
import config

# Replace with your own values  # Path to your client secret JSON file
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def authenticate():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(config.CLIENT_SECRET_FILECLIENT_SECRET_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def delete_and_upload_file(file_path, folder_id):
    creds = authenticate()
    drive_service = build(API_NAME, API_VERSION, credentials=creds)

    file_name = os.path.basename(file_path)
    
    # Search for the file to delete
    results = drive_service.files().list(
        q=f"name='{file_name}' and '{folder_id}' in parents and mimeType='text/csv'",
        spaces='drive',
        fields='files(id, name)').execute()

    if results['files']:
        file_id = results['files'][0]['id']
        
        # Delete the existing file
        drive_service.files().delete(fileId=file_id).execute()
        
        print(f"File {file_name} deleted from Google Drive.")
    else:
        print(f"File {file_name} not found on Google Drive.")

    # Upload the new CSV file
    media = MediaFileUpload(file_path, mimetype='text/csv')
    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }
    uploaded_file = drive_service.files().create(body=file_metadata, media_body=media).execute()
    
    print(f"File {file_name} uploaded with new data.")