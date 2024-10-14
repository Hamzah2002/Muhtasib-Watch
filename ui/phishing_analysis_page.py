from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton

class PhishingAnalysisPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_page()

    def setup_page(self):
        """
        Set up the layout and widgets for the Phishing Analysis feature.
        """
        # Create the main vertical layout for the Phishing Analysis page
        layout = QVBoxLayout()
        layout.setSpacing(20)  # Set space between widgets

        # Create and configure the input field for email content
        self.phishing_label = QLabel("Enter Email Content for Phishing Analysis:")
        self.email_input = QTextEdit()
        self.email_input.setFixedHeight(200)
        self.email_input.setPlaceholderText("Paste the email content here for analysis...")

        # Create the 'Analyze Email' button
        self.check_phishing_button = QPushButton("Analyze Email")

        # Create the result display area
        self.phishing_result_area = QTextEdit()
        self.phishing_result_area.setFixedHeight(300)
        self.phishing_result_area.setReadOnly(True)  # Make it read-only

        # Add widgets to the layout
        layout.addWidget(self.phishing_label)
        layout.addWidget(self.email_input)
        layout.addWidget(self.check_phishing_button)
        layout.addWidget(self.phishing_result_area)

        # Set the layout for the PhishingAnalysisPage widget
        self.setLayout(layout)
