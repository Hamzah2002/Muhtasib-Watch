import sys
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication
from ui import Ui_MainWindow  # Import the separate UI file
import dkim_spf_validator
import attachment_scanner
import url_checker
from src.phishing_analyzer import PhishingAnalyzer  # Import the PhishingAnalyzer class
from gmail_downloader import authenticate_gmail, list_gmail_attachments, download_gmail_attachment  # Gmail integration


class AttachmentScannerWorker(QThread):
    """
    Worker thread to run the attachment scanning process without freezing the main UI.
    """
    update_result = pyqtSignal(str)  # Signal to send results back to the main thread

    def __init__(self, scanner, attachment_urls, local_files=None):
        super().__init__()
        self.scanner = scanner  # Reference to the AttachmentScanner instance
        self.attachment_urls = attachment_urls  # List of URLs to scan
        self.local_files = local_files  # Optional: List of local file paths to scan

    def run(self):
        try:
            result_text = "Attachment Scan Results:\n\n"

            # If there are local files, scan them first
            if self.local_files:
                for file in self.local_files:
                    scan_result = self.scanner.scan_file_with_clamav(file)
                    result_text += f"File: {file}\nStatus: {scan_result['status']}\nDetails: {scan_result['details']}\n\n"

            # If there are URLs, scan them as well
            if self.attachment_urls:
                results = self.scanner.analyze_attachments(self.attachment_urls)
                for result in results:
                    result_text += f"URL: {result.get('url', 'N/A')}\n"
                    result_text += f"File Path: {result.get('file_path', 'N/A')}\n"
                    result_text += f"Status: {result['status']}\n"
                    result_text += f"Details: {result['details']}\n\n"

            # Emit the formatted result text back to the main thread
            self.update_result.emit(result_text)
        except Exception as e:
            self.update_result.emit(f"Error during attachment scanning: {str(e)}")


class MuhtasibWatch(Ui_MainWindow):
    """
    Main application class that handles UI interactions and integrates functionality.
    """

    def __init__(self):
        super().__init__()
        try:
            print("Initializing application components...")
            self.attachment_scanner = attachment_scanner.AttachmentScanner()  # Initialize the AttachmentScanner
            print("Attachment scanner initialized successfully.")

            self.phishing_analyzer = PhishingAnalyzer("models/phishing_model.pkl",
                                                      "models/vectorizer.pkl")  # Load the phishing detection model
            print("Phishing analyzer initialized successfully.")

            self.scan_worker = None  # Placeholder for the threading worker
            self.connectUI()  # Connect the UI buttons to the respective logic
            print("UI components connected successfully.")
        except Exception as e:
            print(f"Error initializing application components: {e}")

    def connectUI(self):
        """
        Connect the buttons in the UI to their corresponding functions.
        """
        try:
            self.check_url_button.clicked.connect(self.check_url)  # URL Checker Page
            self.check_dkim_button.clicked.connect(self.check_dkim_spf)  # DKIM/SPF Page
            self.scan_attachment_button.clicked.connect(self.scan_attachments)  # Attachment Scanning Page
            self.check_phishing_button.clicked.connect(self.check_phishing)  # Phishing Analysis Page
            self.download_gmail_button.clicked.connect(self.download_gmail_attachments)  # Gmail Attachment Download
            print("All UI buttons connected to functions.")
        except Exception as e:
            print(f"Error in connecting UI components: {e}")

    def check_url(self):
        try:
            url = self.url_input.text().strip()
            if url:
                redirect_chain, final_url = url_checker.expand_url(url)
                if final_url:
                    redirection_text = f"Initial URL: {url}\n\n"
                    if redirect_chain:
                        redirection_text += "Redirection Chain:\n" + "\n".join(redirect_chain) + "\n\n"
                    redirection_text += f"Final URL after Redirection: {final_url}\n\n"
                    result = url_checker.check_url_virustotal(final_url)
                    self.url_result_area.setText(f"URL Check Result:\n\n{redirection_text}{result}")
                else:
                    self.url_result_area.setText(f"Invalid or suspicious redirections for URL: {url}")
            else:
                self.url_result_area.setText("Please enter a valid URL.")
        except Exception as e:
            print(f"Error in check_url: {e}")
            self.url_result_area.setText(f"Error in URL checking: {str(e)}")

    def check_dkim_spf(self):
        try:
            dkim_headers = self.dkim_input.toPlainText().strip()
            if dkim_headers:
                result = dkim_spf_validator.analyze_email(dkim_headers)
                self.dkim_result_area.setText(f"DKIM/SPF Analysis Result:\n\n{result}")
        except Exception as e:
            self.dkim_result_area.setText(f"Error in DKIM/SPF analysis: {str(e)}")

    def scan_attachments(self):
        try:
            self.attachment_result_area.setText(
                "Sandboxing... Please wait.\nThis may take a few moments depending on the file size and type.")
            attachment_urls = self.attachment_input.toPlainText().strip().split(
                ',')  # `QTextEdit` uses `.toPlainText()`
            attachment_urls = [url.strip() for url in attachment_urls if url.strip()]

            if attachment_urls:
                self.scan_worker = AttachmentScannerWorker(self.attachment_scanner, attachment_urls)
                self.scan_worker.update_result.connect(self.display_scan_results)
                self.scan_worker.start()
        except Exception as e:
            self.attachment_result_area.setText(f"Error in attachment scanning: {str(e)}")

    def download_gmail_attachments(self):
        try:
            service = authenticate_gmail()
            attachments = list_gmail_attachments(service, user_id='me', query='has:attachment')

            if not attachments:
                self.attachment_result_area.setText("No attachments found in Gmail.")
                return

            local_files = []
            for attachment in attachments:
                save_path = f"downloads/{attachment['filename']}"
                local_files.append(
                    download_gmail_attachment(service, 'me', attachment['message_id'], attachment['attachment_id'],
                                              save_path))

            self.scan_worker = AttachmentScannerWorker(self.attachment_scanner, [], local_files=local_files)
            self.scan_worker.update_result.connect(self.display_scan_results)
            self.scan_worker.start()
        except Exception as e:
            self.attachment_result_area.setText(f"Error downloading Gmail attachments: {str(e)}")

    def check_phishing(self):
        try:
            email_text = self.email_input.toPlainText().strip()
            if email_text:
                prediction = self.phishing_analyzer.predict(email_text)
                keyword_analysis = self.phishing_analyzer.analyze_keywords(email_text)
                detailed_report = f"Prediction: {prediction}\n\n{keyword_analysis}"
                self.phishing_result_area.setText(detailed_report)
        except Exception as e:
            self.phishing_result_area.setText(f"Error in phishing analysis: {str(e)}")

    def display_scan_results(self, result_text):
        try:
            self.attachment_result_area.setText(result_text)
        except Exception as e:
            self.attachment_result_area.setText(f"Error displaying scan results: {str(e)}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MuhtasibWatch()
    window.show()
    sys.exit(app.exec_())
