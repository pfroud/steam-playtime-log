import os
import httplib2
import oauth2client
from apiclient import discovery
from oauth2client import client
from oauth2client import tools

# most of this file from https://developers.google.com/sheets/quickstart/python

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-steam-playtime.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Steam playtime logger'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-steam-playtime.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def save_to_sheets(game_obj):
    """
    Saves playtime for one game to Google Sheets.
    :param game_obj: dict (from json object) with game and playtime information
    :type game_obj: dict
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discovery_url = 'https://sheets.googleapis.com/$discovery/rest?version=v4'
    service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discovery_url)

    from datetime import datetime
    now = datetime.now()

    # Behold the amount of JSON it takes to add three numbers to a spreadsheet. Six nested objects. Read all about it:
    # https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/batchUpdate
    # https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/request#request
    # https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/request#appendcellsrequest
    # https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets#RowData
    # https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets#CellData
    # https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets#ExtendedValue
    # Yes, every oen of those structures is required. I couldn't make this up.
    # I have commented each object with its type to make it easier to follow along.
    json = {
        # batchUpdate
        "requests": {
            # Request
            "appendCells": {
                # AppendCellsRequest
                "sheetId": 0,
                "rows": [{
                    # RowData
                    "values": [{
                        # CellData
                        "userEnteredValue": {
                            # ExtendedValue
                            "stringValue": str(now.date())
                        }
                    }, {
                        # CellData
                        "userEnteredValue": {
                            # ExtendedValue
                            "stringValue": str(now.time())
                        }
                    }, {
                        # CellData
                        "userEnteredValue": {
                            # ExtendedValue
                            "numberValue": game_obj['playtime_forever']
                        }
                    },
                    ]
                }],
                "fields": "*"
            }
        }
    }

    spreadsheet_id = "1xSOC2HNoV_e6uCTnorLh-9j4iHQS7UDnkwNFD2aMuvw"
    # https://developers.google.com/sheets/reference/rest/v4/spreadsheets/request#appendcellsrequest
    service.spreadsheets().batchUpdate(body=json, spreadsheetId=spreadsheet_id).execute()
