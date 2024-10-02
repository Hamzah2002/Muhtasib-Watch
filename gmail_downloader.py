import os
import base64
import json
import re
import uuid  # Add to generate unique filenames for downloads
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Define the scopes for Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def authenticate_gmail():
    """Authenticate and return a Gmail API service instance."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        # If credentials are expired or not available, start OAuth flow
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)


def extract_gmail_ids(gmail_url):
    """
    Extract the message ID and attachment ID from a Gmail URL.
    Returns a tuple: (message_id, attachment_id).
    """
    message_id_match = re.search(r'th=([a-zA-Z0-9]+)', gmail_url)
    attachment_id_match = re.search(r'attid=([0-9\.]+)', gmail_url)

    if message_id_match and attachment_id_match:
        return message_id_match.group(1), attachment_id_match.group(1)
    else:
        logging.error(f"Invalid Gmail URL: {gmail_url}. Unable to extract message ID or attachment ID.")
        return None, None


def list_gmail_attachments(service, user_id='me', query=""):
    """List attachments in a user's Gmail based on a query."""
    try:
        results = service.users().messages().list(userId=user_id, q=query).execute()
        messages = results.get('messages', [])

        if not messages:
            logging.info("No messages found with the given query.")
            return []

        attachments = []
        for message in messages:
            msg = service.users().messages().get(userId=user_id, id=message['id']).execute()
            parts = msg.get('payload', {}).get('parts', [])
            for part in parts:
                if part['filename'] and 'attachmentId' in part['body']:
                    attachment_info = {
                        'message_id': message['id'],
                        'attachment_id': part['body']['attachmentId'],
                        'filename': part['filename']
                    }
                    logging.info(f"Found attachment: {part['filename']} in message ID: {message['id']}")
                    attachments.append(attachment_info)

        return attachments

    except Exception as e:
        logging.error(f"An error occurred while listing attachments: {e}")
        return []


def download_gmail_attachment(service, user_id, msg_id, attachment_id, save_path):
    """Download the attachment from a Gmail message."""
    try:
        attachment = service.users().messages().attachments().get(
            userId=user_id, messageId=msg_id, id=attachment_id).execute()
        file_data = base64.urlsafe_b64decode(attachment['data'].encode('UTF-8'))

        # Create the downloads directory if it does not exist
        if not os.path.exists(os.path.dirname(save_path)):
            os.makedirs(os.path.dirname(save_path))

        with open(save_path, 'wb') as f:
            f.write(file_data)
        logging.info(f'Attachment saved to {save_path}')
        return save_path

    except Exception as e:
        logging.error(f"An error occurred while downloading the attachment: {e}")
        return None


def download_specific_attachment(service, gmail_url):
    """
    Download a specific Gmail attachment using the Gmail URL provided.
    """
    # Extract message ID and attachment ID from the Gmail URL
    msg_id, attachment_id = extract_gmail_ids(gmail_url)

    if not msg_id or not attachment_id:
        logging.error(f"Invalid Gmail URL: {gmail_url}. Unable to extract message ID or attachment ID.")
        return None

    # Use a unique filename for the specific attachment
    save_path = f"downloads/{uuid.uuid4().hex}_attachment.dat"
    logging.info(f"Downloading specific attachment from URL: {gmail_url}")
    return download_gmail_attachment(service, 'me', msg_id, attachment_id, save_path)


def download_multiple_attachments(service, query="has:attachment"):
    """
    List and download multiple attachments based on a Gmail query.
    """
    attachments = list_gmail_attachments(service, user_id='me', query=query)
    if not attachments:
        logging.info("No attachments found based on the query.")
        return []

    local_files = []
    for attachment in attachments:
        unique_filename = f"{uuid.uuid4().hex}_{attachment['filename']}"
        save_path = f"downloads/{unique_filename}"
        downloaded_file = download_gmail_attachment(service, 'me', attachment['message_id'],
                                                    attachment['attachment_id'], save_path)
        if downloaded_file:
            logging.info(f"Successfully downloaded: {downloaded_file}")
            local_files.append(downloaded_file)
        else:
            logging.error(f"Failed to download: {attachment['filename']}")

    return local_files


if __name__ == "__main__":
    service = authenticate_gmail()
    user_id = 'me'

    # Scenario 1: Handle Gmail-specific URL for a single attachment download
    specific_gmail_url = "https://mail.google.com/mail/u/0?ui=2&ik=a35699ab63&attid=0.1&permmsgid=msg-f:1802388023769561211&th=19035e5bb033f87b&view=fimg&fur=ip&sz=s0-l75-ft&attbid=ANGjdJ8y_aPPRUrECZpC0DXunWC8zlSASm-Sp5d5N6mNen3pA10Dz8zs_w767IX2uY0F8grNJDR0QMCalppB4t1aqsMVd1NlpJGcClDezOhk8xCJa64XqWiEcCmbUec&disp=emb"

    downloaded_file = download_specific_attachment(service, specific_gmail_url)
    if downloaded_file:
        logging.info(f"Successfully downloaded the specific attachment: {downloaded_file}")
    else:
        logging.error(f"Failed to download the specific attachment from the given Gmail URL.")

    # Scenario 2: List and download multiple attachments based on a search query
    local_files = download_multiple_attachments(service, query="has:attachment")
    if local_files:
        logging.info(f"Successfully downloaded multiple attachments: {local_files}")
    else:
        logging.error("Failed to download multiple attachments.")
