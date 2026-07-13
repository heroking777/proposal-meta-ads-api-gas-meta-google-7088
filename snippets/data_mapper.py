import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Define the Meta Ads API endpoint and your credentials
META_ADS_API_ENDPOINT = 'https://graph.facebook.com/v15.0/act_{ad_account_id}/insights'
CREDENTIALS_FILE_PATH = 'path/to/your/service-account-file.json'

def fetch_meta_ads_data(ad_account_id, access_token):
    params = {
        'access_token': access_token,
        'level': 'ad',
        'fields': 'spend,campaign_name,adset_name,ad_name'
    }
    response = requests.get(META_ADS_API_ENDPOINT.format(ad_account_id=ad_account_id), params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data: {response.text}")

def authenticate_google_sheets():
    credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_FILE_PATH, scopes=['https://www.googleapis.com/auth/spreadsheets'])
    return build('sheets', 'v4', credentials=credentials)

def write_data_to_google_sheet(spreadsheet_id, range_name, values):
    service = authenticate_google_sheets()
    body = {
        'values': values
    }
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption='RAW',
        body=body).execute()
    return result

def validate_and_map_data(meta_ads_data):
    mapped_data = []
    for data in meta_ads_data['data']:
        mapped_row = [
            data.get('spend', ''),
            data.get('campaign_name', ''),
            data.get('adset_name', ''),
            data.get('ad_name', '')
        ]
        mapped_data.append(mapped_row)
    return mapped_data

def main():
    ad_account_id = 'your_ad_account_id'
    access_token = 'your_access_token'
    spreadsheet_id = 'your_spreadsheet_id'
    range_name = 'Sheet1!A1:D'

    try:
        meta_ads_data = fetch_meta_ads_data(ad_account_id, access_token)
        mapped_data = validate_and_map_data(meta_ads_data)
        write_data_to_google_sheet(spreadsheet_id, range_name, mapped_data)
        print("Data successfully written to Google Sheets.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
```

This Python script includes functions to fetch data from the Meta Ads API, authenticate with Google Sheets, and write the fetched data to a specified range in a Google Sheet. The `validate_and_map_data` function maps the fetched data into a format suitable for writing to Google Sheets. Make sure to replace placeholders like `your_ad_account_id`, `your_access_token`, and `your_spreadsheet_id` with actual values.