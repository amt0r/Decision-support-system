from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox, QTabWidget, QFormLayout, QDoubleSpinBox, QDialog, QFileDialog)
from PyQt6.QtCore import Qt
from ui.gui_theme import Colors, Styles, Widgets
from core.database import Database


SCORE_BUTTONS = [
    ("Ідеально", Colors.SCORE_PERFECT, 15),
    ("Добре", Colors.SCORE_GOOD, 5),
    ("Байдуже", Colors.SCORE_NEUTRAL, 0),
    ("Погано", Colors.SCORE_BAD, -5),
    ("Недоречно", Colors.SCORE_CRITICAL, -1000),
]


def _add_score_buttons(layout, spin):
    for text, color, value in SCORE_BUTTONS:
        btn = QPushButton(text)
        btn.setStyleSheet(Styles.colored_btn(color))
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.clicked.connect(lambda checked, s=spin, v=value: s.setValue(v))
        layout.addWidget(btn)


def _create_spin():
    spin = QDoubleSpinBox()
    spin.setRange(-2000, 2000)
    spin.setSingleStep(1)
    spin.setDecimals(0)
    spin.setFixedWidth(100)
    return spin


def _build_rules_for_answers(db, rules_layout, spinboxes, questions, get_current_value=None):
    for q in questions:
        q_lbl = QLabel(f"Запитання: {q.text}")
        q_lbl.setStyleSheet(Styles.label_heading())
        rules_layout.addWidget(q_lbl)

        answers = db.get_question_answers(q.id)
        for a in answers:
            if a.value == "dk":
                continue

            row = QHBoxLayout()
            row.addWidget(QLabel(f"  • {a.label}"))

            spin = _create_spin()
            if get_current_value:
                spin.setValue(get_current_value(q.id, a.value))

            _add_score_buttons(row, spin)
            row.addWidget(spin)

            rules_layout.addLayout(row)
            spinboxes.append((q.id, a.value, spin))


def _build_rules_for_options(options, rules_layout, rules_widgets, answer_val, get_current_value=None):
    lbl_rules = QLabel(f"Бали для варіанту '{answer_val}':")
    lbl_rules.setStyleSheet(Styles.label_heading())
    rules_layout.addWidget(lbl_rules)

    for opt in options:
        row_layout = QHBoxLayout()
        row_layout.addWidget(QLabel(f"  -> {opt.text[:30]}..."))

        spin = _create_spin()
        if get_current_value:
            spin.setValue(get_current_value(opt.id))

        _add_score_buttons(row_layout, spin)
        row_layout.addWidget(spin)

        rules_layout.addLayout(row_layout)
        rules_widgets.append((answer_val, opt.id, spin))


def _collect_rules_from_spinboxes(spinboxes):
    return [(q_id, a_val, spin.value()) for q_id, a_val, spin in spinboxes if spin.value() != 0]


def _collect_question_rules(rules_widgets):
    return [(val, opt_id, spin.value()) for val, opt_id, spin in rules_widgets if spin.value() != 0]


def _collect_answers(answers_list):
    result = [(val, inp.text().strip()) for val, inp in answers_list if inp.text().strip()]
    result.append(("dk", "Не знаю"))
    return result


class AdminLoginDialog(QDialog):
    def __init__(self, db: Database, parent=None):
        super().__init__(parent)
        self._db = db
        self.is_authenticated = False
        self.setWindowTitle("Вхід адміністратора")
        self.setFixedSize(300, 200)
        layout = QVBoxLayout(self)
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Логін")
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Пароль")
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(QLabel("Логін:"))
        layout.addWidget(self.user_input)
        layout.addWidget(QLabel("Пароль:"))
        layout.addWidget(self.pass_input)
        layout.addWidget(Widgets.button("Увійти", on_click=self._login))

    def _login(self):
        user = self.user_input.text().strip()
        pwd = self.pass_input.text().strip()
        if not user or not pwd:
            QMessageBox.warning(self, "Помилка", "Введіть логін та пароль.")
            return
        admin = self._db.authenticate_admin(user, pwd)
        if admin:
            self.is_authenticated = True
            self.accept()
        else:
            QMessageBox.warning(self, "Помилка", "Невірний логін або пароль.")


