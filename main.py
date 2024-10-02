import os
import sys
import uuid
import time  # Add this for timing issues
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication
from ui import Ui_MainWindow
import dkim_spf_validator
import attachment_scanner
import url_checker
from src.phishing_analyzer import PhishingAnalyzer
from gmail_downloader import authenticate_gmail, list_gmail_attachments, download_gmail_attachment, extract_message_id, get_correct_attachment_id
import logging

# Configure logging for better traceability
logging.basicConfig(level=logging.INFO)


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

            # Scan local files
            for file in self.local_files:
                if os.path.exists(file):
                    logging.info(f"Scanning file: {file}")
                    # Add a short delay to ensure file is completely saved
                    time.sleep(1)  # Small delay to avoid timing issues
                    scan_result = self.scanner.scan_file_with_clamav(file)
                    result_text += f"File: {file}\nStatus: {scan_result['status']}\nDetails: {scan_result['details']}\n\n"
                else:
                    result_text += f"File: {file} not found, skipping scan.\n\n"

            # Analyze attachment URLs
            if self.attachment_urls:
                results = self.scanner.analyze_attachments(self.attachment_urls)
                for result in results:
                    result_text += f"URL: {result.get('url', 'N/A')}\n"
                    result_text += f"File Path: {result.get('file_path', 'N/A')}\n"
                    result_text += f"Status: {result['status']}\n"
                    result_text += f"Details: {result['details']}\n\n"

            self.update_result.emit(result_text)
        except Exception as e:
            self.update_result.emit(f"Error during attachment scanning: {str(e)}")


class MuhtasibWatch(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        try:
            self.attachment_scanner = attachment_scanner.AttachmentScanner()
            self.phishing_analyzer = PhishingAnalyzer("models/phishing_model.pkl", "models/vectorizer.pkl")
            self.scan_worker = None
            self.connectUI()
        except Exception as e:
            print(f"Error initializing application components: {e}")

    def connectUI(self):
        try:
            self.check_url_button.clicked.connect(self.check_url)
            self.check_dkim_button.clicked.connect(self.check_dkim_spf)
            self.scan_attachment_button.clicked.connect(self.scan_attachments)
            self.check_phishing_button.clicked.connect(self.check_phishing)
            self.download_gmail_button.clicked.connect(self.download_gmail_attachments)
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
            self.attachment_result_area.setText("Sandboxing... Please wait.\nThis may take a few moments depending on the file size and type.")
            attachment_urls = self.attachment_input.toPlainText().strip().split(',')
            attachment_urls = [url.strip() for url in attachment_urls if url.strip()]

            if attachment_urls:
                self.scan_worker = AttachmentScannerWorker(self.attachment_scanner, attachment_urls=attachment_urls)
                self.scan_worker.update_result.connect(self.display_scan_results)
                self.scan_worker.start()
        except Exception as e:
            self.attachment_result_area.setText(f"Error in attachment scanning: {str(e)}")

    def download_gmail_attachments(self):
        try:
            gmail_input = self.attachment_input.toPlainText().strip()
            gmail_urls = [url.strip() for url in gmail_input.split(',') if url.strip()]

            service = authenticate_gmail()
            if any("mail.google.com" in url for url in gmail_urls):
                for url in gmail_urls:
                    msg_id = extract_message_id(url)
                    if msg_id:
                        attachment_id = get_correct_attachment_id(service, 'me', msg_id)
                        if attachment_id:
                            save_path = f"downloads/{uuid.uuid4().hex}.dat"
                            local_file = download_gmail_attachment(service, 'me', msg_id, attachment_id, save_path)
                            if local_file and os.path.exists(local_file):
                                logging.info(f"Successfully downloaded: {local_file}")
                                time.sleep(1)  # Add a short delay before scanning
                                scan_result = self.attachment_scanner.scan_file_with_clamav(local_file)
                                self.display_scan_results(f"File: {local_file}\nStatus: {scan_result['status']}\nDetails: {scan_result['details']}\n\n")
                            else:
                                self.attachment_result_area.setText(f"Failed to download attachment from Gmail link: {url}")
                        else:
                            self.attachment_result_area.setText(f"Could not retrieve attachment ID for message: {msg_id}")
                    else:
                        self.attachment_result_area.setText(f"Invalid Gmail link: {url}. Unable to extract message ID.")
                return

            attachments = list_gmail_attachments(service, user_id='me', query='has:attachment')
            if not attachments:
                self.attachment_result_area.setText("No attachments found in Gmail.")
                return

            local_files = []
            for attachment in attachments:
                save_path = f"downloads/{uuid.uuid4().hex}_{attachment['filename']}"
                local_files.append(download_gmail_attachment(service, 'me', attachment['message_id'], attachment['attachment_id'], save_path))

            self.scan_worker = AttachmentScannerWorker(self.attachment_scanner, local_files=local_files)
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
