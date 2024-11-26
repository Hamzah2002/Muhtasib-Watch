from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit

class URLCheckerPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_page()

    def setup_page(self):
        """
        Set up the layout and widgets for the URL Checker feature.
        """
        # Create the main vertical layout for the URL Checker page
        layout = QVBoxLayout()
        layout.setSpacing(20)  # Set space between widgets

        # Create and configure the input field for URLs
        self.url_label = QLabel("Enter the URL link below")
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("e.g., https://example.com")

        # Create the 'Check URLs' button
        self.check_url_button = QPushButton("Check URL")

        # Create the result display area
        self.url_result_area = QTextEdit()
        self.url_result_area.setFixedHeight(300)  # Set a fixed height for the result area
        self.url_result_area.setReadOnly(True)  # Make it read-only

        # Add widgets to the layout
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)
        layout.addWidget(self.check_url_button)
        layout.addWidget(self.url_result_area)

        # Set the layout for the URLCheckerPage widget
        self.setLayout(layout)
