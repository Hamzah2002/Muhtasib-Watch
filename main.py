# main.py
import sys
from PyQt5.QtWidgets import QApplication
from ui import Ui_MainWindow  # Import the separate UI file with navigation setup
import dkim_spf_validator
import attachment_scanner
import url_checker


class MuhtasibWatch(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.attachment_scanner = attachment_scanner.AttachmentScanner()  # Initialize the scanner
        self.connectUI()  # Connect the UI buttons to logic

    def connectUI(self):
        # Connect buttons on each specific page to their respective functions
        self.check_url_button.clicked.connect(self.check_url)  # URL Checker Page
        self.check_dkim_button.clicked.connect(self.check_dkim_spf)  # DKIM/SPF Page
        self.scan_attachment_button.clicked.connect(self.scan_attachments)  # Attachment Scanning Page

    def check_url(self):
        # URL Checker Functionality
        url = self.url_input.text().strip()
        if url:
            # Get the redirection chain and final URL from expand_url()
            redirect_chain, final_url = url_checker.expand_url(url)

            if final_url:
                # Create a formatted string for the redirection details
                redirection_text = f"Initial URL: {url}\n\n"
                if redirect_chain:
                    redirection_text += "Redirection Chain:\n" + "\n".join(redirect_chain) + "\n\n"
                redirection_text += f"Final URL after Redirection: {final_url}\n\n"

                # Check the final URL using VirusTotal
                result = url_checker.check_url_virustotal(final_url)

                # Display the full redirection and VirusTotal check result in the UI (specific results area for URL checker)
                self.url_result_area.setText(f"URL Check Result:\n\n{redirection_text}{result}")
            else:
                self.url_result_area.setText(f"Invalid or suspicious redirections for URL: {url}")

    def check_dkim_spf(self):
        # DKIM/SPF Analysis Functionality
        dkim_headers = self.dkim_input.toPlainText().strip()
        if dkim_headers:
            # Run DKIM and SPF analysis on the input headers
            result = dkim_spf_validator.analyze_email(dkim_headers)
            self.dkim_result_area.setText(f"DKIM/SPF Analysis Result:\n\n{result}")

    def scan_attachments(self):
        # Attachment Scanning Functionality
        # Collect the URLs from the text area, split by commas, and clean up whitespace
        attachment_urls = self.attachment_input.toPlainText().strip().split(',')
        attachment_urls = [url.strip() for url in attachment_urls if url.strip()]

        if attachment_urls:
            # Run the attachment analysis
            results = self.attachment_scanner.analyze_attachments(attachment_urls)

            # Format the results to display in the text area for attachments
            result_text = "Attachment Scan Results:\n\n"
            for result in results:
                result_text += f"URL: {result.get('url', 'N/A')}\n"
                result_text += f"File Path: {result.get('file_path', 'N/A')}\n"
                result_text += f"Status: {result['status']}\n"
                result_text += f"Details: {result['details']}\n\n"

            # Display the formatted attachment scan results
            self.attachment_result_area.setText(result_text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MuhtasibWatch()
    window.show()
    sys.exit(app.exec_())
