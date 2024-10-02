import os
import base64
import re
import uuid
import time  # For delay and retry mechanisms
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
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)


def extract_message_id(gmail_url):
    """Extract the message ID from a Gmail URL."""
    message_id_match = re.search(r'th=([a-zA-Z0-9]+)', gmail_url)
    if message_id_match:
        return message_id_match.group(1)
    else:
        logging.error(f"Invalid Gmail URL: {gmail_url}. Unable to extract message ID.")
        return None


def get_correct_attachment_id(service, user_id, message_id):
    """Use the Gmail API to get the correct attachment ID by inspecting the message payload."""
    try:
        message = service.users().messages().get(userId=user_id, id=message_id, format='full').execute()
        parts = message.get('payload', {}).get('parts', [])

        for part in parts:
            if 'filename' in part and part['filename'] and 'body' in part and 'attachmentId' in part['body']:
                logging.info(f"Found attachment: {part['filename']} with attachmentId: {part['body']['attachmentId']}")
                return part['body']['attachmentId']

        logging.error(f"Could not find a valid attachment ID in message {message_id}")
    except Exception as e:
        logging.error(f"An error occurred while retrieving the correct attachment ID: {e}")
    return None


def generate_uuid_filename(extension=".dat"):
    """Generate a simple UUID-based filename with the given extension."""
    return f"{uuid.uuid4().hex}{extension}"


def download_gmail_attachment(service, user_id, msg_id, attachment_id, save_path, retry_count=5):
    """Download the attachment from a Gmail message using the correct attachment ID."""
    try:
        # Get the attachment data using the Gmail API
        attachment = service.users().messages().attachments().get(
            userId=user_id, messageId=msg_id, id=attachment_id).execute()
        file_data = base64.urlsafe_b64decode(attachment['data'].encode('UTF-8'))

        # Ensure the directory exists
        save_directory = os.path.dirname(save_path)
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        # Write the file data to the specified path
        with open(save_path, 'wb') as f:
            f.write(file_data)
        logging.info(f'Attachment saved to {save_path}')

        # Verify file existence and size
        if not os.path.exists(save_path) or os.path.getsize(save_path) == 0:
            logging.warning(f"File {save_path} not found or empty after writing.")
            return None

        # Retry mechanism to ensure the file is fully accessible
        for attempt in range(retry_count):
            if os.path.exists(save_path):
                logging.info(f"File {save_path} exists and is ready for scanning.")
                break
            logging.warning(f"Retrying file access for {save_path} (Attempt {attempt + 1}/{retry_count})...")
            time.sleep(0.5)
        else:
            logging.error(f"Failed to access {save_path} after multiple attempts.")
            return None

        return os.path.abspath(save_path)  # Return absolute path for ClamAV compatibility

    except Exception as e:
        logging.error(f"An error occurred while downloading the attachment: {e}")
        return None


def list_gmail_attachments(service, user_id='me', query=""):
    """List attachments in a user's Gmail account based on a query."""
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


def download_specific_attachment(service, gmail_url):
    """Download a specific Gmail attachment using the Gmail URL provided."""
    msg_id = extract_message_id(gmail_url)
    if not msg_id:
        logging.error(f"Invalid Gmail URL: {gmail_url}. Unable to extract message ID.")
        return None

    correct_attachment_id = get_correct_attachment_id(service, 'me', msg_id)
    if not correct_attachment_id:
        logging.error(f"Failed to retrieve a valid attachment ID for message {msg_id}")
        return None

    # Generate a safe UUID-based filename to avoid issues
    filename = generate_uuid_filename()
    save_path = os.path.join("downloads", filename)

    return download_gmail_attachment(service, 'me', msg_id, correct_attachment_id, save_path)


if __name__ == "__main__":
    service = authenticate_gmail()

    # Replace with a real Gmail URL for testing
    specific_gmail_url = "YOUR_GMAIL_URL_HERE"
    downloaded_file = download_specific_attachment(service, specific_gmail_url)
    if downloaded_file:
        logging.info(f"Successfully downloaded the specific attachment: {downloaded_file}")
    else:
        logging.error(f"Failed to download the specific attachment from the given Gmail URL.")
