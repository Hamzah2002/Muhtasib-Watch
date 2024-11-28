import sys
import os
import uuid
import time
import logging
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication
from ui.main_window import Ui_MainWindow
from gmail_downloader import authenticate_gmail, download_gmail_attachment, extract_message_id, get_correct_attachment_id
from src.phishing_analyzer import PhishingAnalyzer
import attachment_scanner
import dkim_spf_validator
import url_checker
from outlook_downloader import download_specific_outlook_attachment
from outlook_downloader import authenticate_outlook
from setup_clamav import is_clamav_installed, setup_clamav
import requests
import pyclamd
import tempfile  # Import tempfile for temporary file handling
from urllib.parse import urlparse
from urllib3.util.retry import Retry  # Import Retry for request retries
from requests.adapters import HTTPAdapter




if not is_clamav_installed():
    print("ClamAV is not installed or running. Setting it up...")
    setup_clamav()
else:
    print("ClamAV is installed and running. Proceeding with the application...")

# Function to get the log file path
def get_log_path():
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller's _MEIPASS directory for the bundled app
        return os.path.join(sys._MEIPASS, "app.log")
    return os.path.join(os.getcwd(), "app.log")


TEMP_DIR = tempfile.mkdtemp(prefix="MuhtasibWatch_")


