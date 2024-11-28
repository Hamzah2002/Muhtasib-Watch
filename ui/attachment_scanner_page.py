from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QHBoxLayout, QFrame, QProgressBar
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QFont


class AttachmentScannerWorker(QThread):
    """
    Worker thread for scanning attachments using the backend.
    """
    progress_signal = pyqtSignal(int)
    result_signal = pyqtSignal(dict)

    def __init__(self, attachment_url, scanner, attachment_type="url"):
        super().__init__()
        self.attachment_url = attachment_url
        self.scanner = scanner
        self.attachment_type = attachment_type

    def run(self):
        try:
            # Simulate progress during the download and scan process
            for progress in range(0, 100, 10):
                self.sleep(1)  # Simulate work being done
                self.progress_signal.emit(progress)

            # Perform the actual scan using the scanner backend
            if self.attachment_type == "url":
                result = self.scanner.analyze_attachment(self.attachment_url)
            elif self.attachment_type == "gmail":
                result = self.scanner.download_gmail_attachment(self.attachment_url)
            elif self.attachment_type == "outlook":
                result = self.scanner.download_outlook_attachment(self.attachment_url)
            else:
                result = {"status": "error", "details": "Unknown attachment type"}

            self.progress_signal.emit(100)  # Mark as complete
            self.result_signal.emit(result)  # Emit the scan results
        except Exception as e:
            self.result_signal.emit({"status": "error", "details": str(e)})


class AttachmentScannerPage(QWidget):
    def __init__(self, scanner_backend):
        """
        Initialize the page with a backend scanner instance.
        """
        super().__init__()
        self.scanner_backend = scanner_backend  # Store the backend instance
        self.setup_page()
        self.scan_worker = None  # Initialize worker as None

    def setup_page(self):
        """
        Set up the layout and widgets for the Attachment Scanning feature.
        """
        # Create the main vertical layout for the page
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Title Section
        title_label = QLabel("📎 Attachment Scanning")
        title_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title_label.setStyleSheet("color: #007BFF; margin-bottom: 10px;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Subtitle
        subtitle_label = QLabel(
            "Use this feature to scan email attachments for security risks such as viruses, malware, and phishing threats."
        )
        subtitle_label.setFont(QFont("Segoe UI", 14))
        subtitle_label.setStyleSheet("color: #495057; margin-bottom: 20px; line-height: 1.6;")
        subtitle_label.setWordWrap(True)
        subtitle_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(subtitle_label)

        # Input Section Header
        input_section_label = QLabel("🔗 Enter the Attachment URL or Email Subject:")
        input_section_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        input_section_label.setStyleSheet("color: #333333; margin-bottom: 10px;")
        main_layout.addWidget(input_section_label)

        # Input Text Area
        self.attachment_input = QTextEdit()
        self.attachment_input.setFixedHeight(100)
        self.attachment_input.setPlaceholderText("Paste the attachment URL or enter the email subject here...")
        self.attachment_input.setStyleSheet("""
            QTextEdit {
                background-color: #F8F9FA;
                border: 2px solid #CED4DA;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                color: #495057;
            }
            QTextEdit:focus {
                border: 2px solid #007BFF;
            }
        """)
        main_layout.addWidget(self.attachment_input)

        # Button Section
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        # Scan URL Button
        self.scan_attachment_button = QPushButton("🔍 Scan URL Attachment")
        self.scan_attachment_button.setFixedHeight(50)
        self.scan_attachment_button.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #0056B3;
            }
            QPushButton:pressed {
                background-color: #004085;
            }
        """)
        self.scan_attachment_button.clicked.connect(lambda: self.start_scan("url"))
        button_layout.addWidget(self.scan_attachment_button)

        # Download Gmail Button
        self.download_gmail_button = QPushButton("📧 Scan Gmail Attachment")
        self.download_gmail_button.setFixedHeight(50)
        self.download_gmail_button.setStyleSheet("""
            QPushButton {
                background-color: #28A745;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1E7E34;
            }
        """)
        self.download_gmail_button.clicked.connect(lambda: self.start_scan("gmail"))
        button_layout.addWidget(self.download_gmail_button)

        # Download Outlook Button
        self.download_outlook_button = QPushButton("📤 Scan Outlook Attachment")
        self.download_outlook_button.setFixedHeight(50)
        self.download_outlook_button.setStyleSheet("""
            QPushButton {
                background-color: #FFC107;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #E0A800;
            }
            QPushButton:pressed {
                background-color: #C69500;
            }
        """)
        self.download_outlook_button.clicked.connect(lambda: self.start_scan("outlook"))
        button_layout.addWidget(self.download_outlook_button)

        main_layout.addLayout(button_layout)

        # Progress Bar Section
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #CED4DA;
                border-radius: 8px;
                background-color: #F8F9FA;
                height: 30px;
            }
            QProgressBar::chunk {
                background-color: #007BFF;
                border-radius: 8px;
            }
            QProgressBar[textVisible="true"] {
                text-align: center;
                font-size: 16px;
                font-weight: bold;
                color: #333333;
            }
        """)
        self.progress_bar.setValue(0)  # Initialize progress to 0
        main_layout.addWidget(self.progress_bar)

        # Divider Line
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setFrameShadow(QFrame.Sunken)
        divider.setStyleSheet("color: #CED4DA;")
        main_layout.addWidget(divider)

        # Result Section Header
        result_section_label = QLabel("📝 Scan Results:")
        result_section_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        result_section_label.setStyleSheet("color: #333333; margin-top: 20px;")
        main_layout.addWidget(result_section_label)

        # Results Text Area
        self.attachment_result_area = QTextEdit()
        self.attachment_result_area.setFixedHeight(200)
        self.attachment_result_area.setReadOnly(True)
        self.attachment_result_area.setPlaceholderText("Scan results will appear here...")
        self.attachment_result_area.setStyleSheet("""
            QTextEdit {
                background-color: #F8F9FA;
                border: 2px solid #CED4DA;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                color: #495057;
            }
        """)
        main_layout.addWidget(self.attachment_result_area)

        # Set the layout for the AttachmentScannerPage widget
        self.setLayout(main_layout)

    def start_scan(self, attachment_type):
        """
        Starts the scanning process with backend integration.
        """
        # Get the input URL or email subject
        attachment_input = self.attachment_input.toPlainText().strip()

        # Validate input
        if not attachment_input:
            self.attachment_result_area.setText("Please provide a valid attachment URL or email subject.")
            return

        # Clear previous results and reset progress bar
        self.attachment_result_area.clear()
        self.progress_bar.setValue(0)

        # Initialize the worker thread for scanning
        self.scan_worker = AttachmentScannerWorker(attachment_input, self.scanner_backend, attachment_type)
        self.scan_worker.progress_signal.connect(self.progress_bar.setValue)
        self.scan_worker.result_signal
