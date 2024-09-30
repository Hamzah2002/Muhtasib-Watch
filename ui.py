# ui.py
from PyQt5.QtWidgets import QWidget, QMainWindow, QPushButton, QLineEdit, QLabel, QTextEdit, QVBoxLayout, QHBoxLayout, \
    QListWidget, QStackedWidget, QFormLayout


class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Muhtasib Watch - Email Security Analyzer")
        self.setGeometry(100, 100, 1200, 700)  # Adjust the main window size

        # Main layout: Horizontal box layout to hold the left navigation and main content area
        main_layout = QHBoxLayout()

        # Create the left navigation bar
        self.navigation_bar = QListWidget()
        self.navigation_bar.setFixedWidth(200)
        self.navigation_bar.addItem("URL Checker")
        self.navigation_bar.addItem("DKIM/SPF Analysis")
        self.navigation_bar.addItem("Attachment Scanning")
        self.navigation_bar.addItem("About")

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
        Create the page for URL Checker functionality with adjusted alignment.
        """
        page = QWidget()
        layout = QVBoxLayout()  # Main vertical layout for the page

        # Use a QFormLayout for better alignment between labels and inputs
        form_layout = QFormLayout()
        self.url_label = QLabel("Enter URL:")
        self.url_input = QLineEdit()
        self.url_input.setFixedWidth(500)

        # Add label and input to the form layout
        form_layout.addRow(self.url_label, self.url_input)

        # Create the button and results area
        self.check_url_button = QPushButton("Check URL")
        self.url_result_area = QTextEdit()
        self.url_result_area.setFixedHeight(300)

        # Add everything to the main layout
        layout.addLayout(form_layout)  # Add the form layout
        layout.addWidget(self.check_url_button)
        layout.addWidget(self.url_result_area)

        page.setLayout(layout)
        return page

    def create_dkim_spf_page(self):
        """
        Create the page for DKIM/SPF Analysis functionality.
        """
        page = QWidget()
        layout = QVBoxLayout()

        self.dkim_label = QLabel("Enter DKIM/SPF Headers:")
        self.dkim_input = QTextEdit()
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
        Create the page for Attachment Scanning functionality.
        """
        page = QWidget()
        layout = QVBoxLayout()

        self.attachment_label = QLabel("Enter Attachment URLs (comma-separated):")
        self.attachment_input = QTextEdit()
        self.scan_attachment_button = QPushButton("Scan Attachments")

        self.attachment_result_area = QTextEdit()
        self.attachment_result_area.setFixedHeight(300)

        layout.addWidget(self.attachment_label)
        layout.addWidget(self.attachment_input)
        layout.addWidget(self.scan_attachment_button)
        layout.addWidget(self.attachment_result_area)

        page.setLayout(layout)
        return page

    def create_about_page(self):
        """
        Create the About page with application information.
        """
        page = QWidget()
        layout = QVBoxLayout()

        about_text = QLabel("Muhtasib Watch\n\nAn Email Security Analyzer Application.\n\nVersion 1.0\n\nCreated by Mouhamad Ismail.")
        layout.addWidget(about_text)

        page.setLayout(layout)
        return page

    def display_page(self, index):
        """
        Display the selected page based on the index.
        """
        self.stacked_widget.setCurrentIndex(index)
