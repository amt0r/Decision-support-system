MAIN_STYLE = '''
QMainWindow, QWidget { background-color: #1a1a2e; color: #e0e0e0; font-family: 'Segoe UI', Arial, sans-serif; }
QPushButton { background-color: #e94560; color: white; border: none; padding: 10px 20px; border-radius: 6px; font-weight: bold; }
QPushButton:hover { background-color: #ff5773; }
QPushButton:pressed { background-color: #d13d55; }
QPushButton#btnPrimary { background-color: #e94560; font-size: 16px; }
QPushButton#btnPrimary:hover { background-color: #ff5773; }
QPushButton#btnSecondary { background-color: #0f3460; font-size: 14px; }
QPushButton#btnSecondary:hover { background-color: #1a4a80; }
QPushButton#btnDanger { background-color: #d9534f; }
QPushButton#btnDanger:hover { background-color: #c9302c; }
QPushButton#btnWhy { background-color: transparent; border: 1px solid #533483; color: #e0e0e0; }
QPushButton#btnWhy:hover { background-color: #533483; }
QLabel#titleLabel { font-size: 28px; font-weight: bold; color: #e94560; margin-bottom: 10px; }
QLabel#subtitleLabel { font-size: 16px; color: #a0a0b0; margin-bottom: 20px; }
QLabel#questionLabel { font-size: 20px; font-weight: bold; margin: 20px 0; color: #ffffff; }
QLabel#progressLabel { font-size: 14px; color: #888; }
QRadioButton { font-size: 14px; color: #e0e0e0; padding: 5px; }
QRadioButton::indicator { width: 18px; height: 18px; }
QRadioButton::indicator:checked { background-color: #e94560; border: 2px solid #e94560; border-radius: 9px; }
QRadioButton::indicator:unchecked { background-color: transparent; border: 2px solid #533483; border-radius: 9px; }
QProgressBar { border: none; border-radius: 6px; background-color: #0f3460; text-align: center; }
QProgressBar::chunk { background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #533483, stop:1 #e94560); border-radius: 6px; }
QLineEdit, QTextEdit, QDoubleSpinBox, QSpinBox { background-color: #16213e; border: 1px solid #533483; color: #e0e0e0; padding: 8px; border-radius: 4px; }
QLineEdit:focus, QTextEdit:focus { border: 1px solid #e94560; }
QTableWidget { background-color: #16213e; alternate-background-color: #1a1a2e; color: #e0e0e0; border: none; gridline-color: #333; }
QTableWidget::item { padding: 6px; }
QTableWidget::item:selected { background-color: #e94560; color: white; }
QHeaderView::section { background-color: #0f3460; color: white; padding: 6px; border: none; font-weight: bold; }
QTabWidget::pane { border: 1px solid #333; top: -1px; }
QTabBar::tab { background-color: #0f3460; color: #e0e0e0; padding: 10px 20px; border-top-left-radius: 6px; border-top-right-radius: 6px; margin-right: 2px; }
QTabBar::tab:selected { background-color: #e94560; color: white; }
QGroupBox { border: 1px solid #333; border-radius: 8px; margin-top: 12px; padding-top: 20px; color: #e0e0e0; font-weight: bold; }
QScrollArea { border: none; }
QMessageBox { background-color: #1a1a2e; }
QMessageBox QLabel { color: #e0e0e0; }
QDialog { background-color: #1a1a2e; }
'''
