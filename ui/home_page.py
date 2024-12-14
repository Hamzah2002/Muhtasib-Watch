from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
import os
import sys

def resource_path(relative_path):
    """
    Get the absolute path to a resource, compatible with PyInstaller.
    """
    if hasattr(sys, '_MEIPASS'):
        # If running as a PyInstaller bundle
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

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
        welcome_label.setStyleSheet("color: #000000; padding: 20px;")  # Black for the welcome header
        welcome_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome_label)

        # a scroll area for the user guide
        scroll_area = QScrollArea()
        scroll_area_widget = QWidget()
        scroll_area_layout = QVBoxLayout()

        # ClamAV Setup Guide
        clamav_label = QLabel("🛠️ Setting Up ClamAV for Attachment Scanning")
        clamav_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        clamav_label.setStyleSheet("color: #FF5722; padding: 10px;")
        scroll_area_layout.addWidget(clamav_label)

        # Step 1 - Download and Install ClamAV
        download_label = QLabel("1. Download and Install ClamAV")
        download_label.setFont(QFont("Segoe UI", 14))
        download_label.setStyleSheet("color: #000000; padding-left: 20px;")
        scroll_area_layout.addWidget(download_label)

        download_link = QLabel('<a href="https://www.clamav.net/">https://www.clamav.net/</a>')
        download_link.setOpenExternalLinks(True)
        download_link.setStyleSheet("color: #1E90FF; padding-left: 40px;")
        scroll_area_layout.addWidget(download_link)

        # Step 2 - Locating Installation Directory
        step1_label = QLabel("2. Locate the ClamAV Installation Directory.")
        step1_label.setFont(QFont("Segoe UI", 14))
        step1_label.setStyleSheet("color: #000000; padding-left: 20px;")
        scroll_area_layout.addWidget(step1_label)

        step1_image = QLabel()
        step1_image.setPixmap(
            QPixmap(resource_path("resources/manuals/clamav1.png")).scaledToWidth(600, Qt.SmoothTransformation))
        step1_image.setAlignment(Qt.AlignCenter)
        scroll_area_layout.addWidget(step1_image)

        # Step 3 - Locate Config Files
        step2_label = QLabel(
            "3. Locate 'clamd.conf.example' and 'freshclam.conf.example' in the 'conf_examples' folder.")
        step2_label.setFont(QFont("Segoe UI", 14))
        step2_label.setStyleSheet("color: #000000; padding-left: 20px;")
        scroll_area_layout.addWidget(step2_label)

        step2_image = QLabel()
        step2_image.setPixmap(
            QPixmap(resource_path("resources/manuals/clamav2.png")).scaledToWidth(600, Qt.SmoothTransformation))
        step2_image.setAlignment(Qt.AlignCenter)
        scroll_area_layout.addWidget(step2_image)

        # Step 4 - Move and Rename Files
        step3_label = QLabel("4. Cut and Paste These Files to the Parent 'clamav' Folder and Rename Them:")
        step3_label.setFont(QFont("Segoe UI", 14))
        step3_label.setStyleSheet("color: #000000; padding-left: 20px;")
        scroll_area_layout.addWidget(step3_label)

        renamed_files_label = QLabel(
            "• Rename 'clamd.conf.example' to 'clamd.conf'\n• Rename 'freshclam.conf.example' to 'freshclam.conf'")
        renamed_files_label.setStyleSheet("color: #000000; padding-left: 40px;")
        scroll_area_layout.addWidget(renamed_files_label)

        step3_image = QLabel()
        step3_image.setPixmap(
            QPixmap(resource_path("resources/manuals/clamav3.png")).scaledToWidth(600, Qt.SmoothTransformation))
        step3_image.setAlignment(Qt.AlignCenter)
        scroll_area_layout.addWidget(step3_image)

        # Step 5 - Edit and Save Files
        step4_label = QLabel("5. Open Both Files and Remove the Line Containing 'Example', Then Save.")
        step4_label.setFont(QFont("Segoe UI", 14))
        step4_label.setStyleSheet("color: #000000; padding-left: 20px;")
        scroll_area_layout.addWidget(step4_label)

        step4_image = QLabel()
        step4_image.setPixmap(
            QPixmap(resource_path("resources/manuals/clamav4.png")).scaledToWidth(600, Qt.SmoothTransformation))
        step4_image.setAlignment(Qt.AlignCenter)
        scroll_area_layout.addWidget(step4_image)

        # Final Instructions
        final_instructions = QLabel(
            "Final Step:\n\n"
            "• Run 'clamscan.exe' to Update the Database.\n"
            "• Run 'clamd.exe' to Start the ClamAV Service in the Background."
        )
        final_instructions.setFont(QFont("Segoe UI", 14))
        final_instructions.setStyleSheet("color: #000000; padding-left: 20px;")
        scroll_area_layout.addWidget(final_instructions)




        ### URL Checker Section ###
        url_checker_label = QLabel("🔗 URL Checker - How to Use:")
        url_checker_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        url_checker_label.setStyleSheet("color: #03A9F4; padding: 10px;")  # Changed color to blue
        scroll_area_layout.addWidget(url_checker_label)

        url_checker_description = QLabel(
            "1. Right-click on the embedded link (an embedded link is a clickable word).\n"
            "2. Click on 'Copy Link'.\n"
            "3. Paste the copied link in the URL Checker input area.\n\n"
            "Note: Never click the link before verifying its safety!"
        )
        url_checker_description.setStyleSheet("color: #000000; padding-left: 20px;")  # Normal black for subtext
        scroll_area_layout.addWidget(url_checker_description)

        url_checker_image = QLabel()
        url_checker_image.setPixmap(
            QPixmap(resource_path("resources/manuals/url_checker_example.png")).scaledToWidth(600, Qt.SmoothTransformation)
        )
        url_checker_image.setAlignment(Qt.AlignCenter)
        scroll_area_layout.addWidget(url_checker_image)

        ### DKIM/SPF Analysis Section ###
        dkim_spf_label = QLabel("📧 DKIM/SPF Analysis - How to Use:")
        dkim_spf_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        dkim_spf_label.setStyleSheet("color: #4CAF50; padding: 10px;")  # Changed color to green
        scroll_area_layout.addWidget(dkim_spf_label)

        dkim_spf_description = QLabel(
            "1. Open the email you want to analyze.\n"
            "2. Click on the three dots (⋮) menu icon in the top-right corner.\n"
            "3. Select 'Copy to clipboard'.\n"
            "4. Paste the copied headers into the DKIM/SPF Analysis input area."
        )
        dkim_spf_description.setStyleSheet("color: #000000; padding-left: 20px;")  # Changed color to light gray
        scroll_area_layout.addWidget(dkim_spf_description)

        dkim_spf_image = QLabel()
        dkim_spf_image.setPixmap(
            QPixmap(resource_path("resources/manuals/dkim_spf_example.png")).scaledToWidth(600, Qt.SmoothTransformation)
        )
        dkim_spf_image.setAlignment(Qt.AlignCenter)
        scroll_area_layout.addWidget(dkim_spf_image)

        ### Attachment Scanning Section ###
        attachment_label = QLabel("📎 Attachment Scanning - How to Use:")
        attachment_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        attachment_label.setStyleSheet("color: #FF5722; padding: 10px;")  # Changed color to orange
        scroll_area_layout.addWidget(attachment_label)

        attachment_description_part1 = QLabel(
            "<b>Download Gmail Attachments:</b><br>"
            "Use this feature to download files that are inside an email.<br><br>"
            "1. Right-click on the attachment in the email.<br>"
            "2. Click on 'Copy Link'.<br>"
            "3. Paste the link into the Attachment Scanning input area.<br>"
            "4. Click on the 'Download Gmail Attachments' button to retrieve the file.<br><br>"
        )
        attachment_description_part1.setStyleSheet("color: #000000; padding-left: 20px;")  # Changed color to light gray
        attachment_description_part1.setWordWrap(True)
        scroll_area_layout.addWidget(attachment_description_part1)

        # Image for "Download Gmail Attachments"
        download_gmail_image = QLabel()
        download_gmail_image.setPixmap(
            QPixmap(resource_path("resources/manuals/download_gmail_example.png")).scaledToWidth(600, Qt.SmoothTransformation)
        )
        download_gmail_image.setAlignment(Qt.AlignCenter)
        scroll_area_layout.addWidget(download_gmail_image)

        attachment_description_part2 = QLabel(
            "<b>Downloadable link:</b><br>"
            "Use this feature to analyze links with downloadable content, similar to the URL Checker.<br><br>"
            "1. Right-click on the download link you want to scan.<br>"
            "2. Click on 'Copy Link'.<br>"
            "3. Paste the link into the Attachment Scanning input area.<br>"
            "4. Click on the 'Scan Attachments' button to perform a security check on the file."
        )
        attachment_description_part2.setStyleSheet("color: #000000; padding-left: 20px;")  # Changed color to light gray
        attachment_description_part2.setWordWrap(True)
        scroll_area_layout.addWidget(attachment_description_part2)

        # Image for "Scan Attachments"
        scan_attachments_image = QLabel()
        scan_attachments_image.setPixmap(
            QPixmap(resource_path("resources/manuals/download_link_example.png")).scaledToWidth(600, Qt.SmoothTransformation)
        )
        scan_attachments_image.setAlignment(Qt.AlignCenter)
        scroll_area_layout.addWidget(scan_attachments_image)

        ### Phishing Analysis Section ###
        phishing_label = QLabel("🔍 Phishing Analysis - How to Use:")
        phishing_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        phishing_label.setStyleSheet("color: #9C27B0; padding: 10px;")  # Changed color to purple
        scroll_area_layout.addWidget(phishing_label)

        phishing_description = QLabel(
            "1. Copy the entire email content you want to analyze.\n"
            "2. Paste it into the Phishing Analysis text area.\n"
            "3. Click 'Analyze Email'.\n"
            "4. The tool will provide a prediction of whether the email is legitimate or a potential phishing attempt, along with a keyword analysis."
        )
        phishing_description.setStyleSheet("color: #000000; padding-left: 20px;")  # Changed color to light gray
        scroll_area_layout.addWidget(phishing_description)

        ### Adding the Scroll Area ###
        scroll_area_widget.setLayout(scroll_area_layout)
        scroll_area.setWidget(scroll_area_widget)
        scroll_area.setWidgetResizable(True)

        # Add the scroll area to the main layout
        layout.addWidget(scroll_area)

        # Set the layout for the HomePage widget
        self.setLayout(layout)
