from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QProgressBar, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont


class URLCheckerPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_page()

    def setup_page(self):
        """
        Set up the layout and widgets for the URL Checker feature.
        """
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Title Section
        title_label = QLabel("🔗 URL Checker")
        title_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title_label.setStyleSheet("color: #007BFF; margin-bottom: 10px;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # Subtitle Section
        subtitle_label = QLabel(
            "Enter a URL below to check for potential security issues. "
            "Our system will analyze and validate the URL."
        )
        subtitle_label.setFont(QFont("Segoe UI", 14))
        subtitle_label.setStyleSheet("color: #495057; margin-bottom: 20px; line-height: 1.6;")
        subtitle_label.setWordWrap(True)
        subtitle_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(subtitle_label)

        # Input Section Header
        input_section_label = QLabel("🔗 Enter the URL:")
        input_section_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        input_section_label.setStyleSheet("color: #333333; margin-bottom: 10px;")
        main_layout.addWidget(input_section_label)

        # URL Input Field
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("e.g., https://example.com")
        self.url_input.setStyleSheet("""
            QLineEdit {
                background-color: #F8F9FA;
                border: 2px solid #CED4DA;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                color: #495057;
            }
            QLineEdit:focus {
                border: 2px solid #007BFF;
            }
        """)
        main_layout.addWidget(self.url_input)

        # Button Section
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        # Check URL Button
        self.check_url_button = QPushButton("🔍 Check URL")
        self.check_url_button.setFixedHeight(50)
        self.check_url_button.setStyleSheet("""
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
        self.check_url_button.clicked.connect(self.start_analysis)  # Connect to progress simulation
        button_layout.addWidget(self.check_url_button)

        # Clear Button
        self.clear_button = QPushButton("🗑️ Clear Input")
        self.clear_button.setFixedHeight(50)
        self.clear_button.setStyleSheet("""
            QPushButton {
                background-color: #DC3545;
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
                background-color: #A71D2A;
            }
        """)
        self.clear_button.clicked.connect(self.clear_input)
        button_layout.addWidget(self.clear_button)

        main_layout.addLayout(button_layout)

        # Progress Bar Section
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
        self.progress_bar.setValue(0)  # Initialize progress to 0
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
        self.url_result_area = QTextEdit()
        self.url_result_area.setFixedHeight(300)
        self.url_result_area.setReadOnly(True)
        self.url_result_area.setPlaceholderText("Analysis results will appear here...")
        self.url_result_area.setStyleSheet("""
            QTextEdit {
                background-color: #F8F9FA;
                border: 2px solid #CED4DA;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                color: #495057;
            }
        """)
        main_layout.addWidget(self.url_result_area)

        # Set the layout for the URLCheckerPage widget
        self.setLayout(main_layout)

    def start_analysis(self):
        """
        Starts the URL analysis process and updates the progress bar.
        """
        self.url_result_area.clear()
        self.progress_bar.setValue(0)
        self.current_progress = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(100)  # Update every 100ms

    def update_progress(self):
        """
        Updates the progress bar until it reaches 100%.
        """
        if self.current_progress < 100:
            self.current_progress += 5
            self.progress_bar.setValue(self.current_progress)
        else:
            self.timer.stop()
            self.url_result_area.append("URL analysis completed successfully!")

    def clear_input(self):
        """
        Clears the input field and resets the results.
        """
        self.url_input.clear()
        self.url_result_area.clear()
        self.progress_bar.setValue(0)
