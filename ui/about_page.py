from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
import os
import sys


def resource_path(relative_path):
    """
    Get the absolute path to a resource, compatible with PyInstaller.
    """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)  # If running as a PyInstaller bundle
    return os.path.join(os.path.abspath("."), relative_path)


class AboutPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_page()

    def setup_page(self):
        """
        Set up the layout and widgets for the About page.
        """
        # Create the main vertical layout for the About page
        layout = QVBoxLayout()
        layout.setSpacing(20)  # Set space between widgets
        layout.setContentsMargins(20, 20, 20, 20)  # Add some padding

        # Add logo (centered)
        logo_label = QLabel()
        logo_path = resource_path("resources/Logo.png")
        pixmap = QPixmap(logo_path)
        logo_label.setPixmap(pixmap.scaledToWidth(250, Qt.SmoothTransformation))  # Scale the logo to 250px width
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        # Add project title (centered)
        title_label = QLabel("Muhtasib Watch - Email Security Analyzer")
        title_label.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title_label.setStyleSheet("color: #007BFF; margin-bottom: 10px;")  # Bright blue for the title
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Application purpose and features (left-aligned with better spacing)
        purpose_label = QLabel(
            "<b>Muhtasib Watch</b> is an email security application designed to help users analyze and secure their "
            "emails against potential threats.<br><br>"
            "<b>Key Features:</b><br>"
            "<ol>"
            "<li><b>URL Checking:</b> Analyze embedded URLs for potential risks, even when they redirect.</li>"
            "<li><b>DKIM/SPF Analysis:</b> Validate DKIM and SPF headers to ensure email authenticity.</li>"
            "<li><b>Attachment Sandboxing:</b> Analyze attachments in a secure sandbox environment.</li>"
            "<li><b>Attachment Scanning:</b> Scan attachments for malware and other threats.</li>"
            "<li><b>Phishing Analysis:</b> Use machine learning to predict and flag phishing attempts.</li>"
            "<li><b>Email Integration (Optional):</b> Access Gmail/Outlook attachments for scanning.</li>"
            "</ol>"
            "<b>Note:</b> No login is required unless you wish to scan attachments in your email."
        )
        purpose_label.setStyleSheet(
            "color: #495057; padding: 10px; font-size: 16px; line-height: 1.6; background-color: #F8F9FA; "
            "border-radius: 8px;"
        )
        purpose_label.setWordWrap(True)
        purpose_label.setAlignment(Qt.AlignJustify)
        purpose_label.setTextFormat(Qt.RichText)
        layout.addWidget(purpose_label)

        # Acknowledgment (centered with subtle style)
        acknowledgment_label = QLabel(
            "This project is part of a Directed Study under the supervision of <b>Dr. Bruce Maxim</b> at the "
            "<b>University of Michigan-Dearborn</b>."
        )
        acknowledgment_label.setStyleSheet(
            "color: #6C757D; padding: 15px; font-size: 14px; font-style: italic; text-align: center;"
        )
        acknowledgment_label.setWordWrap(True)
        acknowledgment_label.setAlignment(Qt.AlignCenter)
        acknowledgment_label.setTextFormat(Qt.RichText)
        layout.addWidget(acknowledgment_label)

        # Contact Information (centered with clickable email link)
        contact_label = QLabel(
            "<b>Contact:</b><br>"
            "For any questions or feedback, please contact:<br>"
            "<b>Mouhamad Hamzah Ismail</b><br>"
            "<a href='mailto:mouhamad.hamzah@gmail.com' style='color:#007BFF;'>mouhamad.hamzah@gmail.com</a>"
        )
        contact_label.setStyleSheet(
            "color: #495057; padding: 10px; font-size: 14px; text-align: center;"
        )
        contact_label.setWordWrap(True)
        contact_label.setAlignment(Qt.AlignCenter)
        contact_label.setOpenExternalLinks(True)  # Allow email link to open default email client
        contact_label.setTextFormat(Qt.RichText)
        layout.addWidget(contact_label)

        # Set the layout for the AboutPage widget
        self.setLayout(layout)
