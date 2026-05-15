from ui.gui_theme import Colors

MAIN_STYLE = f"""
QMainWindow, QWidget {{
    background-color: {Colors.BG_MAIN};
    color: {Colors.TEXT};
    font-family: 'Segoe UI', Arial, sans-serif;
}}

QPushButton {{
    background-color: {Colors.ACCENT};
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 6px;
    font-weight: bold;
}}
QPushButton:hover {{ background-color: {Colors.ACCENT_HOVER}; }}
QPushButton:pressed {{ background-color: {Colors.ACCENT_PRESSED}; }}

QPushButton#btnPrimary {{ background-color: {Colors.ACCENT}; font-size: 16px; }}
QPushButton#btnPrimary:hover {{ background-color: {Colors.ACCENT_HOVER}; }}

QPushButton#btnSecondary {{ background-color: {Colors.SECONDARY}; font-size: 14px; }}
QPushButton#btnSecondary:hover {{ background-color: {Colors.SECONDARY_HOVER}; }}

QPushButton#btnDanger {{ background-color: {Colors.DANGER}; }}
QPushButton#btnDanger:hover {{ background-color: {Colors.DANGER_HOVER}; }}

QPushButton#btnWhy {{
    background-color: transparent;
    border: 1px solid {Colors.PURPLE};
    color: {Colors.TEXT};
}}
QPushButton#btnWhy:hover {{ background-color: {Colors.PURPLE}; }}

QLabel#titleLabel {{
    font-size: 28px;
    font-weight: bold;
    color: {Colors.ACCENT};
    margin-bottom: 10px;
}}
QLabel#subtitleLabel {{
    font-size: 16px;
    color: {Colors.TEXT_DIM};
    margin-bottom: 20px;
}}
QLabel#questionLabel {{
    font-size: 20px;
    font-weight: bold;
    margin: 20px 0;
    color: {Colors.TEXT_WHITE};
}}
QLabel#progressLabel {{
    font-size: 14px;
    color: {Colors.TEXT_MUTED};
}}

QRadioButton {{ font-size: 14px; color: {Colors.TEXT}; padding: 5px; }}
QRadioButton::indicator {{ width: 18px; height: 18px; }}
QRadioButton::indicator:checked {{
    background-color: {Colors.ACCENT};
    border: 2px solid {Colors.ACCENT};
    border-radius: 9px;
}}
QRadioButton::indicator:unchecked {{
    background-color: transparent;
    border: 2px solid {Colors.PURPLE};
    border-radius: 9px;
}}

QProgressBar {{
    border: none;
    border-radius: 6px;
    background-color: {Colors.SECONDARY};
    text-align: center;
}}
QProgressBar::chunk {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 {Colors.PURPLE}, stop:1 {Colors.ACCENT});
    border-radius: 6px;
}}

QLineEdit, QTextEdit, QDoubleSpinBox, QSpinBox {{
    background-color: {Colors.BG_CARD};
    border: 1px solid {Colors.PURPLE};
    color: {Colors.TEXT};
    padding: 8px;
    border-radius: 4px;
}}
QLineEdit:focus, QTextEdit:focus {{ border: 1px solid {Colors.ACCENT}; }}

QTableWidget {{
    background-color: {Colors.BG_CARD};
    alternate-background-color: {Colors.BG_MAIN};
    color: {Colors.TEXT};
    border: none;
    gridline-color: {Colors.BORDER};
}}
QTableWidget::item {{ padding: 6px; }}
QTableWidget::item:selected {{ background-color: {Colors.ACCENT}; color: white; }}

QHeaderView::section {{
    background-color: {Colors.SECONDARY};
    color: white;
    padding: 6px;
    border: none;
    font-weight: bold;
}}

QTabWidget::pane {{ border: 1px solid {Colors.BORDER}; top: -1px; }}
QTabBar::tab {{
    background-color: {Colors.SECONDARY};
    color: {Colors.TEXT};
    padding: 10px 20px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    margin-right: 2px;
}}
QTabBar::tab:selected {{ background-color: {Colors.ACCENT}; color: white; }}

QGroupBox {{
    border: 1px solid {Colors.BORDER};
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 20px;
    color: {Colors.TEXT};
    font-weight: bold;
}}

QScrollArea {{ border: none; }}
QMessageBox {{ background-color: {Colors.BG_MAIN}; }}
QMessageBox QLabel {{ color: {Colors.TEXT}; }}
QDialog {{ background-color: {Colors.BG_MAIN}; }}
"""
