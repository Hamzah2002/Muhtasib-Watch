# main.py
import sys
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication
from ui import Ui_MainWindow  # Import the separate UI file
import dkim_spf_validator
import attachment_scanner
import url_checker


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
        """
        Run the attachment scanning in a separate thread.
        """
        # Perform the attachment scanning using the AttachmentScanner instance
        results = self.scanner.analyze_attachments(self.attachment_urls)

        # Format the results into a string to display in the UI
        result_text = "Attachment Scan Results:\n\n"
        for result in results:
            result_text += f"URL: {result.get('url', 'N/A')}\n"
            result_text += f"File Path: {result.get('file_path', 'N/A')}\n"
            result_text += f"Status: {result['status']}\n"
            result_text += f"Details: {result['details']}\n\n"

        # Emit the formatted result text back to the main thread
        self.update_result.emit(result_text)


class MuhtasibWatch(Ui_MainWindow):
    """
    Main application class that handles UI interactions and integrates functionality.
    """
    def __init__(self):
        super().__init__()
        self.attachment_scanner = attachment_scanner.AttachmentScanner()  # Initialize the AttachmentScanner
        self.scan_worker = None  # Placeholder for the threading worker
        self.connectUI()  # Connect the UI buttons to the respective logic

    def connectUI(self):
        """
        Connect the buttons in the UI to their corresponding functions.
        """
        self.check_url_button.clicked.connect(self.check_url)  # URL Checker Page
        self.check_dkim_button.clicked.connect(self.check_dkim_spf)  # DKIM/SPF Page
        self.scan_attachment_button.clicked.connect(self.scan_attachments)  # Attachment Scanning Page

    def check_url(self):
        """
        Functionality for checking URLs using the VirusTotal API.
        """
        url = self.url_input.text().strip()
        if url:
            # Get the redirection chain and final URL from the URL checker
            redirect_chain, final_url = url_checker.expand_url(url)

            if final_url:
                # Create a formatted string for the redirection details
                redirection_text = f"Initial URL: {url}\n\n"
                if redirect_chain:
                    redirection_text += "Redirection Chain:\n" + "\n".join(redirect_chain) + "\n\n"
                redirection_text += f"Final URL after Redirection: {final_url}\n\n"

                # Check the final URL using VirusTotal and display results
                result = url_checker.check_url_virustotal(final_url)
                self.url_result_area.setText(f"URL Check Result:\n\n{redirection_text}{result}")
            else:
                self.url_result_area.setText(f"Invalid or suspicious redirections for URL: {url}")

    def check_dkim_spf(self):
        """
        Functionality for analyzing DKIM and SPF headers.
        """
        dkim_headers = self.dkim_input.toPlainText().strip()
        if dkim_headers:
            # Run DKIM and SPF analysis on the input headers and display the results
            result = dkim_spf_validator.analyze_email(dkim_headers)
            self.dkim_result_area.setText(f"DKIM/SPF Analysis Result:\n\n{result}")

    def scan_attachments(self):
        """
        Start the attachment scanning process with a loading message.
        """
        # Clear the previous results and show a loading message
        self.attachment_result_area.setText("Sandboxing... Please wait.\nThis may take a few moments depending on the file size and type.")

        # Collect the URLs from the input area, split by commas, and clean up whitespace
        attachment_urls = self.attachment_input.toPlainText().strip().split(',')
        attachment_urls = [url.strip() for url in attachment_urls if url.strip()]

        if attachment_urls:
            # Initialize the worker thread with the scanner instance and attachment URLs
            self.scan_worker = AttachmentScannerWorker(self.attachment_scanner, attachment_urls)
            self.scan_worker.update_result.connect(self.display_scan_results)  # Connect signal to result display function
            self.scan_worker.start()  # Start the scanning process in a separate thread

    def display_scan_results(self, result_text):
        """
        Update the UI with the results from the attachment scan.
        """
        self.attachment_result_area.setText(result_text)  # Display the formatted scan results in the UI


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MuhtasibWatch()
    window.show()
    sys.exit(app.exec_())
