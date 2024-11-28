def apply_stylesheet(window):
    """
    Apply a bright, modern, and visually appealing stylesheet to the entire application.
    """
    window.setStyleSheet("""
        /* General Window Styling */
        QMainWindow {
            background-color: #FFFFFF;  /* Pure white background */
            color: #333333;  /* Dark gray text */
            font-family: 'Segoe UI', sans-serif;  /* Modern font */
            border: none;
        }

        QWidget {
            background-color: #FFFFFF;  /* Match background of the main window */
        }

        /* Label Styling */
        QLabel {
            font-size: 16px;
            color: #333333;  /* Dark gray for text */
            padding: 5px;
        }
        QLabel[title="true"] {
            font-size: 22px;
            font-weight: bold;
            color: #007BFF;  /* Vibrant blue for titles */
        }

        /* Button Styling */
        QPushButton {
            background-color: #007BFF;  /* Primary button color (blue) */
            color: #FFFFFF;  /* White text */
            border: none;
            border-radius: 8px;  /* Rounded corners */
            padding: 12px 20px;
            font-size: 14px;
            font-weight: bold;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            transition: background-color 0.3s ease, transform 0.2s ease;
        }
        QPushButton:hover {
            background-color: #0056B3;  /* Darker blue on hover */
            transform: scale(1.02);  /* Slight zoom effect */
        }
        QPushButton:pressed {
            background-color: #004085;  /* Even darker on press */
            transform: scale(0.98);  /* Slight shrink effect */
        }

        /* Input Fields */
        QTextEdit, QLineEdit {
            background-color: #F8F9FA;  /* Light gray background */
            border: 1px solid #CED4DA;  /* Subtle border */
            border-radius: 8px;
            color: #333333;  /* Dark gray text */
            padding: 10px;
            font-size: 14px;
        }
        QTextEdit:focus, QLineEdit:focus {
            border: 1px solid #007BFF;  /* Highlight border on focus */
            background-color: #FFFFFF;  /* Pure white on focus */
            outline: none;
        }

        /* Sidebar Styling */
        QListWidget {
            background-color: #F8F9FA;  /* Light gray sidebar */
            border: none;
            color: #333333;
            border-radius: 10px;
            padding: 5px;
        }
        QListWidget::item {
            height: 50px;
            margin: 5px;
            border-radius: 8px;
            padding-left: 15px;
            font-size: 16px;
            transition: background-color 0.3s ease, transform 0.2s ease;
        }
        QListWidget::item:hover {
            background-color: #E9ECEF;  /* Subtle highlight on hover */
        }
        QListWidget::item:selected {
            background-color: #007BFF;  /* Bright blue for selected item */
            color: #FFFFFF;  /* White text for selected item */
        }

        /* Result Display Area */
        QTextEdit[readOnly="true"] {
            background-color: #F8F9FA;  /* Light gray background */
            border: 1px solid #CED4DA;  /* Subtle border */
            border-radius: 8px;
            color: #495057;  /* Medium gray for text */
            padding: 10px;
        }

        /* Scroll Area */
        QScrollArea {
            background-color: #FFFFFF;  /* Match main window */
            border: none;
        }

        /* Tooltip Styling */
        QToolTip {
            background-color: #007BFF;  /* Tooltip background */
            color: #FFFFFF;  /* Tooltip text */
            border: none;
            padding: 5px;
            border-radius: 4px;
            font-size: 12px;
        }

        /* General Layouts */
        QVBoxLayout, QHBoxLayout {
            background-color: #FFFFFF;  /* Match main window */
        }

        /* Specific Highlight Effects */
        QTextEdit:disabled, QLineEdit:disabled {
            background-color: #E9ECEF;  /* Disabled fields appear gray */
            color: #ADB5BD;  /* Subtle gray for disabled text */
        }
    """)
