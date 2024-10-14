from PyQt5.QtWidgets import QListWidget


class NavigationSidebar(QListWidget):
    def __init__(self):
        super().__init__()
        self.setup_sidebar()

    def setup_sidebar(self):
        """
        Sets up the sidebar navigation with various features and applies custom styles.
        """
        # Set the width of the sidebar
        self.setFixedWidth(250)

        # Add navigation items for each feature
        self.addItem("🏠  Home")
        self.addItem("🔗  URL Checker")
        self.addItem("📧  DKIM/SPF Analysis")
        self.addItem("📎  Attachment Scanning")
        self.addItem("🔍  Phishing Analysis")
        self.addItem("ℹ️  About")

        # Apply specific styles for the sidebar items
        self.setStyleSheet("""
            QListWidget {
                padding: 20px;
                font-size: 16px;
                color: #FFFFFF;
                background-color: #2A2A2A;
            }
            QListWidget::item {
                height: 50px;
                margin: 5px;
                border-radius: 8px;
                padding-left: 10px;
            }
            QListWidget::item:selected {
                background-color: #404040;
                color: #FFFFFF;
            }
        """)
