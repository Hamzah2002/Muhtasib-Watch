from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QHBoxLayout, QProgressBar
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer


class PhishingAnalysisPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_page()

    def setup_page(self):
        """
        Set up the layout and widgets for the Phishing Analysis feature.
        """
        # Create the main vertical layout for the Phishing Analysis page
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Title Section
        title_label = QLabel("🔍 Phishing Analysis")
        title_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title_label.setStyleSheet("color: #007BFF; margin-bottom: 10px;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Subtitle Section
        subtitle_label = QLabel(
            "Paste the email content below to analyze for potential phishing attempts. "
            "Our system will use advanced analysis to detect suspicious elements."
        )
        subtitle_label.setFont(QFont("Segoe UI", 14))
        subtitle_label.setStyleSheet("color: #495057; margin-bottom: 20px; line-height: 1.6;")
        subtitle_label.setWordWrap(True)
        subtitle_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(subtitle_label)

        # Input Section Header
        input_section_label = QLabel("📧 Enter Email Content:")
        input_section_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        input_section_label.setStyleSheet("color: #333333; margin-bottom: 10px;")
        main_layout.addWidget(input_section_label)

        # Email Input Text Area
        self.email_input = QTextEdit()
        self.email_input.setFixedHeight(200)
        self.email_input.setPlaceholderText("Paste the email content here for analysis...")
        self.email_input.setStyleSheet("""
            QTextEdit {
                background-color: #F8F9FA;
                border: 2px solid #CED4DA;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                color: #495057;
            }
            QTextEdit:focus {
                border: 2px solid #007BFF;
            }
        """)
        main_layout.addWidget(self.email_input)

        # Button Section (Analyze Email + Clear Input)
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)

        # Analyze Button
        self.check_phishing_button = QPushButton("🔍 Analyze Email")
        self.check_phishing_button.setFixedHeight(50)
        self.check_phishing_button.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;
                color: white;
                font-size: 16px;
                font-weight: bold;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #0056B3;
            }
            QPushButton:pressed {
                background-color: #004085;
            }
        """)
        self.check_phishing_button.clicked.connect(self.start_analysis)
        button_layout.addWidget(self.check_phishing_button)

        # Clear Input Button
        self.clear_input_button = QPushButton("🗑️ Clear Input")
        self.clear_input_button.setFixedHeight(50)
        self.clear_input_button.setStyleSheet("""
            QPushButton {
                background-color: #DC3545;  /* Red background */
                color: white;
                font-size: 16px;
                font-weight: bold;
                border: none;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #C82333;
            }
            QPushButton:pressed {
                background-color: #BD2130;
            }
        """)
        self.clear_input_button.clicked.connect(self.clear_input_field)
        button_layout.addWidget(self.clear_input_button)

        # Add buttons to the layout
        main_layout.addLayout(button_layout)

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #CED4DA;
                border-radius: 8px;
                background-color: #F8F9FA;
                height: 30px;
            }
            QProgressBar::chunk {
                background-color: #007BFF;
                border-radius: 8px;
            }
            QProgressBar[textVisible="true"] {
                text-align: center;  /* Center the percentage text */
                font-size: 16px;     /* Larger text */
                font-weight: bold;   /* Bold text */
                color: #333333;      /* Text color */
            }
        """)
        self.progress_bar.setValue(0)
        main_layout.addWidget(self.progress_bar)

        # Divider Line
        divider = QLabel("")
        divider.setStyleSheet("background-color: #CED4DA; height: 1px;")
        divider.setFixedHeight(1)
        main_layout.addWidget(divider)

        # Result Section Header
        result_section_label = QLabel("📝 Analysis Results:")
        result_section_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        result_section_label.setStyleSheet("color: #333333; margin-top: 20px;")
        main_layout.addWidget(result_section_label)

        # Results Display Area
        self.phishing_result_area = QTextEdit()
        self.phishing_result_area.setFixedHeight(300)
        self.phishing_result_area.setReadOnly(True)
        self.phishing_result_area.setPlaceholderText("Analysis results will appear here...")
        self.phishing_result_area.setStyleSheet("""
            QTextEdit {
                background-color: #F8F9FA;
                border: 2px solid #CED4DA;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                color: #495057;
            }
        """)
        main_layout.addWidget(self.phishing_result_area)

        # Set the layout for the PhishingAnalysisPage widget
        self.setLayout(main_layout)

    def start_analysis(self):
        """
        Starts the phishing analysis process and updates the progress bar.
        """
        self.progress_bar.setValue(0)
        self.phishing_result_area.clear()
        self.current_progress = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(100)  # Update every 100ms

    def update_progress(self):
        """
        Updates the progress bar value.
        """
        if self.current_progress < 100:
            self.current_progress += 5
            self.progress_bar.setValue(self.current_progress)
        else:
            self.timer.stop()
            self.phishing_result_area.append("Analysis completed successfully!")

    def clear_input_field(self):
        """
        Clears the email input field when the Clear Input button is clicked.
        """
        self.email_input.clear()
