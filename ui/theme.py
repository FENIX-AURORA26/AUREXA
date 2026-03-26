def aplicar_tema(app):
    app.setStyleSheet("""
        QWidget {
            background-color: #07111f;
            color: #f3f4f6;
            font-size: 14px;
        }
        QPushButton {
            background-color: #124e66;
            color: #f8fafc;
            padding: 10px;
            border-radius: 8px;
            border: 1px solid #5fa8d3;
        }
        QPushButton:hover {
            background-color: #1b6f8a;
        }
        QLineEdit, QTextEdit {
            background-color: #0d1b2a;
            border: 1px solid #3b82f6;
            border-radius: 8px;
            padding: 8px;
            color: #f8fafc;
        }
        QLabel {
            color: #e5eef7;
        }
    """)
