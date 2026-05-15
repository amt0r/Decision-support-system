from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QProgressBar, QScrollArea, QFrame, QDialog, QTextEdit, QSpacerItem, QSizePolicy)
from PyQt6.QtCore import Qt
from ui.gui_theme import Colors, Styles, Widgets
from core.models import Recommendation
from typing import List

class ResultsPage(QWidget):
    def __init__(self, on_restart, on_home):
        super().__init__()
        self._on_restart = on_restart
        self._on_home = on_home
        self._recommendations = []
        self._build_ui()

    def _build_ui(self):
        self._layout = QVBoxLayout(self)
        self._layout.setSpacing(15)
        self._layout.setContentsMargins(40, 20, 40, 20)
        title = QLabel("Результати аналізу")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._layout.addWidget(title)
        subtitle = QLabel("Топ-10 рекомендованих рішень для вашого випадку")
        subtitle.setObjectName("subtitleLabel")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._layout.addWidget(subtitle)
        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll_widget = QWidget()
        self._scroll_layout = QVBoxLayout(self._scroll_widget)
        self._scroll_layout.setSpacing(15)
        self._scroll.setWidget(self._scroll_widget)
        self._layout.addWidget(self._scroll)
        nav = QHBoxLayout()
        nav.addWidget(Widgets.button("Пройти знову", on_click=self._on_restart, variant="primary", width=200))
        nav.addStretch()
        nav.addWidget(Widgets.button("На головну", on_click=self._on_home, variant="secondary", width=200))
        self._layout.addLayout(nav)

    def show_results(self, recommendations: List[Recommendation]):
        self._recommendations = recommendations
        while self._scroll_layout.count():
            item = self._scroll_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()
        medals = ["🥇", "🥈", "🥉"]
        for i, rec in enumerate(recommendations[:10]):
            card = QFrame()
            color = Colors.MEDAL_COLORS[i] if i < 3 else Colors.BORDER_LIGHT
            card.setStyleSheet(Styles.result_card(color))
            card_layout = QVBoxLayout(card)
            card_layout.setSpacing(10)
            header = QHBoxLayout()
            medal_str = f"{medals[i]} #{i+1}" if i < 3 else f"#{i+1}"
            medal = QLabel(medal_str)
            medal.setStyleSheet(Styles.text_style(22, color, bold=True))
            header.addWidget(medal)
            header.addStretch()
            pct = QLabel(f"{rec.percentage:.1f}%")
            pct.setStyleSheet(Styles.text_style(20, color, bold=True))
            header.addWidget(pct)
            card_layout.addLayout(header)
            name = QLabel(rec.option.text)
            name.setStyleSheet(Styles.text_style(18, Colors.TEXT_WHITE, bold=True))
            name.setWordWrap(True)
            card_layout.addWidget(name)
            desc = QLabel(rec.option.description)
            desc.setStyleSheet(Styles.text_style(13, Colors.TEXT_DIM))
            desc.setWordWrap(True)
            card_layout.addWidget(desc)
            bar = QProgressBar()
            bar.setMaximum(100)
            bar.setValue(int(rec.percentage))
            bar.setFixedHeight(12)
            bar.setTextVisible(False)
            card_layout.addWidget(bar)
            score_label = QLabel(f"Загальний бал: {rec.score:.1f}")
            score_label.setStyleSheet(Styles.text_style(12, Colors.TEXT_MUTED))
            card_layout.addWidget(score_label)
            card_layout.addWidget(Widgets.button(
                "Чому цей варіант?", on_click=lambda checked, r=rec: self._show_explanation(r), variant="outline"))
            self._scroll_layout.addWidget(card)
        self._scroll_layout.addSpacerItem(
            QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

    def _show_explanation(self, rec: Recommendation):
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Чому: {rec.option.text}")
        dialog.setMinimumSize(600, 450)
        layout = QVBoxLayout(dialog)
        header = QLabel(f"Пояснення для: {rec.option.text}")
        header.setStyleSheet(Styles.text_style(16, Colors.ACCENT, bold=True, extra="padding: 10px"))
        header.setWordWrap(True)
        layout.addWidget(header)
        info = QLabel(f"Загальний бал: {rec.score:.1f} | Відповідність: {rec.percentage:.1f}%")
        info.setStyleSheet(Styles.text_style(14, Colors.TEXT_DIM, extra="padding: 5px"))
        layout.addWidget(info)
        text = QTextEdit()
        text.setReadOnly(True)
        report = "Цей варіант підібрано, тому що (переваги):\n"
        pos_exps = [e for e in rec.explanations if "✅" in e]
        neg_exps = [e for e in rec.explanations if "❌" in e]

        if pos_exps:
            for exp in pos_exps:
                report += f"  {exp}\n"
        else:
            report += "  (Немає явних переваг згідно з вашими відповідями)\n"

        report += "\nНедоліки або невідповідності (що зменшило бал):\n"
        if neg_exps:
            for exp in neg_exps:
                report += f"  {exp}\n"
        else:
            report += "  (Жодних суттєвих недоліків не виявлено)\n"
        text.setPlainText(report)
        text.setStyleSheet(f"font-size: 13px; background-color: {Colors.BG_INPUT}; border-radius: 8px; padding: 10px;")
        layout.addWidget(text)
        layout.addWidget(Widgets.button("Закрити", on_click=dialog.close, width=120),
                         alignment=Qt.AlignmentFlag.AlignCenter)
        dialog.exec()
