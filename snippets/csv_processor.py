import requests
import csv
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Meta Ads API credentials
meta_access_token = 'YOUR_META_ACCESS_TOKEN'
meta_ad_account_id = 'YOUR_META_AD_ACCOUNT_ID'

# Google Sheets API credentials
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'path/to/your/service-account-file.json'
SPREADSHEET_ID = 'YOUR_SPREADSHEET_ID'
RANGE_NAME = 'Sheet1!A1:D'  # Adjust the range as needed

# Function to fetch data from Meta Ads API
def fetch_meta_ads_data():
    url = f'https://graph.facebook.com/v15.0/{meta_ad_account_id}/insights?level=ad&metric=spend,impressions,campaign_name'
    headers = {
        'Authorization': f'Bearer {meta_access_token}'
    }
    response = requests.get(url, headers=headers)
    return response.json()

# Function to write data to Google Sheets
def write_to_google_sheets(data):
    creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = build('sheets', 'v4', credentials=creds)

    values = []
    for item in data['data']:
        values.append([
            item.get('campaign_name', ''),
            item.get('spend', 0),
            item.get('impressions', 0)
        ])

    body = {
        'values': values
    }

    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
        valueInputOption='RAW', body=body).execute()
    
    print(f'{result.get("updatedCells")} cells updated.')

# Main function to orchestrate the process
def main():
    data = fetch_meta_ads_data()
    write_to_google_sheets(data)

if __name__ == '__main__':
    main()
```

Make sure to replace `'YOUR_META_ACCESS_TOKEN'`, `'YOUR_META_AD_ACCOUNT_ID'`, `'path/to/your/service-account-file.json'`, and `'YOUR_SPREADSHEET_ID'` with your actual values. This script fetches ad spend, impressions, and campaign names from Meta Ads API and writes them to a specified range in Google Sheets. Adjust the `RANGE_NAME` as needed for your specific use case.