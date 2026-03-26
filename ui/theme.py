def aplicar_tema(app):
    app.setStyleSheet(
        """
        QWidget {
            background-color: #040912;
            color: #f3f4f6;
            font-size: 16px;
            font-family: 'Segoe UI', 'Inter', sans-serif;
        }
        QPushButton {
            background-color: qlineargradient(
                x1: 0, y1: 0, x2: 1, y2: 1,
                stop: 0 #0f766e,
                stop: 1 #1d4ed8
            );
            color: #f8fafc;
            padding: 14px;
            border-radius: 12px;
            border: 1px solid #67e8f9;
            font-weight: 700;
            min-height: 44px;
        }
        QPushButton:hover {
            background-color: #1b6f8a;
        }
        QLineEdit, QTextEdit {
            background-color: #0d1b2a;
            border: 1px solid #3b82f6;
            border-radius: 10px;
            padding: 12px;
            color: #f8fafc;
            min-height: 40px;
        }
        QLabel {
            color: #e5eef7;
            font-size: 15px;
        }
        """
    )
