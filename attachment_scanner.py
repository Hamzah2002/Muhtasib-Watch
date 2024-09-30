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
        self.cd = None
        self._connect_clamav()

    def _connect_clamav(self):
        """
        Establish a connection to the ClamAV server.
        """
        try:
            # Try to connect to ClamAV using the default ClamdAgnostic mode.
            self.cd = pyclamd.ClamdAgnostic()
            if self.cd.ping():
                logging.info("Successfully connected to ClamAV daemon.")
            else:
                logging.error("Failed to connect to ClamAV. Ensure ClamAV daemon is running.")
                self.cd = None
        except Exception as e:
            logging.error(f"Error connecting to ClamAV: {str(e)}")
            self.cd = None

    def _is_clamav_available(self):
        """
        Check if ClamAV is available for scanning.
        """
        if self.cd and self.cd.ping():
            logging.info("ClamAV is available for scanning.")
            return True
        else:
            logging.error("ClamAV is not available for scanning. Ensure ClamAV is running.")
            return False

    def download_attachment(self, url):
        """
        Download the attachment from the provided URL and save it locally with a unique filename.
        Returns the file path where the attachment is saved or None on failure.
        """
        if not self._is_valid_url(url):
            logging.error(f"Invalid URL: {url}")
            return None

        try:
            # Generate a unique file name using a UUID
            file_name = f"downloads/downloaded_attachment_{uuid.uuid4().hex}"
            logging.info(f"Downloading attachment: {file_name} from {url}")

            response = requests.get(url, timeout=30)  # Set a timeout to avoid hanging

            if response.status_code == 200:
                # Ensure the directory exists
                os.makedirs(os.path.dirname(file_name), exist_ok=True)

                with open(file_name, 'wb') as file:
                    file.write(response.content)
                logging.info(f"Attachment saved as {file_name}")
                return os.path.abspath(file_name)  # Return the full file path
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
        """
        Scan the downloaded file using ClamAV for malware.
        Returns a detailed scan result with additional context.
        """
        # Check if ClamAV is available
        if not self._is_clamav_available():
            return {"url": url, "file_path": file_path, "status": "error", "details": "ClamAV is not available for scanning. Ensure ClamAV is running."}

        try:
            if os.path.exists(file_path):  # Check if file exists before scanning
                logging.info(f"Scanning file {file_path} with ClamAV")
                result = self.cd.scan_file(file_path)
                if result is None:
                    return {"url": url, "file_path": file_path, "status": "clean", "details": "No malware detected"}
                else:
                    return {"url": url, "file_path": file_path, "status": "infected", "details": result}
            else:
                logging.error(f"File {file_path} does not exist at scan time.")
                return {"url": url, "file_path": file_path, "status": "error", "details": "File not found at scan time."}
        except Exception as e:
            logging.error(f"Error scanning file {file_path} with ClamAV: {str(e)}")
            return {
                "url": url,
                "file_path": file_path,
                "status": "error",
                "details": f"File path check failure: {str(e)}. This may be caused by antivirus software restrictions or running the program in a sandboxed environment."
            }

    def analyze_attachments(self, attachment_urls):
        """
        Analyze attachments by downloading and scanning them using ClamAV.
        Returns a structured result for each attachment, including URLs.
        """
        results = []

        for url in attachment_urls:
            logging.info(f"Analyzing attachment from URL: {url}")
            file_path = self.download_attachment(url)  # Use unique filenames for each download
            if file_path:
                scan_result = self.scan_file_with_clamav(file_path, url)
                results.append(scan_result)

                # Ensure the file is deleted after scanning
                try:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        logging.info(f"Deleted the file {file_path} after scanning")
                except Exception as e:
                    logging.error(f"Error deleting file {file_path}: {str(e)}")
                    results.append({
                        "url": url,
                        "file_path": file_path,
                        "status": "warning",
                        "details": f"File scanned successfully, but deletion failed: {str(e)}"
                    })
            else:
                results.append({"url": url, "status": "error", "details": "Failed to download attachment"})

        return results

    @staticmethod
    def _is_valid_url(url):
        """Validate the given URL."""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
