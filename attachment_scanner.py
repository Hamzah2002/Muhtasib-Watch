import os
import requests
import pyclamd
import logging
import uuid  # For generating unique filenames
from urllib.parse import urlparse
import tempfile  # For temporary directory handling

# Configure logging
logging.basicConfig(level=logging.INFO)


class AttachmentScanner:
    def __init__(self, temp_dir=None):
        """
        Initialize the AttachmentScanner.

        :param temp_dir: Directory for temporary files (optional).
        """
        self.temp_dir = temp_dir or tempfile.gettempdir()  # Use provided temp_dir or fallback to system temp
        self.cd = None  # ClamAV connection (initialized lazily)
        logging.info(f"AttachmentScanner initialized with temp_dir: {self.temp_dir}")

    def _connect_clamav(self):
        """
        Connect to the ClamAV daemon using pyclamd.
        """
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
        """
        Download an attachment from the provided URL and save it to a temporary directory.

        :param url: The URL of the attachment to download.
        :return: The full path to the downloaded file, or None if the download failed.
        """
        if not self._is_valid_url(url):
            logging.error(f"Invalid URL: {url}")
            return None

        if "mail.google.com" in url:
            logging.error(f"Invalid operation: The URL '{url}' appears to be a Gmail link. Use the 'Download Gmail Attachments' button instead.")
            return None

        try:
            # Generate a unique file path in the temp directory
            file_name = os.path.join(self.temp_dir, f"attachment_{uuid.uuid4().hex}")
            logging.info(f"Downloading attachment: {file_name} from {url}")

            # Download the file with a timeout
            response = requests.get(url, timeout=60)
            if response.status_code == 200:
                # Save the file to the specified location
                with open(file_name, 'wb') as file:
                    file.write(response.content)
                logging.info(f"Attachment saved as {file_name}")
                return file_name
            else:
                logging.error(f"Failed to download attachment from {url}. Status code: {response.status_code}")
                return None
        except requests.RequestException as re:
            logging.error(f"Error downloading attachment from {url}: {str(re)}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            return None

    @staticmethod
    def _is_valid_url(url):
        """
        Validate the provided URL.

        :param url: The URL to validate.
        :return: True if the URL is valid, False otherwise.
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False

    def scan_file_with_clamav(self, file_path, url=None):
        """
        Scans a file using ClamAV.
        :param file_path: Path to the file to scan.
        :param url: (Optional) URL associated with the file for reference.
        :return: A dictionary with scan results.
        """
        self._connect_clamav()  # Ensure ClamAV is connected only when scanning
        if not self.cd:
            return {
                "url": url,
                "file_path": file_path,
                "status": "error",
                "details": "ClamAV is not available for scanning. Ensure ClamAV is running."
            }

        try:
            if os.path.exists(file_path):
                logging.info(f"Scanning file {file_path} with ClamAV")
                result = self.cd.scan_file(file_path)
                if result is None:
                    status = "clean"
                    details = "No malware detected"
                else:
                    status = "infected"
                    details = result

                # Log the scan result
                logging.info(f"Scan result for {file_path}: {status} - {details}")

                # Delete the file after scanning
                try:
                    os.remove(file_path)
                    logging.info(f"File {file_path} deleted after scanning.")
                except Exception as delete_error:
                    logging.error(f"Failed to delete file {file_path}: {delete_error}")

                return {
                    "url": url,
                    "file_path": file_path,
                    "status": status,
                    "details": details
                }
            else:
                logging.error(f"File {file_path} does not exist at scan time.")
                return {
                    "url": url,
                    "file_path": file_path,
                    "status": "error",
                    "details": "File not found at scan time"
                }
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
