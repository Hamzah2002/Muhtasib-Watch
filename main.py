import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, QTextEdit

# Import your modules
import dkim_spf_validator
import attachment_scanner
import url_checker


class MuhtasibWatch(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.attachment_scanner = attachment_scanner.AttachmentScanner()  # Initialize AttachmentScanner

    def initUI(self):
        self.setWindowTitle("Muhtasib Watch - Email Security Analyzer")
        self.setGeometry(100, 100, 900, 650)  # Resize the window for better spacing

        # URL Input Field
        self.url_label = QLabel("Enter URL:", self)
        self.url_label.move(20, 20)
        self.url_input = QLineEdit(self)
        self.url_input.move(150, 20)
        self.url_input.setFixedWidth(500)

        # Button to Check URL
        self.check_url_button = QPushButton("Check URL", self)
        self.check_url_button.move(670, 20)
        self.check_url_button.clicked.connect(self.check_url)

        # DKIM/SPF Input Field (Multi-line)
        self.dkim_label = QLabel("Enter SPF/DKIM Headers:", self)
        self.dkim_label.move(20, 60)
        self.dkim_input = QTextEdit(self)  # Multi-line input for DKIM/SPF headers
        self.dkim_input.move(150, 60)
        self.dkim_input.setFixedHeight(100)
        self.dkim_input.setFixedWidth(500)

        # Button to Check DKIM/SPF
        self.check_dkim_button = QPushButton("Check DKIM/SPF", self)
        self.check_dkim_button.move(670, 60)
        self.check_dkim_button.clicked.connect(self.check_dkim_spf)

        # Attachment URLs Input Field (Multi-line)
        self.attachment_label = QLabel("Enter Attachment URLs (comma-separated):", self)
        self.attachment_label.move(20, 180)
        self.attachment_input = QTextEdit(self)  # Multi-line input for attachment URLs
        self.attachment_input.move(150, 180)
        self.attachment_input.setFixedHeight(60)
        self.attachment_input.setFixedWidth(500)

        # Button to Scan Attachments
        self.scan_attachment_button = QPushButton("Scan Attachments", self)
        self.scan_attachment_button.move(670, 180)
        self.scan_attachment_button.clicked.connect(self.scan_attachments)

        # Text Area to Show Results
        self.results_area = QTextEdit(self)
        self.results_area.move(20, 260)
        self.results_area.setFixedSize(850, 350)

    # Function to Check URLs using url_checker.py
    def check_url(self):
        url = self.url_input.text().strip()
        if url:
            expanded_url = url_checker.expand_url(url)  # First expand the URL if it's shortened
            if expanded_url:
                result = url_checker.check_url_virustotal(expanded_url)
                self.results_area.setText(f"URL Check Result:\n\n{result}")
            else:
                self.results_area.setText(f"Invalid or suspicious redirections for URL: {url}")

    # Function to Check DKIM/SPF using dkim_spf_validator.py
    def check_dkim_spf(self):
        dkim_headers = self.dkim_input.toPlainText().strip()
        if dkim_headers:
            result = dkim_spf_validator.analyze_email(dkim_headers)  # Analyze the DKIM and SPF headers
            self.results_area.setText(f"DKIM/SPF Analysis Result:\n\n{result}")

    # Function to Scan Attachments using attachment_scanner.py
    def scan_attachments(self):
        attachment_urls = self.attachment_input.toPlainText().strip().split(',')
        attachment_urls = [url.strip() for url in attachment_urls if url.strip()]  # Clean up URLs

        if attachment_urls:
            results = self.attachment_scanner.analyze_attachments(attachment_urls)
            result_text = "Attachment Scan Results:\n\n"
            for result in results:
                result_text += f"URL: {result.get('url', 'N/A')}\n"
                result_text += f"File Path: {result.get('file_path', 'N/A')}\n"
                result_text += f"Status: {result['status']}\n"
                result_text += f"Details: {result['details']}\n\n"
            self.results_area.setText(result_text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MuhtasibWatch()
    window.show()
    sys.exit(app.exec_())
