import os
import base64
import json
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
    # Load credentials from file if available
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


def list_gmail_attachments(service, user_id='me', query=""):
    """List attachments in a user's Gmail based on a query."""
    try:
        # Search for emails based on the provided query
        results = service.users().messages().list(userId=user_id, q=query).execute()
        messages = results.get('messages', [])

        if not messages:
            logging.info("No messages found with the given query.")
            return []

        # List of messages with attachment details
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


# Run a quick test for listing and downloading attachments
if __name__ == "__main__":
    service = authenticate_gmail()
    user_id = 'me'

    # Modify the query to refine which emails are listed (e.g., filter by sender, subject, or label)
    query = "has:attachment"  # This query searches for emails that have attachments
    attachments = list_gmail_attachments(service, user_id, query)

    logging.info(f"Found {len(attachments)} attachments:")
    for attachment in attachments:
        logging.info(f"Message ID: {attachment['message_id']}, Filename: {attachment['filename']}")

        # Download each attachment
        save_path = f"downloads/{attachment['filename']}"
        downloaded_file = download_gmail_attachment(service, user_id, attachment['message_id'], attachment['attachment_id'], save_path)

        # Print the result of the download
        if downloaded_file:
            logging.info(f"Successfully downloaded: {downloaded_file}")
        else:
            logging.error(f"Failed to download: {attachment['filename']}")
