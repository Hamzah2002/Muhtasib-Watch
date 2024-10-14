from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton

class AttachmentScannerPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_page()

    def setup_page(self):
        """
        Set up the layout and widgets for the Attachment Scanning feature.
        """
        # Create the main vertical layout for the Attachment Scanner page
        layout = QVBoxLayout()
        layout.setSpacing(20)  # Set space between widgets

        # Create and configure the input field for attachment URLs
        self.attachment_label = QLabel("Enter Attachment URLs (comma-separated):")
        self.attachment_input = QTextEdit()
        self.attachment_input.setFixedHeight(150)
        self.attachment_input.setPlaceholderText("e.g., https://example.com/file1, https://another.com/file2")

        # Create the 'Scan Attachments' button
        self.scan_attachment_button = QPushButton("Scan Attachments")

        # Create the 'Download Gmail Attachments' button
        self.download_gmail_button = QPushButton("Download Gmail Attachments")

        # Create the result display area
        self.attachment_result_area = QTextEdit()
        self.attachment_result_area.setFixedHeight(300)
        self.attachment_result_area.setReadOnly(True)  # Make it read-only

        # Add widgets to the layout
        layout.addWidget(self.attachment_label)
        layout.addWidget(self.attachment_input)
        layout.addWidget(self.scan_attachment_button)
        layout.addWidget(self.download_gmail_button)
        layout.addWidget(self.attachment_result_area)

        # Set the layout for the AttachmentScannerPage widget
        self.setLayout(layout)
