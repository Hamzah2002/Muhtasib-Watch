# ui.py
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit, QLabel, QTextEdit

class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Muhtasib Watch - Email Security Analyzer")
        self.setGeometry(100, 100, 900, 650)

        # URL Input Field
        self.url_label = QLabel("Enter URL:", self)
        self.url_label.move(20, 20)
        self.url_input = QLineEdit(self)
        self.url_input.move(150, 20)
        self.url_input.setFixedWidth(500)

        # Button to Check URL
        self.check_url_button = QPushButton("Check URL", self)
        self.check_url_button.move(670, 20)

        # DKIM/SPF Input Field (Multi-line)
        self.dkim_label = QLabel("Enter SPF/DKIM Headers:", self)
        self.dkim_label.move(20, 60)
        self.dkim_input = QTextEdit(self)
        self.dkim_input.move(150, 60)
        self.dkim_input.setFixedHeight(100)
        self.dkim_input.setFixedWidth(500)

        # Button to Check DKIM/SPF
        self.check_dkim_button = QPushButton("Check DKIM/SPF", self)
        self.check_dkim_button.move(670, 60)

        # Attachment URLs Input Field (Multi-line)
        self.attachment_label = QLabel("Enter Attachment URLs (comma-separated):", self)
        self.attachment_label.move(20, 180)
        self.attachment_input = QTextEdit(self)
        self.attachment_input.move(150, 180)
        self.attachment_input.setFixedHeight(60)
        self.attachment_input.setFixedWidth(500)

        # Button to Scan Attachments
        self.scan_attachment_button = QPushButton("Scan Attachments", self)
        self.scan_attachment_button.move(670, 180)

        # Text Area to Show Results
        self.results_area = QTextEdit(self)
        self.results_area.move(20, 260)
        self.results_area.setFixedSize(850, 350)
