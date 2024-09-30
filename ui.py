from PyQt5.QtWidgets import QWidget, QMainWindow, QPushButton, QLineEdit, QLabel, QTextEdit, QVBoxLayout, QHBoxLayout, \
    QListWidget, QStackedWidget, QFormLayout, QApplication
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt


class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Muhtasib Watch - Email Security Analyzer")
        self.setGeometry(100, 100, 1200, 700)
        self.setWindowIcon(QIcon("resources/security_icon.png"))  # Set an icon for the application

        # Apply a stylesheet for custom styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2C2F33;
                color: #FFFFFF;
                font-family: Arial;
                font-size: 14px;
            }
            QLabel {
                color: #FFFFFF;
            }
            QPushButton {
                background-color: #7289DA;
                border: 1px solid #99AAB5;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #99AAB5;
            }
            QTextEdit, QLineEdit {
                background-color: #23272A;
                border: 1px solid #7289DA;
                color: #FFFFFF;
                border-radius: 5px;
            }
            QListWidget {
                background-color: #23272A;
                border: 1px solid #7289DA;
                color: #FFFFFF;
                font-weight: bold;
            }
            QListWidget::item:selected {
                background-color: #7289DA;
                color: #FFFFFF;
            }
        """)

        # Main layout: Horizontal box layout to hold the left navigation and main content area
        main_layout = QHBoxLayout()

        # Create the left navigation bar with a custom style
        self.navigation_bar = QListWidget()
        self.navigation_bar.setFixedWidth(220)
        self.navigation_bar.addItem("URL Checker")
        self.navigation_bar.addItem("DKIM/SPF Analysis")
        self.navigation_bar.addItem("Attachment Scanning")
        self.navigation_bar.addItem("Phishing Analysis")  # New item for phishing analysis
        self.navigation_bar.addItem("About")
        self.navigation_bar.setStyleSheet("QListWidget { padding: 10px; }")

        # Create a stacked widget for the main content area
        self.stacked_widget = QStackedWidget()

        # Create individual pages
        self.url_checker_page = self.create_url_checker_page()
        self.dkim_spf_page = self.create_dkim_spf_page()
        self.attachment_scanner_page = self.create_attachment_scanner_page()
        self.phishing_analysis_page = self.create_phishing_analysis_page()  # New page for phishing analysis
        self.about_page = self.create_about_page()

        # Add pages to the stacked widget
        self.stacked_widget.addWidget(self.url_checker_page)
        self.stacked_widget.addWidget(self.dkim_spf_page)
        self.stacked_widget.addWidget(self.attachment_scanner_page)
        self.stacked_widget.addWidget(self.phishing_analysis_page)  # Add new phishing analysis page
        self.stacked_widget.addWidget(self.about_page)

        # Add navigation and stacked widget to the main layout
        main_layout.addWidget(self.navigation_bar)
        main_layout.addWidget(self.stacked_widget)

        # Create a container widget and set the main layout
        container_widget = QWidget()
        container_widget.setLayout(main_layout)
        self.setCentralWidget(container_widget)

        # Connect the navigation bar to display the selected page
        self.navigation_bar.currentRowChanged.connect(self.display_page)

    def create_url_checker_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        self.url_label = QLabel("Enter URLs (comma-separated):")
        self.url_label.setFont(QFont("Arial", 11, QFont.Bold))
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
        self.dkim_label = QLabel("Enter DKIM/SPF Headers:")
        self.dkim_label.setFont(QFont("Arial", 11, QFont.Bold))
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
        """
        Create the Attachment Scanning page.
        """
        page = QWidget()
        layout = QVBoxLayout()
        self.attachment_label = QLabel("Enter Attachment URLs (comma-separated):")
        self.attachment_label.setFont(QFont("Arial", 11, QFont.Bold))
        self.attachment_input = QTextEdit()
        self.attachment_input.setFixedHeight(150)
        self.attachment_input.setPlaceholderText("e.g., https://example.com/file1, https://another.com/file2")
        self.scan_attachment_button = QPushButton("Scan Attachments")

        # **New Gmail Attachment Button**
        self.download_gmail_button = QPushButton("Download Gmail Attachments")  # New button for Gmail attachments

        self.attachment_result_area = QTextEdit()
        self.attachment_result_area.setFixedHeight(300)
        layout.addWidget(self.attachment_label)
        layout.addWidget(self.attachment_input)
        layout.addWidget(self.scan_attachment_button)
        layout.addWidget(self.download_gmail_button)  # Add the new Gmail button to the layout
        layout.addWidget(self.attachment_result_area)
        page.setLayout(layout)
        return page

    def create_phishing_analysis_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        self.phishing_label = QLabel("Enter Email Content for Phishing Analysis:")
        self.phishing_label.setFont(QFont("Arial", 11, QFont.Bold))
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

    def create_about_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        about_text = QLabel(
            "Muhtasib Watch\n\nAn Email Security Analyzer Application.\n\nVersion 1.0\n\nCreated by Mouhamad Ismail.")
        about_text.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(about_text)
        page.setLayout(layout)
        return page

    def display_page(self, index):
        self.stacked_widget.setCurrentIndex(index)


# Run the application
if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec_())
