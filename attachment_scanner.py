import os
import requests
import pyclamd
import logging
import uuid  # Add this to generate unique filenames
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(level=logging.INFO)


class AttachmentScanner:
    def __init__(self):
        self.cd = None  # Don't connect immediately

    def _connect_clamav(self):
        if not self.cd:  # Only connect if not already connected
            try:
                self.cd = pyclamd.ClamdAgnostic()
                if self.cd.ping():
                    logging.info("Successfully connected to ClamAV daemon.")
                else:
                    logging.error("Failed to connect to ClamAV. Ensure ClamAV daemon is running.")
                    self.cd = None
                    raise Exception("ClamAV connection failed.")
            except Exception as e:
                logging.error(f"Error connecting to ClamAV: {str(e)}")
                self.cd = None
                raise Exception("ClamAV connection could not be established.")

    def download_attachment(self, url):
        if not self._is_valid_url(url):
            logging.error(f"Invalid URL: {url}")
            return None

        if "mail.google.com" in url:
            logging.error(f"Invalid operation: The URL '{url}' appears to be a Gmail link. Use the 'Download Gmail Attachments' button instead.")
            return None

        try:
            file_name = f"downloaded_attachment_{uuid.uuid4().hex}"
            logging.info(f"Downloading attachment: {file_name} from {url}")
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                with open(file_name, 'wb') as file:
                    file.write(response.content)
                logging.info(f"Attachment saved as {file_name}")
                return os.path.abspath(file_name)
            else:
                logging.error(f"Failed to download attachment from {url}. Status code: {response.status_code}")
                return None
        except requests.RequestException as re:
            logging.error(f"Error downloading attachment from {url}: {str(re)}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            return None

    def scan_file_with_clamav(self, file_path, url=None):
        self._connect_clamav()  # Ensure ClamAV is connected only when scanning
        if not self.cd:
            return {"url": url, "file_path": file_path, "status": "error", "details": "ClamAV is not available for scanning. Ensure ClamAV is running."}

        try:
            if os.path.exists(file_path):
                logging.info(f"File exists, scanning file {file_path} with ClamAV")
                result = self.cd.scan_file(file_path)
                if result is None:
                    return {"url": url, "file_path": file_path, "status": "clean", "details": "No malware detected"}
                else:
                    return {"url": url, "file_path": file_path, "status": "infected", "details": result}
            else:
                logging.error(f"File {file_path} does not exist at scan time.")
                return {"url": url, "file_path": file_path, "status": "error", "details": "File not found at scan time"}
        except Exception as e:
            logging.error(f"Error scanning file {file_path} with ClamAV: {str(e)}")
            return {
                "url": url,
                "file_path": file_path,
                "status": "error",
                "details": f"File path check failure: {str(e)}. This may be caused by antivirus software restrictions or running the program in a sandboxed environment."
            }

    def analyze_attachment(self, attachment_url):
        """
        Analyze a single attachment from a given URL.
        """
        if "mail.google.com" in attachment_url:
            return {
                "url": attachment_url,
                "status": "error",
                "details": "Gmail URLs cannot be processed with this function. Use the 'Download Gmail Attachments' option instead."
            }

        file_path = self.download_attachment(attachment_url)
        if file_path:
            scan_result = self.scan_file_with_clamav(file_path, attachment_url)
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    logging.info(f"Deleted the file {file_path} after scanning")
            except Exception as e:
                logging.error(f"Error deleting file {file_path}: {str(e)}")
                return {
                    "url": attachment_url,
                    "file_path": file_path,
                    "status": "warning",
                    "details": f"File scanned successfully, but deletion failed: {str(e)}"
                }
            return scan_result
        else:
            return {"url": attachment_url, "status": "error", "details": "Failed to download attachment"}

    @staticmethod
    def _is_valid_url(url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
