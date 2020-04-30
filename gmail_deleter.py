from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path

class GMailDeleter:
    def __init__(self):
        print('User Created')
        self.scopes = ['https://mail.google.com/']
        creds = None
        if os.path.exists('token-delete.pickle'):
            with open('token-delete.pickle', 'rb') as token:
                creds = pickle.load(token)
        try:
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json', self.scopes)
                    creds = flow.run_local_server(port=0)
                    with open('token-delete.pickle', 'wb') as token:
                        pickle.dump(creds, token)
            self.service = build('gmail', 'v1', credentials=creds)
        except Exception as error:
            print("Error occured while authenticating :-")
            print(error)
        print('GMail API auth completed')

    def delete_message(self, message_id):
        try:
            self.service.users().messages().delete(userId='me', id=message_id).execute()
            print('Message with id: %s deleted' % message_id)
        except Exception as error:
            print('An error occurred: %s' % error)