class AddOptionDialog(QDialog):
    def __init__(self, db: Database, parent=None):
        super().__init__(parent)
        self._db = db
        self.setWindowTitle("Додати нове рішення (Обладнання)")
        self.setMinimumSize(1500, 800)

        self.text_input = QLineEdit()
        self.desc_input = QLineEdit()

        layout = QVBoxLayout(self)
        form = QFormLayout()
        form.addRow("Назва:", self.text_input)
        form.addRow("Опис:", self.desc_input)
        layout.addLayout(form)

        layout.addWidget(QLabel("Бали за кожну відповідь (+ або -):"))
        scroll, self.rules_layout = Widgets.scroll_area()

        self.spinboxes = []
        questions = self._db.get_all_questions()
        _build_rules_for_answers(self._db, self.rules_layout, self.spinboxes, questions)

        layout.addWidget(scroll)
        layout.addWidget(Widgets.button("Зберегти", on_click=self.accept))

    def get_data(self):
        return (
            self.text_input.text().strip(),
            self.desc_input.text().strip(),
            0.0,
            _collect_rules_from_spinboxes(self.spinboxes)
        )


class EditOptionRulesDialog(QDialog):
    def __init__(self, db: Database, option_id: int, option_text: str, parent=None):
        super().__init__(parent)
        self._db = db
        self.option_id = option_id
        self.setWindowTitle(f"Редагувати бали: {option_text}")
        self.setMinimumSize(1500, 800)

        layout = QVBoxLayout(self)
        lbl_title = QLabel(f"Редагування балів для: <b>{option_text}</b>")
        lbl_title.setStyleSheet("font-size: 14px; margin-bottom: 10px;")
        layout.addWidget(lbl_title)
        layout.addWidget(QLabel("Бали за кожну відповідь (+ або -):"))

        scroll, self.rules_layout = Widgets.scroll_area()

        self.spinboxes = []
        questions = self._db.get_all_questions()
        all_rules = self._db.get_all_rules()

        current_rules = {}
        for r in all_rules:
            if r.option_id == self.option_id:
                current_rules[(r.question_id, r.answer_value)] = r.score_adjustment

        def get_val(q_id, a_val):
            return current_rules.get((q_id, a_val), 0.0)

        _build_rules_for_answers(self._db, self.rules_layout, self.spinboxes, questions, get_current_value=get_val)

        layout.addWidget(scroll)
        layout.addWidget(Widgets.button("Зберегти", on_click=self.accept))

    def get_data(self):
        return _collect_rules_from_spinboxes(self.spinboxes)


class AddQuestionDialog(QDialog):
    def __init__(self, db: Database, parent=None):
        super().__init__(parent)
        self._db = db
        self.setWindowTitle("Додати нове питання")
        self.setMinimumSize(1000, 600)

        self.text_input = QLineEdit()
        self.cat_input = QLineEdit()

        layout = QVBoxLayout(self)
        form = QFormLayout()
        form.addRow("Текст питання:", self.text_input)
        form.addRow("Категорія:", self.cat_input)
        layout.addLayout(form)

        self.answers = []
        self.rules_widgets = []

        self.answers_layout = QVBoxLayout()
        layout.addLayout(self.answers_layout)
        layout.addWidget(Widgets.button("Додати варіант відповіді", on_click=self._add_answer_row))

        scroll, self.rules_layout = Widgets.scroll_area()
        layout.addWidget(scroll)
        layout.addWidget(Widgets.button("Зберегти", on_click=self.accept))

        self.options = self._db.get_all_options()
        self._val_counter = 97

    def _add_answer_row(self):
        val = chr(self._val_counter)
        self._val_counter += 1

        lbl = QLabel(f"Відповідь '{val}':")
        inp = QLineEdit()
        row = QHBoxLayout()
        row.addWidget(lbl)
        row.addWidget(inp)
        self.answers_layout.addLayout(row)
        self.answers.append((val, inp))

        _build_rules_for_options(self.options, self.rules_layout, self.rules_widgets, val)

    def get_data(self):
        return (
            self.text_input.text().strip(),
            self.cat_input.text().strip(),
            _collect_answers(self.answers),
            _collect_question_rules(self.rules_widgets)
        )