# Configure Logging
logging.basicConfig(
    filename="app.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logging.info("Logging setup complete.")  # Test log to ensure logging works






class AttachmentScannerWorker(QThread):
    update_result = pyqtSignal(str)

    def __init__(self, scanner, attachment_urls=None, local_files=None):
        super().__init__()
        self.scanner = scanner
        self.attachment_urls = attachment_urls if attachment_urls else []
        self.local_files = local_files if local_files else []

    def run(self):
        try:
            result_text = "Attachment Scan Results:\n\n"
            logging.debug("Started attachment scanning.")

            for file in self.local_files:
                if os.path.exists(file):
                    logging.info(f"Scanning file: {file}")
                    time.sleep(1)  # Ensure the file is completely written
                    scan_result = self.scanner.scan_file_with_clamav(file)
                    result_text += f"File: {file}\nStatus: {scan_result['status']}\nDetails: {scan_result['details']}\n\n"
                else:
                    logging.warning(f"File: {file} not found. Skipping scan.")
                    result_text += f"File: {file} not found. Skipping scan.\n\n"

            if self.attachment_urls:
                logging.debug(f"Analyzing attachment URL: {self.attachment_urls[0]}")
                result = self.scanner.analyze_attachment(self.attachment_urls[0])
                result_text += f"URL: {result.get('url', 'N/A')}\n"
                result_text += f"File Path: {result.get('file_path', 'N/A')}\n"
                result_text += f"Status: {result['status']}\n"
                result_text += f"Details: {result['details']}\n\n"

            self.update_result.emit(result_text)
            logging.debug("Attachment scanning completed.")
        except Exception as e:
            logging.error(f"Error during attachment scanning: {e}", exc_info=True)
            self.update_result.emit(f"Error during attachment scanning: {str(e)}")


class MuhtasibWatch(Ui_MainWindow):
    def __init__(self, scanner_backend):
        """
        Initialize the MuhtasibWatch application.

        :param scanner_backend: The AttachmentScanner instance for scanning operations.
        """
        # Pass the scanner_backend to Ui_MainWindow
        super().__init__(scanner_backend=scanner_backend)
        try:
            logging.info("Initializing MuhtasibWatch application.")

            # Store scanner_backend as an instance variable for use throughout the class
            self.attachment_scanner = scanner_backend

            # Connect UI components
            self.connectUI()

            # Initialize the phishing analyzer with model paths
            self.phishing_analyzer = PhishingAnalyzer(
                self.resource_path("models/phishing_model.pkl"),
                self.resource_path("models/vectorizer.pkl")
            )

            # Workers for scanning and Outlook operations
            self.scan_worker = None
            self.outlook_worker = None

        except Exception as e:
            logging.error(f"Error initializing application components: {e}", exc_info=True)

    @staticmethod
    def resource_path(relative_path):
        """
        Get the absolute path to a resource (handles PyInstaller environments).
        """
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)


    def connectUI(self):
        try:
            # Connecting buttons to respective functionalities
            self.url_checker_page.check_url_button.clicked.connect(self.check_url)
            self.dkim_spf_page.check_dkim_button.clicked.connect(self.check_dkim_spf)
            self.attachment_scanner_page.scan_attachment_button.clicked.connect(self.scan_attachments)
            self.attachment_scanner_page.download_outlook_button.clicked.connect(self.download_outlook_attachments)
            self.phishing_analysis_page.check_phishing_button.clicked.connect(self.check_phishing)
            self.attachment_scanner_page.download_gmail_button.clicked.connect(self.download_gmail_attachments)
        except Exception as e:
            logging.error(f"Error in connecting UI components: {e}")

    def check_url(self):
        try:
            url = self.url_checker_page.url_input.text().strip()
            if url:
                redirect_chain, final_url = url_checker.expand_url(url)
                if final_url:
                    redirection_text = f"Initial URL: {url}\n\n"
                    if redirect_chain:
                        redirection_text += "Redirection Chain:\n" + "\n".join(redirect_chain) + "\n\n"
                    redirection_text += f"Final URL after Redirection: {final_url}\n\n"
                    result = url_checker.check_url_virustotal(final_url)
                    self.url_checker_page.url_result_area.setText(f"URL Check Result:\n\n{redirection_text}{result}")
                else:
                    self.url_checker_page.url_result_area.setText(f"Invalid or suspicious redirections for URL: {url}")
            else:
                self.url_checker_page.url_result_area.setText("Please enter a valid URL.")
        except Exception as e:
            self.url_checker_page.url_result_area.setText(f"Error in URL checking: {str(e)}")

    def check_dkim_spf(self):
        try:
            dkim_headers = self.dkim_spf_page.dkim_input.toPlainText().strip()
            if dkim_headers:
                result = dkim_spf_validator.analyze_email(dkim_headers)
                self.dkim_spf_page.dkim_result_area.setText(f"DKIM/SPF Analysis Result:\n\n{result}")
        except Exception as e:
            self.dkim_spf_page.dkim_result_area.setText(f"Error in DKIM/SPF analysis: {str(e)}")

    def scan_attachments(self):
        try:
            self.attachment_scanner_page.attachment_result_area.setText(
                "Sandboxing... Please wait. This may take a few moments depending on the file size and type."
            )
            attachment_url = self.attachment_scanner_page.attachment_input.toPlainText().strip()

            if attachment_url:
                self.scan_worker = AttachmentScannerWorker(self.attachment_scanner, attachment_urls=[attachment_url])
                self.scan_worker.update_result.connect(self.display_scan_results)
                self.scan_worker.start()
            else:
                self.attachment_scanner_page.attachment_result_area.setText("Please enter a valid attachment URL.")
        except Exception as e:
            self.attachment_scanner_page.attachment_result_area.setText(f"Error in attachment scanning: {str(e)}")

    def download_gmail_attachments(self):
        try:
            self.attachment_scanner_page.attachment_result_area.setText(
                "Downloading attachment from Gmail... Please wait."
            )
            gmail_url = self.attachment_scanner_page.attachment_input.toPlainText().strip()

            if gmail_url:
                logging.info(f"Downloading attachment from Gmail URL: {gmail_url}")
                service = authenticate_gmail()

                if "mail.google.com" in gmail_url:
                    msg_id = extract_message_id(gmail_url)
                    if msg_id:
                        attachment_id = get_correct_attachment_id(service, 'me', msg_id)
                        if attachment_id:
                            save_path = f"downloads/{uuid.uuid4().hex}.dat"
                            local_file = download_gmail_attachment(service, 'me', msg_id, attachment_id, save_path)
                            if local_file and os.path.exists(local_file):
                                logging.info(f"Successfully downloaded: {local_file}")
                                time.sleep(1)  # Add a short delay before scanning
                                scan_result = self.attachment_scanner.scan_file_with_clamav(local_file)
                                self.display_scan_results(
                                    f"File: {local_file}\nStatus: {scan_result['status']}\nDetails: {scan_result['details']}\n\n"
                                )
                            else:
                                logging.warning(f"Failed to download attachment from Gmail link: {gmail_url}")
                                self.attachment_scanner_page.attachment_result_area.setText(
                                    f"Failed to download attachment from Gmail link: {gmail_url}"
                                )
                        else:
                            logging.warning(f"Could not retrieve attachment ID for message: {msg_id}")
                            self.attachment_scanner_page.attachment_result_area.setText(
                                f"Could not retrieve attachment ID for message: {msg_id}"
                            )
                    else:
                        logging.warning(f"Invalid Gmail link: {gmail_url}. Unable to extract message ID.")
                        self.attachment_scanner_page.attachment_result_area.setText(
                            f"Invalid Gmail link: {gmail_url}. Unable to extract message ID."
                        )
                else:
                    logging.warning("Invalid Gmail URL provided.")
                    self.attachment_scanner_page.attachment_result_area.setText("Please provide a valid Gmail URL.")
            else:
                logging.warning("No Gmail URL provided.")
                self.attachment_scanner_page.attachment_result_area.setText("Please enter a valid Gmail URL.")
        except Exception as e:
            logging.error(f"Error downloading Gmail attachment: {e}", exc_info=True)
            self.attachment_scanner_page.attachment_result_area.setText(f"Error downloading Gmail attachment: {str(e)}")

    def download_outlook_attachments(self):
        try:
            email_subject = self.attachment_scanner_page.attachment_input.toPlainText().strip()

            if not email_subject:
                self.attachment_scanner_page.attachment_result_area.setText("Please enter a valid email subject.")
                return

            self.attachment_scanner_page.attachment_result_area.setText("Starting Outlook operation...")

            # Start the worker
            self.outlook_worker = OutlookWorker(email_subject)
            self.outlook_worker.result_signal.connect(self.display_outlook_results)
            self.outlook_worker.message_signal.connect(self.display_authentication_message)
            self.outlook_worker.start()

        except Exception as e:
            self.attachment_scanner_page.attachment_result_area.setText(f"Error: {str(e)}")

    def display_authentication_message(self, message):
        self.attachment_scanner_page.attachment_result_area.append(message)

    def display_outlook_results(self, result_text):
        """Display the results of the Outlook operation in the GUI."""
        self.attachment_scanner_page.attachment_result_area.setText(result_text)

    def check_phishing(self):
        try:
            email_text = self.phishing_analysis_page.email_input.toPlainText().strip()
            if email_text:
                logging.info("Starting phishing analysis.")
                prediction = self.phishing_analyzer.predict(email_text)
                keyword_analysis = self.phishing_analyzer.analyze_keywords(email_text)
                detailed_report = f"Prediction: {prediction}\n\n{keyword_analysis}"
                logging.info("Phishing analysis completed successfully.")
                self.phishing_analysis_page.phishing_result_area.setText(detailed_report)
            else:
                logging.warning("No email text provided for phishing analysis.")
                self.phishing_analysis_page.phishing_result_area.setText("Please enter the email text.")
        except Exception as e:
            logging.error(f"Error in phishing analysis: {e}", exc_info=True)
            self.phishing_analysis_page.phishing_result_area.setText(f"Error in phishing analysis: {str(e)}")

    def display_scan_results(self, result_text):
        try:
            self.attachment_scanner_page.attachment_result_area.setText(result_text)
        except Exception as e:
            self.attachment_scanner_page.attachment_result_area.setText(f"Error displaying scan results: {str(e)}")


