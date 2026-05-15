from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QRadioButton, QButtonGroup, QProgressBar, QMessageBox, QSpacerItem, QSizePolicy, QFrame)
from PyQt6.QtCore import Qt

class QuestionnairePage(QWidget):
    def __init__(self, db, on_finish, on_back):
        super().__init__()
        self._db = db
        self._on_finish = on_finish
        self._on_back = on_back
        self._questions = []
        self._current_idx = 0
        self._answers = {}
        self._btn_group = None
        self._build_ui()

    def _build_ui(self):
        self._layout = QVBoxLayout(self)
        self._layout.setSpacing(15)
        self._layout.setContentsMargins(40, 20, 40, 20)
        top = QHBoxLayout()
        self._progress_label = QLabel()
        self._progress_label.setObjectName("progressLabel")
        top.addWidget(self._progress_label)
        top.addStretch()
        self._category_label = QLabel()
        self._category_label.setStyleSheet("color: #e94560; font-weight: bold;")
        top.addWidget(self._category_label)
        self._layout.addLayout(top)
        self._progress_bar = QProgressBar()
        self._progress_bar.setFixedHeight(8)
        self._progress_bar.setTextVisible(False)
        self._layout.addWidget(self._progress_bar)
        self._question_label = QLabel()
        self._question_label.setObjectName("questionLabel")
        self._question_label.setWordWrap(True)
        self._layout.addWidget(self._question_label)
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("color: #333;")
        self._layout.addWidget(line)
        self._answers_widget = QWidget()
        self._answers_layout = QVBoxLayout(self._answers_widget)
        self._answers_layout.setSpacing(8)
        self._layout.addWidget(self._answers_widget)
        self._layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        nav = QHBoxLayout()
        self._btn_back = QPushButton("← Назад")
        self._btn_back.setFixedWidth(150)
        self._btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_back.clicked.connect(self._go_back)
        nav.addWidget(self._btn_back)
        nav.addStretch()
        self._btn_next = QPushButton("Далі →")
        self._btn_next.setObjectName("btnPrimary")
        self._btn_next.setFixedWidth(150)
        self._btn_next.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_next.clicked.connect(self._go_next)
        nav.addWidget(self._btn_next)
        self._layout.addLayout(nav)

    def start(self):
        self._questions = self._db.get_all_questions()
        self._current_idx = 0
        self._answers = {}
        if not self._questions:
            QMessageBox.warning(self, "Увага", "У базі даних немає запитань.")
            self._on_back()
            return
        self._show_question()

    def _show_question(self):
        if not self._questions:
            return
        q = self._questions[self._current_idx]
        total = len(self._questions)
        self._progress_label.setText(f"Питання {self._current_idx + 1} з {total}")
        self._category_label.setText(f"Категорія: {q.category}")
        self._progress_bar.setMaximum(total)
        self._progress_bar.setValue(self._current_idx + 1)
        self._question_label.setText(q.text)
        if self._current_idx == 0:
            self._btn_back.setText("На головну")
        else:
            self._btn_back.setText("← Назад")
        is_last = self._current_idx == total - 1
        self._btn_next.setText("Результат" if is_last else "Далі →")
        while self._answers_layout.count():
            w = self._answers_layout.takeAt(0).widget()
            if w:
                w.deleteLater()
        self._btn_group = QButtonGroup(self)
        answers = self._db.get_question_answers(q.id)
        saved = self._answers.get(q.id)
        for i, ans in enumerate(answers):
            rb = QRadioButton(ans.label)
            rb.setProperty("answer_value", ans.value)
            if saved == ans.value:
                rb.setChecked(True)
            self._btn_group.addButton(rb, i)
            self._answers_layout.addWidget(rb)

    def _go_next(self):
        if not self._btn_group or self._btn_group.checkedId() == -1:
            QMessageBox.warning(self, "Увага", "Будь ласка, оберіть варіант відповіді.")
            return
        checked = self._btn_group.checkedButton()
        q = self._questions[self._current_idx]
        self._answers[q.id] = checked.property("answer_value")
        if self._current_idx < len(self._questions) - 1:
            self._current_idx += 1
            self._show_question()
        else:
            self._on_finish(self._answers)

    def _go_back(self):
        if self._current_idx > 0:
            checked = self._btn_group.checkedButton()
            if checked:
                q = self._questions[self._current_idx]
                self._answers[q.id] = checked.property("answer_value")
            self._current_idx -= 1
            self._show_question()
        else:
            self._on_back()