class EditQuestionDialog(QDialog):
    def __init__(self, db: Database, question_id: int, question_text: str, question_category: str, parent=None):
        super().__init__(parent)
        self._db = db
        self.question_id = question_id
        self.setWindowTitle(f"Редагувати питання: {question_text}")
        self.setMinimumSize(1000, 600)

        self.text_input = QLineEdit()
        self.text_input.setText(question_text)
        self.cat_input = QLineEdit()
        self.cat_input.setText(question_category)

        layout = QVBoxLayout(self)
        form = QFormLayout()
        form.addRow("Текст питання:", self.text_input)
        form.addRow("Категорія:", self.cat_input)
        layout.addLayout(form)

        self.answers = []
        self.rules_widgets = []

        self.answers_layout = QVBoxLayout()
        layout.addLayout(self.answers_layout)
        layout.addWidget(Widgets.button("Додати варіант відповіді", on_click=self._add_answer_row_empty))

        scroll, self.rules_layout = Widgets.scroll_area()
        layout.addWidget(scroll)
        layout.addWidget(Widgets.button("Зберегти", on_click=self.accept))

        self.options = self._db.get_all_options()
        self._val_counter = 97

        self.all_rules = self._db.get_all_rules()
        current_answers = self._db.get_question_answers(self.question_id)

        for ans in current_answers:
            if ans.value == "dk":
                continue
            if len(ans.value) == 1 and 'a' <= ans.value <= 'z':
                self._val_counter = max(self._val_counter, ord(ans.value) + 1)
            self._add_answer_row_with_data(ans.value, ans.label)

    def _add_answer_row_empty(self):
        val = chr(self._val_counter)
        self._val_counter += 1
        self._add_answer_row_with_data(val, "")

    def _add_answer_row_with_data(self, val: str, label: str):
        lbl = QLabel(f"Відповідь '{val}':")
        inp = QLineEdit()
        inp.setText(label)
        row = QHBoxLayout()
        row.addWidget(lbl)
        row.addWidget(inp)
        self.answers_layout.addLayout(row)
        self.answers.append((val, inp))

        current_ans_rules = {}
        for r in self.all_rules:
            if r.question_id == self.question_id and r.answer_value == val:
                current_ans_rules[r.option_id] = r.score_adjustment

        def get_val(opt_id):
            return current_ans_rules.get(opt_id, 0.0)

        _build_rules_for_options(self.options, self.rules_layout, self.rules_widgets, val, get_current_value=get_val)

    def get_data(self):
        return (
            self.text_input.text().strip(),
            self.cat_input.text().strip(),
            _collect_answers(self.answers),
            _collect_question_rules(self.rules_widgets)
        )


