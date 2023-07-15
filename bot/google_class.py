from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


class GoogleSheet:
    service = None
    creds = None
    __SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    def __init__(self, sheet_id: str, cred_path: str, token_path: str = None):
        self.sheet_id = sheet_id
        self.token_path = token_path
        self.cred_path = cred_path

        if self.token_path != None and os.path.exists(self.token_path):
            self.creds = Credentials.from_authorized_user_file('token.json', self.__SCOPES)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'creds_app.json', self.__SCOPES)
                self.creds = flow.run_local_server(port=0)

            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())
                self.token_path = 'token.json'
        self.service = build('sheets', 'v4', credentials=self.creds)

    def add_value(self, range: int, value: list):
        data = [{
            'range': range,
            'values': value
        }]
        body = {
            'valueInputOption': 'USER_ENTERED',
            'data': data
        }
        res = self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.sheet_id, body=body).execute()