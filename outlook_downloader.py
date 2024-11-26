import os
import logging
import base64
import uuid
import requests
from urllib.parse import quote
from msal import PublicClientApplication, SerializableTokenCache
import re

# Configure logging
logging.basicConfig(level=logging.INFO)

# Microsoft Graph API endpoint and scopes
GRAPH_API_ENDPOINT = 'https://graph.microsoft.com/v1.0'
SCOPES = ['Mail.Read', 'Mail.ReadWrite']

# App registration details
CLIENT_ID = '1b7410b1-1190-413a-836d-4cf16ad24f3d'
TENANT_ID = 'e66e77b4-5724-44d7-8721-06df160450ce'
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"

# Token cache file path
TOKEN_CACHE_FILE = 'token_cache.json'


def load_token_cache():
    """Load the token cache from the file, or create a new one if not available."""
    cache = SerializableTokenCache()

    if os.path.exists(TOKEN_CACHE_FILE):
        # Load the cache from the file
        with open(TOKEN_CACHE_FILE, 'r') as f:
            cache.deserialize(f.read())

    return cache


def save_token_cache(cache):
    """Save the token cache to a file if there are any changes."""
    if cache.has_state_changed:
        with open(TOKEN_CACHE_FILE, 'w') as f:
            f.write(cache.serialize())


def authenticate_outlook(message_callback=None):
    """Authenticate user via OAuth2 and return access token."""
    cache = load_token_cache()

    try:
        app = PublicClientApplication(CLIENT_ID, authority=AUTHORITY, token_cache=cache)

        # Try to get token from cache
        accounts = app.get_accounts()
        if accounts:
            token_response = app.acquire_token_silent(SCOPES, account=accounts[0])
            if token_response:
                save_token_cache(cache)
                return token_response['access_token']

        # No token, initiate login
        flow = app.initiate_device_flow(scopes=SCOPES)
        if 'user_code' not in flow:
            raise ValueError("Failed to create device flow.")

        # Send the user code message to the GUI via callback, or log it if no callback is provided
        if message_callback:
            message_callback(flow['message'])  # Send to GUI
        else:
            logging.info(flow['message'])  # Default to terminal log

        # Wait for user to authenticate
        token_response = app.acquire_token_by_device_flow(flow)
        if 'access_token' in token_response:
            save_token_cache(cache)
            return token_response['access_token']
        else:
            logging.error(f"Authentication failed: {token_response.get('error_description')}")
            return None
    except Exception as e:
        logging.error(f"Error authenticating with Outlook: {str(e)}")
        return None


def sanitize_query(query):
    """Remove problematic characters from the query."""
    return re.sub(r"[^\w\s]", "", query)  # Remove special characters except spaces


def list_outlook_emails(token, query=None):
    """List the user's Outlook emails based on a search query."""
    headers = {'Authorization': f'Bearer {token}'}
    try:
        url = f"{GRAPH_API_ENDPOINT}/me/messages"
        if query:
            # Properly encode and format the search query
            encoded_query = quote(query)
            url += f"?$search=\"{encoded_query}\""

        response = requests.get(url, headers=headers)
        logging.info(f"Graph API URL: {url}")
        logging.info(f"Response Status Code: {response.status_code}")
        logging.info(f"Response Content: {response.text}")  # Log the full response

        response.raise_for_status()  # Raise an error for non-200 responses

        emails = response.json().get('value', [])
        if not emails:
            logging.info("No emails found.")
            return []

        # Log and return the list of emails
        for email in emails:
            logging.info(f"Email: {email['subject']} (ID: {email['id']})")

        return emails
    except requests.exceptions.HTTPError as e:
        logging.error(f"Error listing Outlook emails: {e}")
        return []


def download_outlook_attachment(token, message_id, attachment_id, save_path):
    """Download an attachment from a specific Outlook email message."""
    headers = {'Authorization': f'Bearer {token}'}
    try:
        url = f"{GRAPH_API_ENDPOINT}/me/messages/{message_id}/attachments/{attachment_id}"

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Extract attachment data and save it
        attachment = response.json()
        if not attachment.get('contentBytes'):
            logging.error("No attachment data found.")
            return None

        file_data = base64.b64decode(attachment['contentBytes'])
        with open(save_path, 'wb') as file:
            file.write(file_data)

        logging.info(f"Attachment saved to {save_path}")
        return os.path.abspath(save_path)
    except Exception as e:
        logging.error(f"Error downloading attachment: {str(e)}")
        return None


def download_specific_outlook_attachment(email_subject):
    """Search for an email by subject and download the first attachment."""
    token = authenticate_outlook()
    if not token:
        logging.error("Unable to authenticate with Outlook.")
        return None

    # Sanitize the query to remove unsupported characters
    sanitized_subject = sanitize_query(email_subject)
    emails = list_outlook_emails(token, query=sanitized_subject)
    if not emails:
        logging.error("No emails found with the given subject.")
        return None

    # Find first email with an attachment
    message_id = emails[0]['id']
    headers = {'Authorization': f'Bearer {token}'}
    try:
        # Get email details to find attachments
        url = f"{GRAPH_API_ENDPOINT}/me/messages/{message_id}?$expand=attachments"
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        email_data = response.json()
        attachments = email_data.get('attachments', [])
        if not attachments:
            logging.info("No attachments found in this email.")
            return None

        # Download the first attachment
        attachment_id = attachments[0]['id']
        filename = attachments[0]['name']
        save_path = os.path.join("downloads", f"{uuid.uuid4().hex}_{filename}")

        return download_outlook_attachment(token, message_id, attachment_id, save_path)
    except Exception as e:
        logging.error(f"Error retrieving attachments: {str(e)}")
        return None


if __name__ == '__main__':
    subject_to_search = "Test Email Subject"
    downloaded_file = download_specific_outlook_attachment(subject_to_search)
    if downloaded_file:
        logging.info(f"Successfully downloaded attachment: {downloaded_file}")
    else:
        logging.error(f"Failed to download the attachment.")
