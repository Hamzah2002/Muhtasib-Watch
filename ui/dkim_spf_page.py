from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton

class DKIMSPFPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_page()

    def setup_page(self):
        """
        Set up the layout and widgets for the DKIM/SPF Analysis feature.
        """
        # Create the main vertical layout for the DKIM/SPF analysis page
        layout = QVBoxLayout()
        layout.setSpacing(20)  # Set space between widgets

        # Create and configure the input field for DKIM/SPF headers
        self.dkim_label = QLabel("Enter DKIM/SPF Headers:")
        self.dkim_input = QTextEdit()
        self.dkim_input.setFixedHeight(150)
        self.dkim_input.setPlaceholderText("Paste the DKIM/SPF headers here...")

        # Create the 'Check DKIM/SPF' button
        self.check_dkim_button = QPushButton("Check DKIM/SPF")

        # Create the result display area
        self.dkim_result_area = QTextEdit()
        self.dkim_result_area.setFixedHeight(300)
        self.dkim_result_area.setReadOnly(True)  # Make it read-only

        # Add widgets to the layout
        layout.addWidget(self.dkim_label)
        layout.addWidget(self.dkim_input)
        layout.addWidget(self.check_dkim_button)
        layout.addWidget(self.dkim_result_area)

        # Set the layout for the DKIMSPFPage widget
        self.setLayout(layout)
