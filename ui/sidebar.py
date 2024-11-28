from PyQt5.QtWidgets import QListWidget, QVBoxLayout, QPushButton, QWidget
from PyQt5.QtCore import Qt


class NavigationSidebar(QWidget):
    def __init__(self):
        super().__init__()
        self.is_collapsed = False
        self.setup_sidebar()

    def setup_sidebar(self):
        """
        Sets up the collapsible sidebar navigation with modern styles and animations.
        """
        # Set initial width of the sidebar
        self.setFixedWidth(250)
        self.setStyleSheet("background-color: #F8F9FA; color: #333333; border: none;")

        # Create the main vertical layout
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)

        # Add a toggle button
        self.toggle_button = QPushButton("☰  Menu")
        self.toggle_button.setFixedHeight(50)
        self.toggle_button.setStyleSheet("""
            QPushButton {
                background-color: #E9ECEF;  /* Light gray */
                color: #333333;  /* Dark text */
                font-size: 18px;
                border: none;
                text-align: left;
                padding-left: 20px;
                font-weight: bold;
                transition: background-color 0.3s ease;
            }
            QPushButton:hover {
                background-color: #CED4DA;  /* Slightly darker gray on hover */
            }
        """)
        self.toggle_button.clicked.connect(self.toggle_sidebar)
        layout.addWidget(self.toggle_button)

        # Add the navigation items
        self.nav_items = QListWidget()
        self.nav_items.addItem("🏠  Home")
        self.nav_items.addItem("🔗  URL Checker")
        self.nav_items.addItem("📧  DKIM/SPF Analysis")
        self.nav_items.addItem("📎  Attachment Scanning")
        self.nav_items.addItem("🔍  Phishing Analysis")
        self.nav_items.addItem("ℹ️  About")
        self.nav_items.setStyleSheet("""
            QListWidget {
                border: none;
                background-color: #F8F9FA;  /* Light gray background */
                font-size: 16px;
                color: #333333;  /* Dark text */
                padding: 10px;
            }
            QListWidget::item {
                height: 50px;
                margin: 5px;
                border-radius: 8px;
                padding-left: 20px;
                transition: background-color 0.3s ease, transform 0.2s ease;
            }
            QListWidget::item:hover {
                background-color: #E9ECEF;  /* Subtle highlight on hover */
                transform: scale(1.02);  /* Slight zoom on hover */
            }
            QListWidget::item:selected {
                background-color: #007BFF;  /* Bright blue for selected */
                color: #FFFFFF;  /* White text */
            }
        """)
        layout.addWidget(self.nav_items)

        self.setLayout(layout)

    def toggle_sidebar(self):
        """
        Toggles the sidebar between expanded and collapsed states.
        """
        self.is_collapsed = not self.is_collapsed
        if self.is_collapsed:
            self.setFixedWidth(80)
            self.toggle_button.setText("☰")
            self.nav_items.setStyleSheet("""
                QListWidget {
                    border: none;
                    background-color: #F8F9FA;  /* Match background */
                    font-size: 16px;
                    color: #333333;
                }
                QListWidget::item {
                    height: 50px;
                    margin: 5px;
                    border-radius: 8px;
                    padding-left: 10px;  /* Reduced padding in collapsed view */
                }
                QListWidget::item:hover {
                    background-color: #E9ECEF;
                    transform: scale(1.02);
                }
                QListWidget::item:selected {
                    background-color: #007BFF;
                    color: #FFFFFF;
                }
            """)
        else:
            self.setFixedWidth(250)
            self.toggle_button.setText("☰  Menu")
            self.nav_items.setStyleSheet("""
                QListWidget {
                    border: none;
                    background-color: #F8F9FA;
                    font-size: 16px;
                    color: #333333;
                    padding: 10px;
                }
                QListWidget::item {
                    height: 50px;
                    margin: 5px;
                    border-radius: 8px;
                    padding-left: 20px;
                    transition: background-color 0.3s ease, transform 0.2s ease;
                }
                QListWidget::item:hover {
                    background-color: #E9ECEF;
                    transform: scale(1.02);
                }
                QListWidget::item:selected {
                    background-color: #007BFF;
                    color: #FFFFFF;
                }
            """)
