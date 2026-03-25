def aplicar_tema(app):
    app.setStyleSheet("""
        QWidget {
            background-color: #0f172a;
            color: white;
            font-size: 14px;
        }
        QPushButton {
            background-color: #1e293b;
            padding: 10px;
            border-radius: 8px;
        }
        QPushButton:hover {
            background-color: #334155;
        }
    """)