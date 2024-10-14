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
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Muhtasib Watch - Email Security Analyzer")
        self.setGeometry(100, 100, 1400, 800)
        # self.setWindowIcon(QIcon("resources/security_icon.png"))  # Commented out if no icon provided

        apply_stylesheet(self)

        main_layout = QHBoxLayout()

        # Create the sidebar navigation
        self.navigation_bar = NavigationSidebar()

        # Create the stacked widget for content pages
        self.stacked_widget = QStackedWidget()

        # Add pages
        self.home_page = HomePage()
        self.url_checker_page = URLCheckerPage()
        self.dkim_spf_page = DKIMSPFPage()
        self.attachment_scanner_page = AttachmentScannerPage()
        self.phishing_analysis_page = PhishingAnalysisPage()
        self.about_page = AboutPage()

        # Add to stacked widget
        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.url_checker_page)
        self.stacked_widget.addWidget(self.dkim_spf_page)
        self.stacked_widget.addWidget(self.attachment_scanner_page)
        self.stacked_widget.addWidget(self.phishing_analysis_page)
        self.stacked_widget.addWidget(self.about_page)

        main_layout.addWidget(self.navigation_bar)
        main_layout.addWidget(self.stacked_widget)

        container_widget = QWidget()
        container_widget.setLayout(main_layout)
        self.setCentralWidget(container_widget)

        # Connect sidebar navigation
        self.navigation_bar.currentRowChanged.connect(self.display_page)

    def display_page(self, index):
        self.stacked_widget.setCurrentIndex(index)
