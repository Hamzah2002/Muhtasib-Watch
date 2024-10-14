from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_page()

    def setup_page(self):
        """
        Set up the layout and widgets for the Home page.
        """
        # Create the main vertical layout for the Home page
        layout = QVBoxLayout()

        # Add a welcome label
        welcome_label = QLabel("Welcome to Muhtasib Watch\n\nSelect a feature from the sidebar to begin.\n\n"
                               "Below is a quick guide on how to use each feature effectively.")
        welcome_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        welcome_label.setStyleSheet("color: #FFFFFF; padding: 20px;")
        welcome_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome_label)

        # Add a scroll area for the user guide
        scroll_area = QScrollArea()
        scroll_area_widget = QWidget()
        scroll_area_layout = QVBoxLayout()

        ### URL Checker Section ###
        url_checker_label = QLabel("🔗 URL Checker - How to Use:")
        url_checker_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        url_checker_label.setStyleSheet("color: #FFFFFF; padding: 10px;")
        scroll_area_layout.addWidget(url_checker_label)

        url_checker_description = QLabel(
            "1. Right-click on the embedded link (an embedded link is a clickable word).\n"
            "2. Click on 'Copy Link'.\n"
            "3. Paste the copied link in the URL Checker input area.\n\n"
            "Note: Never click the link before verifying its safety!"
        )
        url_checker_description.setStyleSheet("color: #A0A0A0; padding-left: 20px;")
        scroll_area_layout.addWidget(url_checker_description)

        url_checker_image = QLabel()
        url_checker_image.setPixmap(
            QPixmap("resources/manuals/url_checker_example.png").scaledToWidth(600, Qt.SmoothTransformation))
        url_checker_image.setAlignment(Qt.AlignCenter)
        scroll_area_layout.addWidget(url_checker_image)

        ### DKIM/SPF Analysis Section ###
        dkim_spf_label = QLabel("📧 DKIM/SPF Analysis - How to Use:")
        dkim_spf_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        dkim_spf_label.setStyleSheet("color: #FFFFFF; padding: 10px;")
        scroll_area_layout.addWidget(dkim_spf_label)

        dkim_spf_description = QLabel(
            "1. Open the email you want to analyze.\n"
            "2. Click on the three dots (⋮) menu icon in the top-right corner.\n"
            "3. Select 'Copy to clipboard'.\n"
            "4. Paste the copied headers into the DKIM/SPF Analysis input area."
        )
        dkim_spf_description.setStyleSheet("color: #A0A0A0; padding-left: 20px;")
        scroll_area_layout.addWidget(dkim_spf_description)

        dkim_spf_image = QLabel()
        dkim_spf_image.setPixmap(
            QPixmap("resources/manuals/dkim_spf_example.png").scaledToWidth(600, Qt.SmoothTransformation))
        dkim_spf_image.setAlignment(Qt.AlignCenter)
        scroll_area_layout.addWidget(dkim_spf_image)

        ### Attachment Scanning Section ###
        attachment_label = QLabel("📎 Attachment Scanning - How to Use:")
        attachment_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        attachment_label.setStyleSheet("color: #FFFFFF; padding: 10px;")
        scroll_area_layout.addWidget(attachment_label)

        attachment_description = QLabel(
            "<b>Download Gmail Attachments:</b><br>"
            "Use this feature to download files that are inside an email.<br><br>"
            "1. Right-click on the attachment in the email.<br>"
            "2. Click on 'Copy Link'.<br>"
            "3. Paste the link into the Attachment Scanning input area.<br>"
            "4. Click on the 'Download Gmail Attachments' button to retrieve the file.<br><br>"
            "<b>Scan Attachments:</b><br>"
            "Use this feature to analyze links with downloadable content, similar to the URL Checker.<br><br>"
            "1. Right-click on the download link you want to scan.<br>"
            "2. Click on 'Copy Link'.<br>"
            "3. Paste the link into the Attachment Scanning input area.<br>"
            "4. Click on the 'Scan Attachments' button to perform a security check on the file."
        )
        attachment_description.setStyleSheet("color: #A0A0A0; padding-left: 20px;")
        attachment_description.setWordWrap(True)
        scroll_area_layout.addWidget(attachment_description)

        ### Phishing Analysis Section ###
        phishing_label = QLabel("🔍 Phishing Analysis - How to Use:")
        phishing_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        phishing_label.setStyleSheet("color: #FFFFFF; padding: 10px;")
        scroll_area_layout.addWidget(phishing_label)

        phishing_description = QLabel(
            "1. Copy the entire email content you want to analyze.\n"
            "2. Paste it into the Phishing Analysis text area.\n"
            "3. Click 'Analyze Email'.\n"
            "4. The tool will provide a prediction of whether the email is legitimate or a potential phishing attempt, along with a keyword analysis."
        )
        phishing_description.setStyleSheet("color: #A0A0A0; padding-left: 20px;")
        scroll_area_layout.addWidget(phishing_description)

        phishing_image = QLabel()
        phishing_image.setPixmap(
            QPixmap("resources/manuals/phishing_analysis_example.png").scaledToWidth(600, Qt.SmoothTransformation))
        phishing_image.setAlignment(Qt.AlignCenter)
        scroll_area_layout.addWidget(phishing_image)

        ### Adding the Scroll Area ###
        scroll_area_widget.setLayout(scroll_area_layout)
        scroll_area.setWidget(scroll_area_widget)
        scroll_area.setWidgetResizable(True)

        # Add the scroll area to the main layout
        layout.addWidget(scroll_area)

        # Set the layout for the HomePage widget
        self.setLayout(layout)
