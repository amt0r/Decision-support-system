import sqlite3
import hashlib
import json
from typing import List, Optional, Tuple
from models import Question, QuestionAnswer, Option, Rule, Admin

DB_PATH = "dss_energy.db"

class Database:
    def __init__(self, db_path: str = DB_PATH):
        self._db_path = db_path
        self._connection = None

    def connect(self):
        self._connection = sqlite3.connect(self._db_path)
        self._connection.execute("PRAGMA foreign_keys = ON")
        return self._connection

    def close(self):
        if self._connection:
            self._connection.close()
            self._connection = None

    def get_connection(self):
        if self._connection is None:
            self.connect()
        return self._connection

    def initialize(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                category TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS question_answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_id INTEGER NOT NULL,
                value TEXT NOT NULL,
                label TEXT NOT NULL,
                FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS options (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                description TEXT NOT NULL,
                base_score REAL NOT NULL DEFAULT 0.0
            );
            CREATE TABLE IF NOT EXISTS rules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_id INTEGER NOT NULL,
                answer_value TEXT NOT NULL,
                option_id INTEGER NOT NULL,
                score_adjustment REAL NOT NULL,
                FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE,
                FOREIGN KEY (option_id) REFERENCES options(id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            );
        """)
        conn.commit()

    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def get_all_questions(self) -> List[Question]:
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT id, text, category FROM questions ORDER BY id")
        return [Question(id=r[0], text=r[1], category=r[2]) for r in cursor.fetchall()]

    def get_question_answers(self, question_id: int) -> List[QuestionAnswer]:
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT id, question_id, value, label FROM question_answers WHERE question_id = ? ORDER BY id", (question_id,))
        return [QuestionAnswer(id=r[0], question_id=r[1], value=r[2], label=r[3]) for r in cursor.fetchall()]

    def get_all_options(self) -> List[Option]:
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT id, text, description, base_score FROM options ORDER BY id")
        return [Option(id=r[0], text=r[1], description=r[2], base_score=r[3]) for r in cursor.fetchall()]

    def get_option_by_id(self, option_id: int) -> Optional[Option]:
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT id, text, description, base_score FROM options WHERE id = ?", (option_id,))
        r = cursor.fetchone()
        if r:
            return Option(id=r[0], text=r[1], description=r[2], base_score=r[3])
        return None

    def get_rules_for_answer(self, question_id: int, answer_value: str) -> List[Rule]:
        cursor = self.get_connection().cursor()
        cursor.execute(
            "SELECT id, question_id, answer_value, option_id, score_adjustment FROM rules WHERE question_id = ? AND answer_value = ?",
            (question_id, answer_value)
        )
        return [Rule(id=r[0], question_id=r[1], answer_value=r[2], option_id=r[3], score_adjustment=r[4]) for r in cursor.fetchall()]

    def get_all_rules(self) -> List[Rule]:
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT id, question_id, answer_value, option_id, score_adjustment FROM rules ORDER BY id")
        return [Rule(id=r[0], question_id=r[1], answer_value=r[2], option_id=r[3], score_adjustment=r[4]) for r in cursor.fetchall()]

    def authenticate_admin(self, username: str, password: str) -> Optional[Admin]:
        cursor = self.get_connection().cursor()
        password_hash = self._hash_password(password)
        cursor.execute("SELECT id, username, password_hash FROM admins WHERE username = ? AND password_hash = ?", (username, password_hash))
        r = cursor.fetchone()
        if r:
            return Admin(id=r[0], username=r[1], password_hash=r[2])
        return None

    def add_question(self, text: str, category: str, answers: List[Tuple[str, str]]) -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO questions (text, category) VALUES (?, ?)", (text, category))
        question_id = cursor.lastrowid
        for value, label in answers:
            cursor.execute("INSERT INTO question_answers (question_id, value, label) VALUES (?, ?, ?)", (question_id, value, label))
        conn.commit()
        return question_id

    def add_question_with_rules(self, text: str, category: str, answers: List[Tuple[str, str]], rules_data: List[Tuple[str, int, float]]) -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO questions (text, category) VALUES (?, ?)", (text, category))
        question_id = cursor.lastrowid
        for value, label in answers:
            cursor.execute("INSERT INTO question_answers (question_id, value, label) VALUES (?, ?, ?)", (question_id, value, label))
        for answer_value, option_id, score_adjustment in rules_data:
            cursor.execute("INSERT INTO rules (question_id, answer_value, option_id, score_adjustment) VALUES (?, ?, ?, ?)", (question_id, answer_value, option_id, score_adjustment))
        conn.commit()
        return question_id

    def update_question(self, question_id: int, text: str, category: str):
        conn = self.get_connection()
        conn.execute("UPDATE questions SET text = ?, category = ? WHERE id = ?", (text, category, question_id))
        conn.commit()

    def update_question_with_rules(self, question_id: int, text: str, category: str, answers: List[Tuple[str, str]], rules_data: List[Tuple[str, int, float]]):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("UPDATE questions SET text = ?, category = ? WHERE id = ?", (text, category, question_id))
        
        cursor.execute("DELETE FROM question_answers WHERE question_id = ?", (question_id,))
        cursor.execute("DELETE FROM rules WHERE question_id = ?", (question_id,))
        
        for value, label in answers:
            cursor.execute("INSERT INTO question_answers (question_id, value, label) VALUES (?, ?, ?)", (question_id, value, label))
            
        for answer_value, option_id, score_adjustment in rules_data:
            cursor.execute(
                "INSERT INTO rules (question_id, answer_value, option_id, score_adjustment) VALUES (?, ?, ?, ?)",
                (question_id, answer_value, option_id, score_adjustment)
            )
            
        conn.commit()

    def delete_question(self, question_id: int):
        conn = self.get_connection()
        conn.execute("DELETE FROM question_answers WHERE question_id = ?", (question_id,))
        conn.execute("DELETE FROM rules WHERE question_id = ?", (question_id,))
        conn.execute("DELETE FROM questions WHERE id = ?", (question_id,))
        conn.commit()

    def add_option(self, text: str, description: str, base_score: float) -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO options (text, description, base_score) VALUES (?, ?, ?)", (text, description, base_score))
        conn.commit()
        return cursor.lastrowid

    def add_option_with_rules(self, text: str, description: str, base_score: float, rules_data: List[Tuple[int, str, float]]) -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO options (text, description, base_score) VALUES (?, ?, ?)", (text, description, base_score))
        option_id = cursor.lastrowid
        for question_id, answer_value, score_adjustment in rules_data:
            cursor.execute("INSERT INTO rules (question_id, answer_value, option_id, score_adjustment) VALUES (?, ?, ?, ?)", (question_id, answer_value, option_id, score_adjustment))
        conn.commit()
        return option_id

    def update_option(self, option_id: int, text: str, description: str, base_score: float):
        conn = self.get_connection()
        conn.execute("UPDATE options SET text = ?, description = ?, base_score = ? WHERE id = ?", (text, description, base_score, option_id))
        conn.commit()

    def delete_option(self, option_id: int):
        conn = self.get_connection()
        conn.execute("DELETE FROM rules WHERE option_id = ?", (option_id,))
        conn.execute("DELETE FROM options WHERE id = ?", (option_id,))
        conn.commit()

    def update_option_rules(self, option_id: int, rules_data: List[Tuple[int, str, float]]):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM rules WHERE option_id = ?", (option_id,))
        for question_id, answer_value, score_adjustment in rules_data:
            cursor.execute(
                "INSERT INTO rules (question_id, answer_value, option_id, score_adjustment) VALUES (?, ?, ?, ?)",
                (question_id, answer_value, option_id, score_adjustment)
            )
        conn.commit()

    def add_rule(self, question_id: int, answer_value: str, option_id: int, score_adjustment: float) -> int:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO rules (question_id, answer_value, option_id, score_adjustment) VALUES (?, ?, ?, ?)",
            (question_id, answer_value, option_id, score_adjustment)
        )
        conn.commit()
        return cursor.lastrowid

    def delete_rule(self, rule_id: int):
        conn = self.get_connection()
        conn.execute("DELETE FROM rules WHERE id = ?", (rule_id,))
        conn.commit()

    def get_question_by_id(self, question_id: int) -> Optional[Question]:
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT id, text, category FROM questions WHERE id = ?", (question_id,))
        r = cursor.fetchone()
        if r:
            return Question(id=r[0], text=r[1], category=r[2])
        return None

    def clear_all_data(self):
        conn = self.get_connection()
        conn.execute("DELETE FROM rules")
        conn.execute("DELETE FROM options")
        conn.execute("DELETE FROM question_answers")
        conn.execute("DELETE FROM questions")
        conn.commit()

    def export_data(self) -> dict:
        data = {
            "questions": [],
            "options": [],
            "rules": []
        }
        
        questions = self.get_all_questions()
        for q in questions:
            answers = self.get_question_answers(q.id)
            data["questions"].append({
                "id": q.id,
                "text": q.text,
                "category": q.category,
                "answers": [{"value": a.value, "label": a.label} for a in answers]
            })
            
        options = self.get_all_options()
        for o in options:
            data["options"].append({
                "id": o.id,
                "text": o.text,
                "description": o.description,
                "base_score": o.base_score
            })
            
        rules = self.get_all_rules()
        for r in rules:
            data["rules"].append({
                "question_id": r.question_id,
                "answer_value": r.answer_value,
                "option_id": r.option_id,
                "score_adjustment": r.score_adjustment
            })
            
        return data

    def import_data(self, data: dict):
        self.clear_all_data()
        conn = self.get_connection()
        cursor = conn.cursor()
        
        for q in data.get("questions", []):
            cursor.execute("INSERT INTO questions (id, text, category) VALUES (?, ?, ?)", (q["id"], q["text"], q["category"]))
            for a in q.get("answers", []):
                cursor.execute("INSERT INTO question_answers (question_id, value, label) VALUES (?, ?, ?)", (q["id"], a["value"], a["label"]))
                
        for o in data.get("options", []):
            cursor.execute("INSERT INTO options (id, text, description, base_score) VALUES (?, ?, ?, ?)", (o["id"], o["text"], o["description"], o["base_score"]))
            
        for r in data.get("rules", []):
            cursor.execute("INSERT INTO rules (question_id, answer_value, option_id, score_adjustment) VALUES (?, ?, ?, ?)", 
                           (r["question_id"], r["answer_value"], r["option_id"], r["score_adjustment"]))
                           
        conn.commit()

    def populate_initial_data(self):
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT COUNT(*) FROM questions")
        q_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM options")
        o_count = cursor.fetchone()[0]
        if q_count > 0 or o_count > 0:
            return

        questions_data = [
            ("Яка основна мета використання резервного живлення?", "призначення",
             [("a", "Освітлення та зарядка гаджетів"), ("b", "Побутова техніка (холодильник, бойлер)"), ("c", "Повне забезпечення будинку"), ("dk", "Не знаю")]),
            ("Який ваш бюджет на резервне живлення?", "бюджет",
             [("a", "До 10 000 грн"), ("b", "10 000 – 30 000 грн"), ("c", "30 000 – 80 000 грн"), ("d", "Понад 80 000 грн"), ("dk", "Не знаю")]),
            ("Яка потужність вам потрібна?", "потужність",
             [("a", "До 1 кВт"), ("b", "1–3 кВт"), ("c", "3–5 кВт"), ("d", "Понад 5 кВт"), ("dk", "Не знаю")]),
            ("Наскільки важливий рівень шуму?", "комфорт",
             [("a", "Дуже важливо (тиша)"), ("b", "Помірно важливо"), ("c", "Не важливо"), ("dk", "Не знаю")]),
            ("Чи є у вас доступ до достатнього сонячного світла?", "джерело",
             [("a", "Так, відмінний"), ("b", "Частковий"), ("c", "Ні, мінімальний"), ("dk", "Не знаю")]),
            ("Як часто відбуваються відключення електроенергії?", "частота",
             [("a", "Рідко (кілька разів на рік)"), ("b", "Регулярно (кілька разів на місяць)"), ("c", "Часто (щодня або через день)"), ("dk", "Не знаю")]),
            ("Яка типова тривалість відключення?", "тривалість",
             [("a", "До 2 годин"), ("b", "2–6 годин"), ("c", "6–12 годин"), ("d", "Понад 12 годин"), ("dk", "Не знаю")]),
            ("Наскільки важлива екологічність рішення?", "екологія",
             [("a", "Дуже важливо"), ("b", "Помірно важливо"), ("c", "Не важливо"), ("dk", "Не знаю")]),
            ("Чи потрібна портативність пристрою?", "мобільність",
             [("a", "Так, дуже важливо"), ("b", "Бажано, але не критично"), ("c", "Ні, стаціонарний варіант"), ("dk", "Не знаю")]),
            ("Скільки приладів потрібно живити одночасно?", "навантаження",
             [("a", "1–3 прилади"), ("b", "4–6 приладів"), ("c", "Понад 6 приладів"), ("dk", "Не знаю")]),
            ("Чи є можливість зберігання палива (бензин, дизель, газ)?", "паливо",
             [("a", "Так, є місце та можливість"), ("b", "Обмежена можливість"), ("c", "Ні, неможливо"), ("dk", "Не знаю")]),
            ("Чи потрібне автоматичне перемикання при зникненні електроенергії?", "автоматизація",
             [("a", "Так, обов'язково"), ("b", "Бажано"), ("c", "Ні, ручне перемикання прийнятне"), ("dk", "Не знаю")]),
        ]

        conn = self.get_connection()
        cursor = conn.cursor()

        q_id_map = {}
        for idx, (text, category, answers) in enumerate(questions_data, start=1):
            cursor.execute("INSERT INTO questions (text, category) VALUES (?, ?)", (text, category))
            q_id_map[idx] = cursor.lastrowid
            for val, label in answers:
                cursor.execute("INSERT INTO question_answers (question_id, value, label) VALUES (?, ?, ?)", (q_id_map[idx], val, label))

        options_data = [
            ("Бензиновий генератор 3кВт", "Класичний генератор на бензині потужністю 3 кВт. Надійне живлення побутових приладів. Потребує палива та обслуговування, шумний у роботі.", 0.0),
            ("Дизельний генератор 5кВт", "Потужний дизельний генератор на 5 кВт. Економічний у витраті палива, надійний для тривалої роботи. Важкий та шумний.", 0.0),
            ("Інверторний генератор 2кВт", "Тихий інверторний генератор потужністю 2 кВт. Видає чисту синусоїду для чутливої електроніки. Компактний та економічний.", 0.0),
            ("Портативна зарядна станція 1кВт", "Літій-іонна зарядна станція на 1 кВт. Безшумна, портативна, заряджається від мережі або сонячних панелей.", 0.0),
            ("Потужна зарядна станція 3кВт", "Високопотужна зарядна станція на 3 кВт з великим акумулятором. Живить основні побутові прилади протягом кількох годин.", 0.0),
            ("Сонячна електростанція 5кВт", "Комплект сонячних панелей з акумулятором та інвертором на 5 кВт. Екологічне рішення для автономного живлення.", 0.0),
            ("ДБЖ (UPS) 1.5кВт", "Джерело безперебійного живлення на 1.5 кВт. Миттєве перемикання при зникненні мережі. Ідеальний для комп'ютерів та мережевого обладнання.", 0.0),
            ("Гібридний інвертор 5кВт", "Потужний інвертор з підтримкою сонячних панелей та акумуляторів на 5 кВт. Автоматичне перемикання, програмований режим роботи.", 0.0),
            ("Газовий генератор 6кВт", "Генератор на природному газі або пропані потужністю 6 кВт. Менше обслуговування та тихіший за бензиновий аналог.", 0.0),
            ("Портативна сонячна станція 500Вт", "Компактна сонячна електростанція на 500 Вт з вбудованою панеллю. Ідеальна для зарядки гаджетів, освітлення та виїздів на природу.", 0.0),
        ]

        o_id_map = {}
        for idx, (text, desc, base) in enumerate(options_data, start=1):
            cursor.execute("INSERT INTO options (text, description, base_score) VALUES (?, ?, ?)", (text, desc, base))
            o_id_map[idx] = cursor.lastrowid

        rules_data = [
            (1, "a", 4, 15), (1, "a", 10, 15), (1, "a", 7, 5), (1, "a", 3, 5),
            (1, "a", 2, -5), (1, "a", 8, -5), (1, "a", 9, -5),
            (1, "b", 1, 15), (1, "b", 5, 15), (1, "b", 3, 5), (1, "b", 8, 5),
            (1, "b", 10, -1000),
            (1, "c", 2, 15), (1, "c", 8, 15), (1, "c", 6, 15), (1, "c", 9, 15),
            (1, "c", 3, -5), (1, "c", 4, -1000), (1, "c", 10, -1000), (1, "c", 7, -1000),

            (2, "a", 10, 15), (2, "a", 4, 5), (2, "a", 7, 5),
            (2, "a", 5, -5),
            (2, "a", 2, -1000), (2, "a", 6, -1000), (2, "a", 8, -1000), (2, "a", 9, -1000),
            (2, "b", 1, 15), (2, "b", 3, 15), (2, "b", 4, 5), (2, "b", 7, 5),
            (2, "c", 5, 15), (2, "c", 2, 5), (2, "c", 6, 5), (2, "c", 9, 5),
            (2, "d", 8, 15), (2, "d", 6, 15), (2, "d", 9, 5),

            (3, "a", 10, 15), (3, "a", 4, 5),
            (3, "a", 1, -5), (3, "a", 2, -5), (3, "a", 5, -5), (3, "a", 6, -5), (3, "a", 8, -5), (3, "a", 9, -5),
            (3, "b", 1, 15), (3, "b", 3, 15), (3, "b", 5, 15), (3, "b", 7, 5),
            (3, "b", 10, -1000),
            (3, "c", 2, 15), (3, "c", 6, 15), (3, "c", 8, 15), (3, "c", 5, 5),
            (3, "c", 4, -1000), (3, "c", 10, -1000), (3, "c", 7, -1000),
            (3, "d", 9, 15), (3, "d", 2, 5), (3, "d", 8, 5), (3, "d", 6, 5),
            (3, "d", 1, -5),
            (3, "d", 4, -1000), (3, "d", 10, -1000), (3, "d", 7, -1000), (3, "d", 3, -1000),

            (4, "a", 4, 15), (4, "a", 5, 15), (4, "a", 6, 15), (4, "a", 7, 15),
            (4, "a", 8, 15), (4, "a", 10, 15),
            (4, "a", 3, -5),
            (4, "a", 1, -1000), (4, "a", 2, -1000), (4, "a", 9, -1000),
            (4, "b", 3, 5),
            (4, "b", 1, -5), (4, "b", 2, -5),
            (4, "c", 1, 5), (4, "c", 2, 5), (4, "c", 9, 5),

            (5, "a", 6, 15), (5, "a", 10, 15), (5, "a", 8, 5),
            (5, "b", 6, 5), (5, "b", 10, 5), (5, "b", 8, 5),
            (5, "c", 1, 5), (5, "c", 2, 5), (5, "c", 9, 5),
            (5, "c", 8, -5),
            (5, "c", 6, -1000), (5, "c", 10, -1000),

            (6, "a", 7, 15), (6, "a", 4, 5), (6, "a", 10, 5),
            (6, "b", 1, 5), (6, "b", 3, 5), (6, "b", 5, 5), (6, "b", 6, 5),
            (6, "c", 8, 15), (6, "c", 6, 15), (6, "c", 2, 5), (6, "c", 9, 5),
            (6, "c", 7, -5),

            (7, "a", 7, 15), (7, "a", 4, 15), (7, "a", 10, 5),
            (7, "b", 5, 15), (7, "b", 1, 5), (7, "b", 3, 5), (7, "b", 4, 5),
            (7, "c", 2, 15), (7, "c", 1, 5), (7, "c", 5, 5), (7, "c", 9, 5),
            (7, "c", 7, -1000),
            (7, "d", 2, 15), (7, "d", 9, 15), (7, "d", 6, 15), (7, "d", 8, 15),
            (7, "d", 7, -1000), (7, "d", 4, -1000), (7, "d", 10, -1000),

            (8, "a", 6, 15), (8, "a", 10, 15),
            (8, "a", 4, 5), (8, "a", 5, 5), (8, "a", 7, 5), (8, "a", 8, 5),
            (8, "a", 3, -5),
            (8, "a", 1, -1000), (8, "a", 2, -1000), (8, "a", 9, -1000),
            (8, "b", 6, 5), (8, "b", 10, 5),
            (8, "b", 1, -5), (8, "b", 2, -5),

            (9, "a", 4, 15), (9, "a", 10, 15), (9, "a", 3, 5),
            (9, "a", 2, -1000), (9, "a", 6, -1000), (9, "a", 8, -1000), (9, "a", 9, -1000),
            (9, "b", 4, 5), (9, "b", 10, 5), (9, "b", 3, 5),
            (9, "b", 2, -5),
            (9, "c", 8, 5), (9, "c", 6, 5), (9, "c", 2, 5), (9, "c", 9, 5),

            (10, "a", 4, 15), (10, "a", 10, 5), (10, "a", 7, 5), (10, "a", 3, 5),
            (10, "b", 1, 15), (10, "b", 5, 15), (10, "b", 3, 5), (10, "b", 2, 5),
            (10, "b", 10, -1000),
            (10, "c", 2, 15), (10, "c", 9, 15), (10, "c", 8, 15), (10, "c", 6, 5),
            (10, "c", 4, -1000), (10, "c", 10, -1000), (10, "c", 7, -1000),

            (11, "a", 1, 15), (11, "a", 2, 15), (11, "a", 9, 15), (11, "a", 3, 5),
            (11, "b", 3, 5),
            (11, "b", 1, -5), (11, "b", 2, -5),
            (11, "c", 4, 5), (11, "c", 5, 5), (11, "c", 6, 5), (11, "c", 7, 5),
            (11, "c", 8, 5), (11, "c", 10, 5),
            (11, "c", 1, -1000), (11, "c", 2, -1000), (11, "c", 9, -1000), (11, "c", 3, -1000),

            (12, "a", 7, 15), (12, "a", 8, 15),
            (12, "a", 1, -1000), (12, "a", 2, -1000), (12, "a", 3, -1000), (12, "a", 9, -1000),
            (12, "b", 7, 5), (12, "b", 8, 5),
            (12, "c", 1, 5), (12, "c", 2, 5), (12, "c", 3, 5),
        ]

        for q_idx, aval, o_idx, adj in rules_data:
            real_qid = q_id_map[q_idx]
            real_oid = o_id_map[o_idx]
            cursor.execute("INSERT INTO rules (question_id, answer_value, option_id, score_adjustment) VALUES (?, ?, ?, ?)", (real_qid, aval, real_oid, adj))

        admin_hash = self._hash_password("admin123")
        cursor.execute("INSERT OR IGNORE INTO admins (username, password_hash) VALUES (?, ?)", ("admin", admin_hash))

        conn.commit()
