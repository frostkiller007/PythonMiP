from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
import mimetypes
import os
import base64
import re

def create_message(sender, to, subject, message_text):
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def create_message_with_attachment(sender, to, subject, message_text, filepath):
        size = os.path.getsize(filepath)
        if(size > 35000000):
            raise Exception("Filesize exceeded")
        message = MIMEMultipart()
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject

        msg = MIMEText(message_text)
        message.attach(msg)

        content_type, encoding = mimetypes.guess_type(filepath)

        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        main_type, sub_type = content_type.split('/', 1)
        if main_type == 'text':
            with open(filepath, 'r') as f:
                text = f.read()
            msg = MIMEText(text, _subtype=sub_type)
        elif main_type == 'image':
            with open(filepath, 'rb') as f:
                image = f.read()
            msg = MIMEImage(image, _subtype=sub_type)
        elif main_type == 'audio':
            with open(filepath, 'rb') as f:
                audio = f.read()
            msg = MIMEAudio(audio, _subtype=sub_type)
        else:
            with open(filepath, 'rb') as f:
                base = f.read()
            msg = MIMEBase(main_type, sub_type)
            msg.set_payload(base)
        filename = os.path.basename(filepath)
        msg.add_header('Content-Disposition', 'attachment', filename=filename)
        message.attach(msg)

        return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}


def get_email():
    verified = False
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    while (not verified):
        print("Enter valid email-id :- ")
        receiver = input().rstrip().lstrip()
        verified = re.match(email_regex, receiver)
    return receiver

def get_input():
    print("SENDER")
    sender = get_email()
    print("RECEIVER")
    receiver = get_email()
    print('Enter subject :-')
    subject = input()
    print('Enter message body :-')
    body = input()
    return sender, receiver, subject, body
