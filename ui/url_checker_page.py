from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
import logging


class URLCheckerPage(QWidget):
    def __init__(self):
        super().__init__()
        logging.info("Initializing URLCheckerPage")  # Log initialization
        self.setup_page()

    def setup_page(self):
        """
        Set up the layout and widgets for the URL Checker feature.
        """
        logging.info("Setting up URLCheckerPage widgets")

        # Create the main vertical layout for the URL Checker page
        layout = QVBoxLayout()
        layout.setSpacing(20)  # Set space between widgets

        # Create and configure the input field for URLs
        self.url_label = QLabel("Enter the URL link below")
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("e.g., https://example.com")

        # Create the 'Check URLs' button
        self.check_url_button = QPushButton("Check URL")

        # Connect the button to the debugging method
        self.check_url_button.clicked.connect(self.debug_button_click)

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

    def debug_button_click(self):
        logging.info("Check URL button clicked")  # Log when the button is clicked
        self.url_result_area.setText("Button clicked! (Debugging Message)")
