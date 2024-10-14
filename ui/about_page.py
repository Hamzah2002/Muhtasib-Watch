from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

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

        # Add logo (centered)
        logo_label = QLabel()
        pixmap = QPixmap("resources/Logo.png")  # Replace with the actual logo file path
        logo_label.setPixmap(pixmap.scaledToWidth(300, Qt.SmoothTransformation))  # Scale the logo to 300px width
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        # Add project title (left-aligned)
        title_label = QLabel("Muhtasib Watch - Email Security Analyzer")
        title_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title_label.setStyleSheet("color: #FFFFFF; padding: 20px;")
        title_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(title_label)

        # Application purpose and features (left-aligned)
        purpose_label = QLabel(
            "Muhtasib Watch is an email security application designed to help users analyze and secure their emails against potential threats.<br><br>"
            "<b>Key Features:</b><br><br>"
            "1. <b>URL Checking:</b> Analyze embedded URLs for potential risks, even when they redirect. Each link is followed and verified.<br><br>"
            "2. <b>DKIM/SPF Analysis:</b> Validate DKIM and SPF headers to ensure email authenticity and prevent spoofing.<br><br>"
            "3. <b>Attachment Sandboxing:</b> Analyze attachments in a secure sandbox environment to detect malicious behavior.<br><br>"
            "4. <b>Attachment Scanning:</b> Scan individual attachments and downloadable items for malware and other threats.<br><br>"
            "5. <b>Machine Learning-Based Phishing Analysis:</b> Uses machine learning models to predict and flag phishing attempts based on email content.<br><br>"
            "6. <b>Gmail Attachment Access (Optional):</b> You can scan attachments in your Gmail account, but the application will only require read access to download and analyze those files.<br><br>"
            "<b>No login is required unless you want to scan attachments in your email.</b>"
        )
        purpose_label.setStyleSheet("color: #A0A0A0; padding: 10px; line-height: 1.5;")
        purpose_label.setWordWrap(True)
        purpose_label.setAlignment(Qt.AlignLeft)
        purpose_label.setTextFormat(Qt.RichText)
        layout.addWidget(purpose_label)

        # Acknowledgment (left-aligned)
        acknowledgment_label = QLabel(
            "This project is part of a Directed Study under the supervision of Dr. Bruce Maxim at the University of Michigan-Dearborn."
        )
        acknowledgment_label.setStyleSheet("color: #A0A0A0; padding: 20px; font-size: 14px;")
        acknowledgment_label.setWordWrap(True)
        acknowledgment_label.setAlignment(Qt.AlignLeft)
        acknowledgment_label.setTextFormat(Qt.RichText)
        layout.addWidget(acknowledgment_label)

        # Contact Information (left-aligned)
        contact_label = QLabel(
            "For any questions or feedback, please feel free to contact the developer:<br>"
            "<b>Mouhamad Hamzah Ismail</b><br>"
            "<a href='mailto:mouhamad.hamzah@gmail.com' style='color:#1E90FF;'>mouhamad.hamzah@gmail.com</a>"
        )
        contact_label.setStyleSheet("color: #A0A0A0; padding: 10px; font-size: 14px;")
        contact_label.setWordWrap(True)
        contact_label.setAlignment(Qt.AlignLeft)
        contact_label.setOpenExternalLinks(True)  # Allow the email link to open in the default email client
        contact_label.setTextFormat(Qt.RichText)
        layout.addWidget(contact_label)

        # Set the layout for the AboutPage widget
        self.setLayout(layout)
