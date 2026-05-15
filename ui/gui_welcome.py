from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
from ui.gui_theme import Styles, Widgets

class WelcomePage(QWidget):
    def __init__(self, on_start, on_admin):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)
        layout.addSpacerItem(QSpacerItem(20, 60, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        title = QLabel("Система підтримки прийняття рішень")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        subtitle = QLabel("Підбір резервного живлення для дому")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        desc = QLabel("Дайте відповіді на запитання, і система\nпідбере оптимальне рішення для вашого випадку.")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setStyleSheet(Styles.text_style(14))
        layout.addWidget(desc)
        btn_start = Widgets.button("Почати консультацію", on_click=on_start, variant="primary", width=300)
        layout.addWidget(btn_start, alignment=Qt.AlignmentFlag.AlignCenter)
        btn_admin = Widgets.button("Панель адміністратора", on_click=on_admin, variant="secondary", width=300)
        layout.addWidget(btn_admin, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacerItem(QSpacerItem(20, 60, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
