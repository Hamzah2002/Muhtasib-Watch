import sys
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication
from ui import Ui_MainWindow  # Import the separate UI file
import dkim_spf_validator
import attachment_scanner
import url_checker
from src.phishing_analyzer import PhishingAnalyzer  # Import the PhishingAnalyzer class


class AttachmentScannerWorker(QThread):
    """
    Worker thread to run the attachment scanning process without freezing the main UI.
    """
    update_result = pyqtSignal(str)  # Signal to send results back to the main thread

    def __init__(self, scanner, attachment_urls):
        super().__init__()
        self.scanner = scanner  # Reference to the AttachmentScanner instance
        self.attachment_urls = attachment_urls  # List of URLs to scan

    def run(self):
        try:
            # Perform the attachment scanning using the AttachmentScanner instance
            results = self.scanner.analyze_attachments(self.attachment_urls)
            result_text = "Attachment Scan Results:\n\n"
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
            print("All UI buttons connected to functions.")
        except Exception as e:
            print(f"Error in connecting UI components: {e}")

    def check_url(self):
        """
        Functionality for checking URLs using the VirusTotal API.
        """
        try:
            # If using QLineEdit for URL input, use `.text()`
            url = self.url_input.text().strip()  # This works if `self.url_input` is a QLineEdit
            if url:
                print(f"Checking URL: {url}")
                redirect_chain, final_url = url_checker.expand_url(url)
                if final_url:
                    redirection_text = f"Initial URL: {url}\n\n"
                    if redirect_chain:
                        redirection_text += "Redirection Chain:\n" + "\n".join(redirect_chain) + "\n\n"
                    redirection_text += f"Final URL after Redirection: {final_url}\n\n"
                    result = url_checker.check_url_virustotal(final_url)
                    print(f"VirusTotal Check Result: {result}")
                    self.url_result_area.setText(f"URL Check Result:\n\n{redirection_text}{result}")
                else:
                    self.url_result_area.setText(f"Invalid or suspicious redirections for URL: {url}")
            else:
                self.url_result_area.setText("Please enter a valid URL.")
        except Exception as e:
            print(f"Error in check_url: {e}")
            self.url_result_area.setText(f"Error in URL checking: {str(e)}")

    def check_dkim_spf(self):
        """
        Functionality for analyzing DKIM and SPF headers.
        """
        try:
            dkim_headers = self.dkim_input.toPlainText().strip()  # QTextEdit uses `.toPlainText()`
            if dkim_headers:
                print("Analyzing DKIM/SPF headers...")
                result = dkim_spf_validator.analyze_email(dkim_headers)
                self.dkim_result_area.setText(f"DKIM/SPF Analysis Result:\n\n{result}")
        except Exception as e:
            print(f"Error in check_dkim_spf: {e}")
            self.dkim_result_area.setText(f"Error in DKIM/SPF analysis: {str(e)}")

    def scan_attachments(self):
        """
        Start the attachment scanning process with a loading message.
        """
        try:
            self.attachment_result_area.setText(
                "Sandboxing... Please wait.\nThis may take a few moments depending on the file size and type.")
            attachment_urls = self.attachment_input.toPlainText().strip().split(',')  # `QTextEdit` uses `.toPlainText()`
            attachment_urls = [url.strip() for url in attachment_urls if url.strip()]

            if attachment_urls:
                print(f"Starting attachment scan for URLs: {attachment_urls}")
                self.scan_worker = AttachmentScannerWorker(self.attachment_scanner, attachment_urls)
                self.scan_worker.update_result.connect(self.display_scan_results)
                self.scan_worker.start()
        except Exception as e:
            print(f"Error in scan_attachments: {e}")
            self.attachment_result_area.setText(f"Error in attachment scanning: {str(e)}")

    def check_phishing(self):
        """
        Functionality for phishing analysis.
        """
        try:
            email_text = self.email_input.toPlainText().strip()  # `QTextEdit` uses `.toPlainText()`
            if email_text:
                print(f"Analyzing email text for phishing: {email_text[:50]}...")  # Print first 50 characters for reference
                prediction = self.phishing_analyzer.predict(email_text)
                keyword_analysis = self.phishing_analyzer.analyze_keywords(email_text)
                detailed_report = f"Prediction: {prediction}\n\n{keyword_analysis}"
                self.phishing_result_area.setText(detailed_report)
        except Exception as e:
            print(f"Error in check_phishing: {e}")
            self.phishing_result_area.setText(f"Error in phishing analysis: {str(e)}")

    def display_scan_results(self, result_text):
        """
        Update the UI with the results from the attachment scan.
        """
        try:
            print("Displaying scan results...")
            self.attachment_result_area.setText(result_text)
        except Exception as e:
            print(f"Error in display_scan_results: {e}")


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        window = MuhtasibWatch()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Error in main: {e}")
