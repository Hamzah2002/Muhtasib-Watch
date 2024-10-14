def apply_stylesheet(window):
    """
    Apply a modern and consistent stylesheet to the entire application.
    """
    window.setStyleSheet("""
        /* Main Window Styling */
        QMainWindow {
            background-color: #1F1F1F;  /* Dark background */
            color: #FFFFFF;  /* Default text color */
            font-family: 'Segoe UI', sans-serif;
        }

        /* Widgets styling */
        QWidget {
            background-color: #1F1F1F;  /* Match background of the main window */
        }

        QLabel {
            font-size: 16px;
            color: #A0A0A0;  /* Light gray for labels */
            padding: 5px;
        }

        QPushButton {
            background-color: #2E2E2E;  /* Button background */
            border: 1px solid #404040;  /* Border for buttons */
            border-radius: 10px;  /* Rounded corners */
            padding: 12px;
            font-size: 14px;
            color: #FFFFFF;
        }
        QPushButton:hover {
            background-color: #3E3E3E;  /* Hover effect for buttons */
        }

        QTextEdit, QLineEdit {
            background-color: #292929;  /* Input fields background */
            border: 1px solid #404040;  /* Input fields border */
            border-radius: 10px;
            color: #FFFFFF;  /* Text color in input fields */
            padding: 8px;
        }

        QListWidget {
            background-color: #2A2A2A;  /* Sidebar background */
            border: 1px solid #404040;  /* Sidebar border */
            color: #FFFFFF;  /* Sidebar text color */
            border-radius: 10px;
        }
        QListWidget::item {
            height: 50px;
            margin: 5px;
            border-radius: 8px;
            padding-left: 10px;
        }
        QListWidget::item:selected {
            background-color: #404040;  /* Selected item background */
            color: #FFFFFF;
        }

        QScrollArea {
            background-color: #1F1F1F;  /* Match background of the main window */
        }

        QVBoxLayout, QHBoxLayout, QStackedWidget {
            background-color: #1F1F1F;  /* Match background of the main window */
        }

        /* Specific to text areas like results and email content input */
        QTextEdit {
            background-color: #292929;
            border: 1px solid #404040;
            border-radius: 10px;
            color: #FFFFFF;
            padding: 8px;
        }
    """)