class OutlookWorker(QThread):
    result_signal = pyqtSignal(str)  # Signal to send results to the GUI
    message_signal = pyqtSignal(str)  # Signal to send authentication messages to the GUI

    def __init__(self, subject):
        super().__init__()
        self.subject = subject  # The subject to search for

    def run(self):
        try:
            # Define a callback to send authentication messages to the GUI
            def message_callback(message):
                self.message_signal.emit(message)

            # Authenticate and handle the workflow
            token = authenticate_outlook(message_callback=message_callback)
            if not token:
                self.result_signal.emit("Authentication failed.")
                return

            # Perform the attachment download
            result_text = f"Searching for emails with subject: {self.subject}\n"
            downloaded_file = download_specific_outlook_attachment(self.subject)

            if downloaded_file:
                result_text += f"Attachment downloaded successfully: {downloaded_file}"
            else:
                result_text += "No attachments found for the given subject."

            self.result_signal.emit(result_text)
        except Exception as e:
            self.result_signal.emit(f"Error during Outlook operation: {str(e)}")


if __name__ == '__main__':
    try:
        logging.info("Application started.")

        # Create a temporary directory for file handling
        temp_dir = tempfile.mkdtemp(prefix="MuhtasibWatch_")
        logging.info(f"Temporary directory for attachment scanning: {temp_dir}")

        # Initialize the AttachmentScanner with the temporary directory
        scanner_backend = attachment_scanner.AttachmentScanner(temp_dir=temp_dir)

        # Initialize the main application window
        app = QApplication(sys.argv)
        window = MuhtasibWatch(scanner_backend=scanner_backend)  # Pass scanner_backend to MuhtasibWatch
        window.show()

        logging.info("Application is running.")

        # Start the application
        sys.exit(app.exec_())
    except Exception as e:
        logging.error(f"Unhandled exception occurred: {e}", exc_info=True)
        print(f"Unhandled exception: {e}")

