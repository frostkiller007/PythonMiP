from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path

class GMailModifier:
    def __init__(self):
        print('User Created')
        self.scopes = ['https://www.googleapis.com/auth/gmail.modify']
        creds = None
        if os.path.exists('token-trash.pickle'):
            with open('token-trash.pickle', 'rb') as token:
                creds = pickle.load(token)
        try:
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json', self.scopes)
                    creds = flow.run_local_server(port=0)
                    with open('token-trash.pickle', 'wb') as token:
                        pickle.dump(creds, token)
            self.service = build('gmail', 'v1', credentials=creds)
        except Exception as error:
            print("Error occured while authenticating :-")
            print(error)
        print('GMail API auth completed')

    def trash_message(self, message_id):
        try:
            message = (self.service.users().messages().trash(userId='me', id=message_id).execute())
            print('Message Id: %s sent to Trash.' % message['id'])
            return message
        except Exception as error:
            print('An error occurred while sending email: %s' % error)
            return None

    def add_labels(self, ids, labelids):
        try:
            obj = {
                'ids': ids,
                'addLabelIds': labelids
            }
            self.service.users().messages().batchModify(userId='me', body=obj).execute()
            print('Messages modified.')
        except Exception as error:
            print('Error occurred during modifying: %s' % error)