class AdminPanelPage(QWidget):
    def __init__(self, db: Database, on_logout):
        super().__init__()
        self._db = db
        self._on_logout = on_logout
        self._build_ui()

    def _build_ui(self):
        self._layout = QVBoxLayout(self)
        header = QHBoxLayout()
        title = QLabel("Панель адміністратора")
        title.setObjectName("titleLabel")
        header.addWidget(title)
        header.addStretch()
        header.addWidget(Widgets.button("Вийти", on_click=self._on_logout, variant="danger"))
        self._layout.addLayout(header)

        self._tabs = QTabWidget()
        self._layout.addWidget(self._tabs)

        self._tab_questions = QWidget()
        self._build_questions_tab()
        self._tabs.addTab(self._tab_questions, "Питання")

        self._tab_options = QWidget()
        self._build_options_tab()
        self._tabs.addTab(self._tab_options, "Рішення (Обладнання)")

        self._tab_migration = QWidget()
        self._build_migration_tab()
        self._tabs.addTab(self._tab_migration, "Міграція")

    def _build_questions_tab(self):
        layout = QVBoxLayout(self._tab_questions)
        self._q_table = QTableWidget()
        self._q_table.setColumnCount(2)
        self._q_table.setHorizontalHeaderLabels(["Текст", "Категорія"])
        self._q_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self._q_table)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(Widgets.button("Додати питання", on_click=self._add_question))
        btn_layout.addWidget(Widgets.button("Редагувати питання", on_click=self._edit_question, variant="secondary"))
        btn_layout.addWidget(Widgets.button("Видалити питання", on_click=self._delete_question, variant="danger"))
        layout.addLayout(btn_layout)

    def _build_options_tab(self):
        layout = QVBoxLayout(self._tab_options)
        self._opt_table = QTableWidget()
        self._opt_table.setColumnCount(2)
        self._opt_table.setHorizontalHeaderLabels(["Назва", "Опис"])
        self._opt_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self._opt_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self._opt_table)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(Widgets.button("Додати рішення", on_click=self._add_option))
        btn_layout.addWidget(Widgets.button("Редагувати бали", on_click=self._edit_option_rules, variant="secondary"))
        btn_layout.addWidget(Widgets.button("Видалити рішення", on_click=self._delete_option, variant="danger"))
        layout.addLayout(btn_layout)

    def load_data(self):
        questions = self._db.get_all_questions()
        self._q_table.setRowCount(len(questions))
        for i, q in enumerate(questions):
            t_item = QTableWidgetItem(q.text)
            t_item.setData(Qt.ItemDataRole.UserRole, q.id)
            self._q_table.setItem(i, 0, t_item)
            self._q_table.setItem(i, 1, QTableWidgetItem(q.category))

        options = self._db.get_all_options()
        self._opt_table.setRowCount(len(options))
        for i, opt in enumerate(options):
            t_item = QTableWidgetItem(opt.text)
            t_item.setData(Qt.ItemDataRole.UserRole, opt.id)
            self._opt_table.setItem(i, 0, t_item)
            self._opt_table.setItem(i, 1, QTableWidgetItem(opt.description))

    def _add_question(self):
        dialog = AddQuestionDialog(self._db, self)
        if dialog.exec():
            text, cat, ans_data, rules_data = dialog.get_data()
            if not text or not cat or not ans_data:
                QMessageBox.warning(self, "Помилка", "Заповніть всі обов'язкові поля!")
                return
            self._db.add_question_with_rules(text, cat, ans_data, rules_data)
            self.load_data()
            QMessageBox.information(self, "Успіх", "Питання з варіантами та правилами збережено!")

    def _delete_question(self):
        row = self._q_table.currentRow()
        if row < 0:
            return
        q_id = self._q_table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        if QMessageBox.question(self, "Підтвердження", "Видалити питання і всі його правила?") == QMessageBox.StandardButton.Yes:
            self._db.delete_question(q_id)
            self.load_data()

    def _edit_question(self):
        row = self._q_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Помилка", "Виберіть питання для редагування!")
            return
        q_id = self._q_table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        q_text = self._q_table.item(row, 0).text()
        q_cat = self._q_table.item(row, 1).text()

        dialog = EditQuestionDialog(self._db, q_id, q_text, q_cat, self)
        if dialog.exec():
            text, cat, ans_data, rules_data = dialog.get_data()
            if not text or not cat or not ans_data:
                QMessageBox.warning(self, "Помилка", "Заповніть всі обов'язкові поля!")
                return
            self._db.update_question_with_rules(q_id, text, cat, ans_data, rules_data)
            self.load_data()
            QMessageBox.information(self, "Успіх", "Питання успішно оновлено!")

    def _add_option(self):
        dialog = AddOptionDialog(self._db, self)
        if dialog.exec():
            text, desc, base, rules = dialog.get_data()
            if not text or not desc:
                QMessageBox.warning(self, "Помилка", "Заповніть назву та опис!")
                return
            self._db.add_option_with_rules(text, desc, base, rules)
            self.load_data()
            QMessageBox.information(self, "Успіх", "Нове рішення успішно додано разом із правилами нарахування балів!")

    def _delete_option(self):
        row = self._opt_table.currentRow()
        if row < 0:
            return
        opt_id = self._opt_table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        if QMessageBox.question(self, "Підтвердження", "Видалити рішення?") == QMessageBox.StandardButton.Yes:
            self._db.delete_option(opt_id)
            self.load_data()

    def _edit_option_rules(self):
        row = self._opt_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Помилка", "Виберіть рішення для редагування балів!")
            return
        opt_id = self._opt_table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        opt_text = self._opt_table.item(row, 0).text()

        dialog = EditOptionRulesDialog(self._db, opt_id, opt_text, self)
        if dialog.exec():
            rules = dialog.get_data()
            self._db.update_option_rules(opt_id, rules)
            QMessageBox.information(self, "Успіх", "Бали успішно оновлено!")

    def _build_migration_tab(self):
        layout = QVBoxLayout(self._tab_migration)

        lbl_info = QLabel("<b>Міграція даних</b><br>Тут ви можете зберегти всі налаштування запитань та обладнання у файл, або відновити їх. Також можна повністю очистити базу.")
        lbl_info.setStyleSheet("font-size: 14px; margin-bottom: 20px;")
        layout.addWidget(lbl_info)
        layout.addWidget(Widgets.button("Експортувати в JSON (Зберегти)", on_click=self._export_data, variant="export"))
        layout.addWidget(Widgets.button("Імпортувати з JSON (Завантажити)", on_click=self._import_data, variant="import"))
        layout.addSpacing(40)
        layout.addWidget(Widgets.button("Очистити базу даних (Скинути все)", on_click=self._clear_database, variant="critical"))
        layout.addStretch()

    def _export_data(self):
        import json
        data = self._db.export_data()
        file_path, _ = QFileDialog.getSaveFileName(self, "Експортувати дані", "dss_backup.json", "JSON Files (*.json)")
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                QMessageBox.information(self, "Успіх", "Дані успішно експортовано!")
            except Exception as e:
                QMessageBox.critical(self, "Помилка", f"Не вдалося зберегти файл:\n{e}")

    def _import_data(self):
        import json
        import os
        file_path, _ = QFileDialog.getOpenFileName(self, "Імпортувати дані", "", "JSON Files (*.json)")
        if file_path:
            if not os.path.exists(file_path):
                QMessageBox.critical(self, "Помилка", "Обраний файл не існує.")
                return

            reply = QMessageBox.question(self, "Увага!", "Імпорт повністю зітре всі поточні запитання та обладнання і замінить їх даними з файлу. Продовжити?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    self._db.validate_import_data(data)

                    self._db.import_data(data)
                    self.load_data()
                    QMessageBox.information(self, "Успіх", "Дані успішно імпортовано!")
                except json.JSONDecodeError:
                    QMessageBox.critical(self, "Помилка", "Файл не є валідним JSON або пошкоджений.")
                except ValueError as ve:
                    QMessageBox.critical(self, "Помилка", f"Невірний формат або структура файлу:\n{ve}")
                except Exception as e:
                    QMessageBox.critical(self, "Помилка", f"Не вдалося завантажити файл:\n{e}")

    def _clear_database(self):
        reply = QMessageBox.question(self, "КРИТИЧНА ДІЯ", "Ви впевнені, що хочете видалити всі запитання, обладнання та правила? Цю дію неможливо скасувати!", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self._db.clear_all_data()
            self.load_data()
            QMessageBox.information(self, "Успіх", "База даних повністю очищена.")
