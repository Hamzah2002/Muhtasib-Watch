# main.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, QTextEdit

# Import the functions from your other files
import dkim_spf_validator  # Make sure this file has the necessary validation functions
import attachment_scanner  # Make sure this file has attachment scanning functions
import url_checker         # Ensure this file has URL checking functions

class MuhtasibWatch(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Muhtasib Watch - Email Security Analyzer")
        self.setGeometry(100, 100, 800, 600)

        # URL Input Field
        self.url_label = QLabel("Enter URL:", self)
        self.url_label.move(20, 20)
        self.url_input = QLineEdit(self)
        self.url_input.move(100, 20)
        self.url_input.setFixedWidth(500)

        # Button to Check URL
        self.check_url_button = QPushButton("Check URL", self)
        self.check_url_button.move(620, 20)
        self.check_url_button.clicked.connect(self.check_url)  # Connect to the check_url function

        # Text Area to Show Results
        self.results_area = QTextEdit(self)
        self.results_area.move(20, 70)
        self.results_area.setFixedSize(760, 400)

        # DKIM/SPF Input Field
        self.dkim_label = QLabel("Enter SPF/DKIM Info:", self)
        self.dkim_label.move(20, 500)
        self.dkim_input = QLineEdit(self)
        self.dkim_input.move(150, 500)
        self.dkim_input.setFixedWidth(300)

        # Button to Check DKIM/SPF
        self.check_dkim_button = QPushButton("Check DKIM/SPF", self)
        self.check_dkim_button.move(470, 500)
        self.check_dkim_button.clicked.connect(self.check_dkim_spf)

        # Button to Scan Attachments
        self.scan_attachment_button = QPushButton("Scan Attachments", self)
        self.scan_attachment_button.move(620, 500)
        self.scan_attachment_button.clicked.connect(self.scan_attachments)

    # Function to Check URLs using url_checker.py
    def check_url(self):
        url = self.url_input.text()
        if url:
            # Call the check_url_virustotal function from url_checker.py
            result = url_checker.check_url_virustotal(url)
            self.results_area.setText(f"URL Check Result:\n{result}")

    # Function to Check DKIM/SPF using dkim_spf_validator.py
    def check_dkim_spf(self):
        dkim_info = self.dkim_input.text()
        if dkim_info:
            # Call your DKIM/SPF validation function here
            result = dkim_spf_validator.validate_dkim_spf(dkim_info)
            self.results_area.setText(f"DKIM/SPF Check Result:\n{result}")

    # Function to Scan Attachments using attachment_scanner.py
    def scan_attachments(self):
        # You can customize this part to use a file picker dialog and scan the selected attachment
        result = attachment_scanner.scan_attachments()
        self.results_area.setText(f"Attachment Scan Result:\n{result}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MuhtasibWatch()
    window.show()
    sys.exit(app.exec_())
