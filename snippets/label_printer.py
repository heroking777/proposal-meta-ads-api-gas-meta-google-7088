import gspread
from oauth2client.service_account import ServiceAccountCredentials
from meta_ads_api import MetaAdsAPI

def print_barcode_to_google_sheet():
    # Set up Google Sheets API credentials
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    # Open the Google Sheet by its name
    sheet = client.open('Meta Ads Data').sheet1

    # Initialize Meta Ads API with your credentials
    meta_ads_api = MetaAdsAPI(api_key='your_meta_ads_api_key')

    # Fetch data from Meta Ads API
    ads_data = meta_ads_api.get_all_ads()

    # Clear existing data in the sheet
    sheet.clear()

    # Write headers to the sheet
    headers = ['Ad ID', 'Name', 'Status', 'Budget']
    sheet.insert_row(headers, 1)

    # Insert data into the sheet
    for ad in ads_data:
        row = [ad['id'], ad['name'], ad['status'], ad['budget']]
        sheet.insert_row(row, len(sheet.get_all_values()) + 2)

    print("Data fetched and written to Google Sheet successfully.")

# Call the function to execute the automation
print_barcode_to_google_sheet()
```

Please note that you need to replace `'your_meta_ads_api_key'` with your actual Meta Ads API key and `'client_secret.json'` with the path to your Google Sheets API credentials file. Also, ensure that the `meta_ads_api` library is installed in your Python environment.