from pickle import APPEND


def apply_theme(app):
    app.setStyleSheet("""
QWidget {
background-color: #0f172a;
color: #e2e8f0;
font-family: Segoe UI;
font-size: 14px;
}

```
QLineEdit {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 8px;
    color: #e2e8f0;
}

QLineEdit:focus {
    border: 1px solid #38bdf8;
}

QPushButton {
    background-color: #2563eb;
    border: none;
    border-radius: 10px;
    padding: 10px;
    color: white;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #1d4ed8;
}

QPushButton:pressed {
    background-color: #1e40af;
}

QLabel {
    color: #cbd5f5;
}

QFrame {
    background-color: #1e293b;
    border-radius: 12px;
}
""")
