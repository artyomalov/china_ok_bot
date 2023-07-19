from __future__ import print_function
from googleapiclient.discovery import build
from google.oauth2 import service_account
from config_reader import config
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'service.json'

creds = None
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=credentials)


sheet = service.spreadsheets()
cursor = sheet.values()


def add_data_to_gsheets(range: str, send_data: list[list]):
    '''
    add user data to related google sheets table.
    range: google sheets range(for example: <gsheets_table_name>!A1:E1)
    send_data: list that consistsdata ennumerated as lements of another list
    where first element will placed at first cell of range, second alement
    will palced at the second cell of range e. t. c.

    '''
    cursor.append(
        spreadsheetId=config.sample_spreadsheet_id.get_secret_value(),
        range=range,
        valueInputOption='USER_ENTERED',
        insertDataOption='INSERT_ROWS',
        body={'values': send_data}
    ).execute()
