# gve_devnet_meraki_network_client_reporter
prototype script that gathers a client report for every network within a Meraki organization. optionally can upload report to google drive

## Contacts
* Jorge Banegas

## Solution Components
* Meraki

## Prerequisites
#### Meraki API Keys
In order to use the Meraki API, you need to enable the API for your organization first. After enabling API access, you can generate an API key. Follow these instructions to enable API access and generate an API key:
1. Login to the Meraki dashboard
2. In the left-hand menu, navigate to `Organization > Settings > Dashboard API access`
3. Click on `Enable access to the Cisco Meraki Dashboard API`
4. Go to `My Profile > API access`
5. Under API access, click on `Generate API key`
6. Save the API key in a safe place. The API key will only be shown once for security purposes, so it is very important to take note of the key then. In case you lose the key, then you have to revoke the key and a generate a new key. Moreover, there is a limit of only two API keys per profile.

> For more information on how to generate an API key, please click [here](https://developer.cisco.com/meraki/api-v1/#!authorization/authorization). 

> Note: You can add your account as Full Organization Admin to your organizations by following the instructions [here](https://documentation.meraki.com/General_Administration/Managing_Dashboard_Access/Managing_Dashboard_Administrators_and_Permissions).


## Installation/Configuration
1. Clone this repository with `git clone [repository name]`
2. Edit neccesary configuration details inside config.py
```python
meraki_api_key = ''
org_id = ''
```
3. Set up a Python virtual environment. Make sure Python 3 is installed in your environment, and if not, you may download Python [here](https://www.python.org/downloads/). Once Python 3 is installed in your environment, you can activate the virtual environment with the instructions found [here](https://docs.python.org/3/tutorial/venv.html).
4. Install the requirements with `pip3 install -r requirements.txt`

5. If you want to specify the date to then query the clients from the last 4 weeks, you can specify in line 94, leave it as None and it will query clients from today to the last 4 weeks
```python
#custom_end_time = None
custom_end_time = datetime.datetime(2023, 8, 1)
```

## Usage
To run the program, use the command:
```
python main.py
```

# Screenshots

![/IMAGES/local_report.png](/IMAGES/local_report.png)

## Enable Google Drive Integration

change the G_DRIVE variable as true and login into your google drive and select the folder from your GDRIVE and copy the id from the folder URL like the one below. Enter this id to the google_folder_id variable

![/IMAGES/local_report.png](/IMAGES/folder_url.png)

```
# GOOGLE DRIVE INTEGRATION toggle True or False
G_DRIVE = True

# Follow README steps to create credentials json file
CLIENT_SECRET_FILE = 'client_secret.json'   # The path to the client secret json file you downloaded.
file_path = 'client_counts.csv'  # Replace with the path to the new CSV file you want to upload
google_folder_id = '1zWa7fXQTMnjUD1r_YNefU2aUzXvir904'
```

Follow the next steps to generate a secret.json 
## Generating `client_secret.json` for Google API Authentication

### Overview

This guide helps you create a `client_secret.json` file for OAuth authentication with Google APIs.

### Steps

1. **Create a Project in Google Cloud Console**
   - Go to [Google Cloud Console](https://console.cloud.google.com/).
   - Click "New Project", name it, and click "Create".

2. **Enable the API**
   - In "APIs & Services" > "Library", enable your API (e.g., Google Drive API).

3. **Set Up OAuth Consent Screen**
   - In "APIs & Services" > "OAuth consent screen", choose "External".
   - Provide a name, email, scopes (e.g., `https://www.googleapis.com/auth/drive.file`), support email, and privacy policy URL.

4. **Create Credentials**
   - In "APIs & Services" > "Credentials", click "Create Credentials" > "OAuth client ID".
   - Choose "Desktop app" or "Web application".
   - Name your OAuth client.
   - For "Authorized redirect URIs", use your callback URL or leave blank.
   - Click "Create" to get OAuth client ID and secret.

5. **Download `client_secret.json`**
   - After creating OAuth client, download `client_secret.json`.

6. **Using `client_secret.json` in Code**
   - Put `client_secret.json` in your script's directory and rename the file to client_secret.json
   - Authenticate using it in your Python script.

### Security
- Keep `client_secret.json` secure.
- Follow best practices for secure coding.

![/IMAGES/0image.png](/IMAGES/g_drive_report.png)


![/IMAGES/0image.png](/IMAGES/0image.png)

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.