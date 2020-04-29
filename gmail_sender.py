from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path

class GMailSender:
    def __init__(self):
        print('User Created')
        self.scopes = ['https://www.googleapis.com/auth/gmail.send']
        creds = None
        if os.path.exists('token-send.pickle'):
            with open('token-send.pickle', 'rb') as token:
                creds = pickle.load(token)
        try:
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json', self.scopes)
                    creds = flow.run_local_server(port=0)
                    with open('token-send.pickle', 'wb') as token:
                        pickle.dump(creds, token)

            self.service = build('gmail', 'v1', credentials=creds)
        except Exception as error:
            print("Error occured while authenticating :-")
            print(error)
        print('GMail API auth completed')

    def send_mail(self, message):
        try:
            message = (self.service.users().messages().send(userId='me', body=message).execute())
            print('Message Id: %s' % message['id'])
            return message
        except Exception as error:
            print('An error occurred while sending email: %s' % error)
            return None