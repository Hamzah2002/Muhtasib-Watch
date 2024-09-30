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
        self.navigation_bar.addItem("About")
        self.navigation_bar.setStyleSheet("QListWidget { padding: 10px; }")

        # Create a stacked widget for the main content area
        self.stacked_widget = QStackedWidget()

        # Create individual pages
        self.url_checker_page = self.create_url_checker_page()
        self.dkim_spf_page = self.create_dkim_spf_page()
        self.attachment_scanner_page = self.create_attachment_scanner_page()
        self.about_page = self.create_about_page()

        # Add pages to the stacked widget
        self.stacked_widget.addWidget(self.url_checker_page)
        self.stacked_widget.addWidget(self.dkim_spf_page)
        self.stacked_widget.addWidget(self.attachment_scanner_page)
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
        """
        Create the page for URL Checker functionality with a bold header.
        """
        page = QWidget()
        layout = QVBoxLayout()

        # Create the label with a bold font
        self.url_label = QLabel("Enter URLs (comma-separated):")
        url_label_font = QFont()
        url_label_font.setBold(True)
        url_label_font.setPointSize(11)  # Set a slightly larger font size
        self.url_label.setFont(url_label_font)

        self.url_input = QTextEdit()
        self.url_input.setFixedHeight(150)
        self.url_input.setPlaceholderText("e.g., https://example.com, https://another.com")

        self.check_url_button = QPushButton("Check URLs")
        self.check_url_button.setIcon(QIcon("resources/url_icon.png"))
        self.check_url_button.setFixedWidth(150)
        self.url_result_area = QTextEdit()
        self.url_result_area.setFixedHeight(300)

        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)
        layout.addWidget(self.check_url_button)
        layout.addWidget(self.url_result_area)
        layout.setContentsMargins(50, 20, 50, 20)

        page.setLayout(layout)
        return page

    def create_dkim_spf_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        # Create the label with a bold font
        self.dkim_label = QLabel("Enter DKIM/SPF Headers:")
        dkim_label_font = QFont()
        dkim_label_font.setBold(True)
        dkim_label_font.setPointSize(11)  # Set a slightly larger font size
        self.dkim_label.setFont(dkim_label_font)

        self.dkim_input = QTextEdit()
        self.dkim_input.setFixedHeight(150)
        self.check_dkim_button = QPushButton("Check DKIM/SPF")
        self.check_dkim_button.setIcon(QIcon("resources/headers_icon.png"))
        self.check_dkim_button.setFixedWidth(150)
        self.dkim_result_area = QTextEdit()
        self.dkim_result_area.setFixedHeight(300)

        layout.addWidget(self.dkim_label)
        layout.addWidget(self.dkim_input)
        layout.addWidget(self.check_dkim_button)
        layout.addWidget(self.dkim_result_area)
        layout.setContentsMargins(50, 20, 50, 20)

        page.setLayout(layout)
        return page

    def create_attachment_scanner_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        # Create the label with a bold font
        self.attachment_label = QLabel("Enter Attachment URLs (comma-separated):")
        attachment_label_font = QFont()
        attachment_label_font.setBold(True)
        attachment_label_font.setPointSize(11)  # Set a slightly larger font size
        self.attachment_label.setFont(attachment_label_font)

        self.attachment_input = QTextEdit()
        self.attachment_input.setFixedHeight(150)
        self.attachment_input.setPlaceholderText("e.g., https://example.com/file1, https://another.com/file2")

        self.scan_attachment_button = QPushButton("Scan Attachments")
        self.scan_attachment_button.setIcon(QIcon("resources/scan_icon.png"))
        self.scan_attachment_button.setFixedWidth(150)
        self.attachment_result_area = QTextEdit()
        self.attachment_result_area.setFixedHeight(300)

        layout.addWidget(self.attachment_label)
        layout.addWidget(self.attachment_input)
        layout.addWidget(self.scan_attachment_button)
        layout.addWidget(self.attachment_result_area)
        layout.setContentsMargins(50, 20, 50, 20)

        page.setLayout(layout)
        return page

    def create_about_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        about_text = QLabel("Muhtasib Watch\n\nAn Email Security Analyzer Application.\n\nVersion 1.0\n\nCreated by Mouhamad Ismail.")
        about_text.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(about_text)
        layout.setContentsMargins(50, 50, 50, 50)

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
