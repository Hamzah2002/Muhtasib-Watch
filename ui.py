from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QLineEdit, QTextEdit, QHBoxLayout,
    QListWidget, QStackedWidget, QApplication
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QScrollArea, QVBoxLayout, QWidget

class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        # Set the main window title and dimensions
        self.setWindowTitle("Muhtasib Watch - Email Security Analyzer")
        self.setGeometry(100, 100, 1400, 800)
        self.setWindowIcon(QIcon("resources/security_icon.png"))

        # Set application-wide styles for consistency and visual appeal
        self.apply_stylesheet()

        # Create the main layout with a horizontal split for sidebar and main content
        main_layout = QHBoxLayout()

        # Create the sidebar navigation panel
        self.create_sidebar_navigation()

        # Create the stacked widget for content pages
        self.create_stacked_widget()

        # Add navigation bar and content area to the main layout
        main_layout.addWidget(self.navigation_bar)
        main_layout.addWidget(self.stacked_widget)

        # Set the main layout to the central widget
        container_widget = QWidget()
        container_widget.setLayout(main_layout)
        self.setCentralWidget(container_widget)

        # Connect sidebar navigation to display corresponding pages
        self.navigation_bar.currentRowChanged.connect(self.display_page)

    def apply_stylesheet(self):
        """
        Apply a modern and consistent stylesheet to the entire application.
        """
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1F1F1F;
                color: #FFFFFF;
                font-family: 'Segoe UI', sans-serif;
            }
            QWidget {
                background-color: #1F1F1F;
            }
            QLabel {
                font-size: 16px;
                color: #A0A0A0;
            }
            QPushButton {
                background-color: #2E2E2E;
                border: 1px solid #404040;
                border-radius: 10px;
                padding: 12px;
                font-size: 14px;
                color: #FFFFFF;
            }
            QPushButton:hover {
                background-color: #3E3E3E;
            }
            QTextEdit, QLineEdit {
                background-color: #292929;
                border: 1px solid #404040;
                border-radius: 10px;
                color: #FFFFFF;
                padding: 8px;
            }
            QListWidget {
                background-color: #2A2A2A;
                border: 1px solid #404040;
                color: #FFFFFF;
                border-radius: 10px;
            }
            QListWidget::item:selected {
                background-color: #404040;
                color: #FFFFFF;
            }
            QScrollArea {
                background-color: #1F1F1F;  /* Match background of the main window */
            }
            QVBoxLayout, QHBoxLayout, QStackedWidget {
                background-color: #1F1F1F;  /* Match background of the main window */
            }
        """)

    def create_sidebar_navigation(self):
        """
        Create the sidebar navigation menu with items for each feature.
        """
        self.navigation_bar = QListWidget()
        self.navigation_bar.setFixedWidth(250)
        self.navigation_bar.addItem("🏠  Home")
        self.navigation_bar.addItem("🔗  URL Checker")
        self.navigation_bar.addItem("📧  DKIM/SPF Analysis")
        self.navigation_bar.addItem("📎  Attachment Scanning")
        self.navigation_bar.addItem("🔍  Phishing Analysis")
        self.navigation_bar.addItem("ℹ️  About")

        # Apply specific styles for the sidebar items
        self.navigation_bar.setStyleSheet("""
            QListWidget {
                padding: 20px;
                font-size: 16px;
            }
            QListWidget::item {
                height: 50px;
                margin: 5px;
                border-radius: 8px;
                padding-left: 10px;
            }
            QListWidget::item:selected {
                background-color: #404040;
            }
        """)

    def create_stacked_widget(self):
        """
        Create the stacked widget and add individual pages for each feature.
        """
        self.stacked_widget = QStackedWidget()

        # Create and add pages for each feature
        self.home_page = self.create_home_page()
        self.url_checker_page = self.create_url_checker_page()
        self.dkim_spf_page = self.create_dkim_spf_page()
        self.attachment_scanner_page = self.create_attachment_scanner_page()
        self.phishing_analysis_page = self.create_phishing_analysis_page()
        self.about_page = self.create_about_page()

        # Add pages to the stacked widget
        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.url_checker_page)
        self.stacked_widget.addWidget(self.dkim_spf_page)
        self.stacked_widget.addWidget(self.attachment_scanner_page)
        self.stacked_widget.addWidget(self.phishing_analysis_page)
        self.stacked_widget.addWidget(self.about_page)

    # Create the individual feature pages
    from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget
    from PyQt5.QtGui import QPixmap, QFont
    from PyQt5.QtCore import Qt

    def create_about_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        # Add Logo (keep it centered)
        logo_label = QLabel()
        pixmap = QPixmap("Logo.png")
        logo_label.setPixmap(pixmap.scaledToWidth(300, Qt.SmoothTransformation))  # Keep logo at 300px width
        logo_label.setAlignment(Qt.AlignCenter)  # Center the logo
        layout.addWidget(logo_label)

        # Add Project Title (left-aligned)
        title_label = QLabel("Muhtasib Watch - Email Security Analyzer")
        title_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title_label.setStyleSheet("color: #FFFFFF; padding: 20px;")
        title_label.setAlignment(Qt.AlignLeft)  # Align text to the left
        layout.addWidget(title_label)

        # Application Purpose and Features (left-aligned)
        purpose_label = QLabel(
            "Muhtasib Watch is an email security application designed to help users analyze and secure their emails against potential threats.<br><br>"
            "<b>Key Features:</b><br>"
            "1. <b>URL Checking:</b> Analyze embedded URLs for potential risks, even when they redirect. Each link is followed and verified.<br>"
            "2. <b>DKIM/SPF Analysis:</b> Validate DKIM and SPF headers to ensure email authenticity and prevent spoofing.<br>"
            "3. <b>Attachment Sandboxing:</b> Analyze attachments in a secure sandbox environment to detect malicious behavior.<br>"
            "4. <b>Attachment Scanning:</b> Scan individual attachments and downloadable items for malware and other threats.<br>"
            "5. <b>Machine Learning-Based Phishing Analysis:</b> Uses machine learning models to predict and flag phishing attempts based on email content.<br>"
            "6. <b>Gmail Attachment Access (Optional):</b> You can scan attachments in your Gmail account, but the application will only require read access to download and analyze those files.<br><br>"
            "<b>No login is required unless you want to scan attachments in your email.</b>"
        )
        purpose_label.setStyleSheet("color: #A0A0A0; padding: 10px;")
        purpose_label.setWordWrap(True)
        purpose_label.setAlignment(Qt.AlignLeft)  # Align text to the left
        purpose_label.setTextFormat(Qt.RichText)  # Set text format to RichText
        layout.addWidget(purpose_label)

        # Acknowledgment (left-aligned)
        acknowledgment_label = QLabel(
            "This project is part of a Directed Study under the supervision of Dr. Bruce Maxim at the University of Michigan-Dearborn."
        )
        acknowledgment_label.setStyleSheet("color: #A0A0A0; padding: 20px; font-size: 14px;")
        acknowledgment_label.setWordWrap(True)
        acknowledgment_label.setAlignment(Qt.AlignLeft)  # Align text to the left
        acknowledgment_label.setTextFormat(Qt.RichText)  # Set text format to RichText
        layout.addWidget(acknowledgment_label)

        # Contact Information (left-aligned)
        contact_label = QLabel(
            "For any questions or feedback, please feel free to contact the developer:<br>"
            "<b>Mouhamad Hamzah Ismail</b><br>"
            "<a href='mailto:mouhamad.hamzah@gmail.com' style='color:#1E90FF;'>mouhamad.hamzah@gmail.com</a>"
        )
        contact_label.setStyleSheet("color: #A0A0A0; padding: 10px; font-size: 14px;")
        contact_label.setWordWrap(True)
        contact_label.setAlignment(Qt.AlignLeft)  # Align text to the left
        contact_label.setOpenExternalLinks(True)  # Enable clickable links
        contact_label.setTextFormat(Qt.RichText)  # Set text format to RichText
        layout.addWidget(contact_label)

        page.setLayout(layout)
        return page

    def create_url_checker_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)

        self.url_label = QLabel("Enter URLs (comma-separated):")
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("e.g., https://example.com, https://another.com")
        self.check_url_button = QPushButton("Check URLs")
        self.url_result_area = QTextEdit()
        self.url_result_area.setFixedHeight(300)

        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)
        layout.addWidget(self.check_url_button)
        layout.addWidget(self.url_result_area)
        page.setLayout(layout)
        return page

    def create_dkim_spf_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)

        self.dkim_label = QLabel("Enter DKIM/SPF Headers:")
        self.dkim_input = QTextEdit()
        self.dkim_input.setFixedHeight(150)
        self.check_dkim_button = QPushButton("Check DKIM/SPF")
        self.dkim_result_area = QTextEdit()
        self.dkim_result_area.setFixedHeight(300)

        layout.addWidget(self.dkim_label)
        layout.addWidget(self.dkim_input)
        layout.addWidget(self.check_dkim_button)
        layout.addWidget(self.dkim_result_area)
        page.setLayout(layout)
        return page

    def create_attachment_scanner_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)

        self.attachment_label = QLabel("Enter Attachment URLs (comma-separated):")
        self.attachment_input = QTextEdit()
        self.attachment_input.setFixedHeight(150)
        self.attachment_input.setPlaceholderText("e.g., https://example.com/file1, https://another.com/file2")
        self.scan_attachment_button = QPushButton("Scan Attachments")
        self.download_gmail_button = QPushButton("Download Gmail Attachments")  # New button added
        self.attachment_result_area = QTextEdit()
        self.attachment_result_area.setFixedHeight(300)

        layout.addWidget(self.attachment_label)
        layout.addWidget(self.attachment_input)
        layout.addWidget(self.scan_attachment_button)
        layout.addWidget(self.download_gmail_button)  # Added the new button here
        layout.addWidget(self.attachment_result_area)
        page.setLayout(layout)
        return page

    def create_phishing_analysis_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)

        self.phishing_label = QLabel("Enter Email Content for Phishing Analysis:")
        self.email_input = QTextEdit()
        self.email_input.setFixedHeight(200)
        self.check_phishing_button = QPushButton("Analyze Email")
        self.phishing_result_area = QTextEdit()
        self.phishing_result_area.setFixedHeight(300)

        layout.addWidget(self.phishing_label)
        layout.addWidget(self.email_input)
        layout.addWidget(self.check_phishing_button)
        layout.addWidget(self.phishing_result_area)
        page.setLayout(layout)
        return page

    from PyQt5.QtWidgets import QLabel, QScrollArea, QVBoxLayout, QWidget
    from PyQt5.QtGui import QPixmap, QFont
    from PyQt5.QtCore import Qt

    def create_home_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        # Add a welcome label
        welcome_text = QLabel("Welcome to Muhtasib Watch\n\nSelect a feature from the sidebar to begin.\n\n"
                              "Below is a quick guide on how to use each feature effectively.")
        welcome_text.setFont(QFont("Segoe UI", 18, QFont.Bold))
        welcome_text.setStyleSheet("color: #FFFFFF; padding: 20px;")
        welcome_text.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome_text)

        # Add a scroll area to contain the manual
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
            QPixmap("manuals/url_checker_example.png").scaledToWidth(600, Qt.SmoothTransformation))
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
        dkim_spf_image.setPixmap(QPixmap("manuals/dkim_spf_example.png").scaledToWidth(600, Qt.SmoothTransformation))
        dkim_spf_image.setAlignment(Qt.AlignCenter)
        scroll_area_layout.addWidget(dkim_spf_image)

        ### Attachment Scanning Section ###
        # Attachment Scanning Section
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
            QPixmap("manuals/phishing_analysis_example.png").scaledToWidth(600, Qt.SmoothTransformation))
        phishing_image.setAlignment(Qt.AlignCenter)
        scroll_area_layout.addWidget(phishing_image)

        ### Adding the Scroll Area ###
        scroll_area_widget.setLayout(scroll_area_layout)
        scroll_area.setWidget(scroll_area_widget)
        scroll_area.setWidgetResizable(True)

        layout.addWidget(scroll_area)
        page.setLayout(layout)

        return page

    def display_page(self, index):
        """
        Display the page corresponding to the selected index.
        """
        self.stacked_widget.setCurrentIndex(index)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec_())
