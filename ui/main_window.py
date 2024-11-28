from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QStackedWidget
from PyQt5.QtCore import Qt
from .sidebar import NavigationSidebar
from .url_checker_page import URLCheckerPage
from .dkim_spf_page import DKIMSPFPage
from .attachment_scanner_page import AttachmentScannerPage
from .phishing_analysis_page import PhishingAnalysisPage
from .about_page import AboutPage
from .home_page import HomePage
from .styles import apply_stylesheet


class Ui_MainWindow(QMainWindow):
    def __init__(self, scanner_backend):
        """
        Initialize the main window.

        :param scanner_backend: The backend instance used for attachment scanning.
        """
        super().__init__()
        self.scanner_backend = scanner_backend  # Store the scanner backend instance
        self.setupUI(scanner_backend)  # Pass the scanner_backend to setupUI

    def setupUI(self, scanner_backend):
        """
        Setup the main UI components, passing the scanner backend to the relevant page.
        """
        self.setWindowTitle("Muhtasib Watch - Email Security Analyzer")
        self.setGeometry(100, 100, 1400, 800)
        self.setWindowIcon(QIcon("resources/Logo.png"))

        # Apply custom stylesheet
        apply_stylesheet(self)

        # Main layout for the window
        main_layout = QHBoxLayout()

        # Create the sidebar navigation
        self.navigation_bar = NavigationSidebar()

        # Create the stacked widget for content pages
        self.stacked_widget = QStackedWidget()

        # Initialize pages
        self.home_page = HomePage()
        self.url_checker_page = URLCheckerPage()
        self.dkim_spf_page = DKIMSPFPage()
        self.attachment_scanner_page = AttachmentScannerPage(scanner_backend=scanner_backend)
        self.phishing_analysis_page = PhishingAnalysisPage()
        self.about_page = AboutPage()

        # Add pages to the stacked widget
        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.url_checker_page)
        self.stacked_widget.addWidget(self.dkim_spf_page)
        self.stacked_widget.addWidget(self.attachment_scanner_page)
        self.stacked_widget.addWidget(self.phishing_analysis_page)
        self.stacked_widget.addWidget(self.about_page)

        # Add the sidebar and stacked widget to the layout
        main_layout.addWidget(self.navigation_bar)
        main_layout.addWidget(self.stacked_widget)

        # Set the central widget of the main window
        container_widget = QWidget()
        container_widget.setLayout(main_layout)
        self.setCentralWidget(container_widget)

        # Connect the sidebar's navigation signal
        self.navigation_bar.nav_items.currentRowChanged.connect(self.display_page)

    def display_page(self, index):
        """
        Switches to the selected page based on the sidebar's current row.
        """
        self.stacked_widget.setCurrentIndex(index)

