from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QLineEdit, QLabel, QTextEdit, QVBoxLayout, QHBoxLayout,
    QListWidget, QWidget, QStackedWidget, QApplication
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt

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
    def create_home_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        welcome_text = QLabel("Welcome to Muhtasib Watch\n\nSelect a feature from the sidebar to begin.")
        welcome_text.setFont(QFont("Segoe UI", 18, QFont.Bold))
        welcome_text.setStyleSheet("color: #FFFFFF; padding: 50px;")
        layout.addWidget(welcome_text)
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
        self.attachment_result_area = QTextEdit()
        self.attachment_result_area.setFixedHeight(300)

        layout.addWidget(self.attachment_label)
        layout.addWidget(self.attachment_input)
        layout.addWidget(self.scan_attachment_button)
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

    def create_about_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        about_text = QLabel("Muhtasib Watch\n\nAn Email Security Analyzer Application.\n\nVersion 1.0")
        about_text.setFont(QFont("Segoe UI", 16, QFont.Bold))
        layout.addWidget(about_text)

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
