import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1a1Qq-6sAMVj5qO9nbecTcxtG_rldNzP8Pe3bvUuhpRg'
JSON_CREDS_PATH = 'credentials.json'

def get_sheets_service():
    credentials = service_account.Credentials.from_service_account_file(
        JSON_CREDS_PATH, scopes=SCOPES
    )
    service = build('sheets', 'v4', credentials=credentials)
    return service.spreadsheets()

def append_data_to_sheet(receipt):
    sheets = get_sheets_service()

    # Flatten line_items into a list of lists
    values = [[
        receipt.store_name,
        receipt.store_addr,
        receipt.telephone,
        receipt.date,
        receipt.time,
        receipt.,
        item.item_name,
        item.item_value,
        item.item_quantity
    ] for item in receipt.line_items]

    body = {'values': values}
    result = sheets.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range='Sheet1',  # Update with your sheet name or range
        valueInputOption='USER_ENTERED',
        body=body
    ).execute()

    print(f"{result['updates']['updatedCells']} cells updated.")
