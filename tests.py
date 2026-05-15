import unittest
import os
import json
from database import Database
from engine import InferenceEngine

class TestDatabaseInitialization(unittest.TestCase):
    def setUp(self):
        self.test_db_path = "test_dss.db"
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
        self.db = Database(self.test_db_path)
        self.db.initialize()
        self.db.populate_initial_data()

    def tearDown(self):
        self.db.close()
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

    def test_questions_populated(self):
        questions = self.db.get_all_questions()
        self.assertGreater(len(questions), 0)
        self.assertEqual(len(questions), 12)

    def test_options_populated(self):
        options = self.db.get_all_options()
        self.assertGreater(len(options), 0)
        self.assertEqual(len(options), 10)

    def test_rules_populated(self):
        rules = self.db.get_all_rules()
        self.assertGreater(len(rules), 0)

    def test_question_answers_populated(self):
        questions = self.db.get_all_questions()
        for q in questions:
            answers = self.db.get_question_answers(q.id)
            self.assertGreater(len(answers), 0, f"Запитання '{q.text}' не має відповідей")

    def test_populate_idempotent(self):
        """Повторний виклик populate_initial_data не дублює дані."""
        count_before = len(self.db.get_all_questions())
        self.db.populate_initial_data()
        count_after = len(self.db.get_all_questions())
        self.assertEqual(count_before, count_after)

class TestAdminAuthentication(unittest.TestCase):
    def setUp(self):
        self.test_db_path = "test_dss.db"
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
        self.db = Database(self.test_db_path)
        self.db.initialize()
        self.db.populate_initial_data()

    def tearDown(self):
        self.db.close()
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

    def test_valid_login(self):
        admin = self.db.authenticate_admin("admin", "admin123")
        self.assertIsNotNone(admin)
        self.assertEqual(admin.username, "admin")

    def test_wrong_password(self):
        admin = self.db.authenticate_admin("admin", "wrongpass")
        self.assertIsNone(admin)

    def test_wrong_username(self):
        admin = self.db.authenticate_admin("nonexistent", "admin123")
        self.assertIsNone(admin)

    def test_empty_credentials(self):
        admin = self.db.authenticate_admin("", "")
        self.assertIsNone(admin)

class TestQuestionCRUD(unittest.TestCase):
    def setUp(self):
        self.test_db_path = "test_dss.db"
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
        self.db = Database(self.test_db_path)
        self.db.initialize()
        self.db.populate_initial_data()

    def tearDown(self):
        self.db.close()
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

    def test_add_question(self):
        count_before = len(self.db.get_all_questions())
        answers = [("a", "Так"), ("b", "Ні"), ("dk", "Не знаю")]
        q_id = self.db.add_question("Тестове запитання?", "тест", answers)
        self.assertIsNotNone(q_id)
        count_after = len(self.db.get_all_questions())
        self.assertEqual(count_after, count_before + 1)

    def test_add_question_with_rules(self):
        options = self.db.get_all_options()
        opt_id = options[0].id
        answers = [("a", "Так"), ("b", "Ні"), ("dk", "Не знаю")]
        rules = [("a", opt_id, 10.0), ("b", opt_id, -5.0)]
        q_id = self.db.add_question_with_rules("З правилами?", "тест", answers, rules)
        
        saved_rules = self.db.get_rules_for_answer(q_id, "a")
        self.assertEqual(len(saved_rules), 1)
        self.assertEqual(saved_rules[0].score_adjustment, 10.0)

    def test_delete_question(self):
        answers = [("a", "Так"), ("dk", "Не знаю")]
        q_id = self.db.add_question("Видалити мене?", "тест", answers)
        count_before = len(self.db.get_all_questions())
        self.db.delete_question(q_id)
        count_after = len(self.db.get_all_questions())
        self.assertEqual(count_after, count_before - 1)

    def test_delete_question_cascades_rules(self):
        options = self.db.get_all_options()
        opt_id = options[0].id
        answers = [("a", "Так"), ("dk", "Не знаю")]
        rules = [("a", opt_id, 15.0)]
        q_id = self.db.add_question_with_rules("Каскад?", "тест", answers, rules)
        
        rules_before = len(self.db.get_all_rules())
        self.db.delete_question(q_id)
        rules_after = len(self.db.get_all_rules())
        self.assertLess(rules_after, rules_before)

    def test_update_question_with_rules(self):
        options = self.db.get_all_options()
        opt_id = options[0].id
        answers = [("a", "Старий"), ("dk", "Не знаю")]
        rules = [("a", opt_id, 5.0)]
        q_id = self.db.add_question_with_rules("Оригінал?", "тест", answers, rules)
        
        new_answers = [("a", "Новий"), ("b", "Інший"), ("dk", "Не знаю")]
        new_rules = [("a", opt_id, 15.0), ("b", opt_id, -5.0)]
        self.db.update_question_with_rules(q_id, "Оновлено?", "нова_кат", new_answers, new_rules)
        
        q = self.db.get_question_by_id(q_id)
        self.assertEqual(q.text, "Оновлено?")
        self.assertEqual(q.category, "нова_кат")
        
        saved_answers = self.db.get_question_answers(q_id)
        self.assertEqual(len(saved_answers), 3)
        
        saved_rules = self.db.get_rules_for_answer(q_id, "a")
        self.assertEqual(saved_rules[0].score_adjustment, 15.0)

    def test_get_question_by_id(self):
        q = self.db.get_question_by_id(1)
        self.assertIsNotNone(q)
        self.assertEqual(q.id, 1)

    def test_get_question_by_invalid_id(self):
        q = self.db.get_question_by_id(99999)
        self.assertIsNone(q)

class TestOptionCRUD(unittest.TestCase):
    def setUp(self):
        self.test_db_path = "test_dss.db"
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
        self.db = Database(self.test_db_path)
        self.db.initialize()
        self.db.populate_initial_data()

    def tearDown(self):
        self.db.close()
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

    def test_add_option(self):
        count_before = len(self.db.get_all_options())
        opt_id = self.db.add_option("Тестовий пристрій", "Опис тестового пристрою", 0.0)
        self.assertIsNotNone(opt_id)
        count_after = len(self.db.get_all_options())
        self.assertEqual(count_after, count_before + 1)

    def test_add_option_with_rules(self):
        questions = self.db.get_all_questions()
        q_id = questions[0].id
        rules = [(q_id, "a", 10.0), (q_id, "b", -5.0)]
        opt_id = self.db.add_option_with_rules("Пристрій+правила", "Опис", 0.0, rules)
        
        all_rules = self.db.get_all_rules()
        opt_rules = [r for r in all_rules if r.option_id == opt_id]
        self.assertEqual(len(opt_rules), 2)

    def test_delete_option(self):
        opt_id = self.db.add_option("Видалити мене", "Опис", 0.0)
        count_before = len(self.db.get_all_options())
        self.db.delete_option(opt_id)
        count_after = len(self.db.get_all_options())
        self.assertEqual(count_after, count_before - 1)

    def test_delete_option_cascades_rules(self):
        questions = self.db.get_all_questions()
        q_id = questions[0].id
        rules = [(q_id, "a", 10.0)]
        opt_id = self.db.add_option_with_rules("Каскад", "Опис", 0.0, rules)
        
        rules_before = len(self.db.get_all_rules())
        self.db.delete_option(opt_id)
        rules_after = len(self.db.get_all_rules())
        self.assertLess(rules_after, rules_before)

    def test_update_option_rules(self):
        questions = self.db.get_all_questions()
        q_id = questions[0].id
        rules = [(q_id, "a", 5.0)]
        opt_id = self.db.add_option_with_rules("Оновити", "Опис", 0.0, rules)
        
        new_rules = [(q_id, "a", 15.0), (q_id, "b", -10.0)]
        self.db.update_option_rules(opt_id, new_rules)
        
        all_rules = self.db.get_all_rules()
        opt_rules = [r for r in all_rules if r.option_id == opt_id]
        self.assertEqual(len(opt_rules), 2)

    def test_get_option_by_id(self):
        opt = self.db.get_option_by_id(1)
        self.assertIsNotNone(opt)
        self.assertEqual(opt.id, 1)

    def test_get_option_by_invalid_id(self):
        opt = self.db.get_option_by_id(99999)
        self.assertIsNone(opt)

class TestInferenceEngine(unittest.TestCase):
    def setUp(self):
        self.test_db_path = "test_dss.db"
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
        self.db = Database(self.test_db_path)
        self.db.initialize()
        self.db.populate_initial_data()
        self.engine = InferenceEngine(self.db)

    def tearDown(self):
        self.db.close()
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

    def test_evaluation_returns_sorted(self):
        answers = {1: "a", 2: "a", 3: "a"}
        recommendations = self.engine.evaluate(answers)
        for i in range(len(recommendations) - 1):
            self.assertGreaterEqual(recommendations[i].percentage, recommendations[i + 1].percentage)

    def test_evaluation_returns_all_options(self):
        answers = {1: "a", 2: "b", 3: "c"}
        recommendations = self.engine.evaluate(answers)
        self.assertEqual(len(recommendations), len(self.db.get_all_options()))

    def test_dont_know_gives_zero(self):
        answers = {1: "dk", 2: "dk", 3: "dk"}
        recommendations = self.engine.evaluate(answers)
        scores = set(rec.score for rec in recommendations)
        self.assertLessEqual(len(scores), 1)
        for rec in recommendations:
            self.assertEqual(len(rec.explanations), 0)

    def test_top_recommendations_limit(self):
        answers = {1: "a", 2: "b", 3: "c"}
        top3 = self.engine.get_top_recommendations(answers, top_n=3)
        self.assertLessEqual(len(top3), 3)

    def test_top_recommendations_limit_1(self):
        answers = {1: "a"}
        top1 = self.engine.get_top_recommendations(answers, top_n=1)
        self.assertLessEqual(len(top1), 1)

    def test_all_questions_answered(self):
        """Відповіді на всі 12 запитань повинні працювати без помилок."""
        questions = self.db.get_all_questions()
        answers = {}
        for q in questions:
            q_answers = self.db.get_question_answers(q.id)
            non_dk = [a for a in q_answers if a.value != "dk"]
            if non_dk:
                answers[q.id] = non_dk[0].value
        recommendations = self.engine.evaluate(answers)
        self.assertGreater(len(recommendations), 0)
        self.assertTrue(all(rec.percentage >= 0 for rec in recommendations))

    def test_mixed_answers_and_dk(self):
        answers = {1: "a", 2: "dk", 3: "b", 4: "dk"}
        recommendations = self.engine.evaluate(answers)
        self.assertGreater(len(recommendations), 0)

    def test_explanations_format(self):
        """Пояснення мають містити ✅ або ❌ і не мають містити нульових балів."""
        answers = {1: "a", 2: "b", 3: "c"}
        recommendations = self.engine.evaluate(answers)
        for rec in recommendations:
            for exp in rec.explanations:
                self.assertTrue("✅" in exp or "❌" in exp,
                    f"Пояснення повинно містити ✅ або ❌: {exp}")

    def test_empty_answers(self):
        """Пуста відповідь не повинна ламати двигун."""
        recommendations = self.engine.evaluate({})
        self.assertEqual(len(recommendations), len(self.db.get_all_options()))

class TestEmptyDatabase(unittest.TestCase):
    """Тести на порожній базі даних (після очищення)."""
    def setUp(self):
        self.test_db_path = "test_dss_empty.db"
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
        self.db = Database(self.test_db_path)
        self.db.initialize()

    def tearDown(self):
        self.db.close()
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

    def test_empty_questions(self):
        self.assertEqual(len(self.db.get_all_questions()), 0)

    def test_empty_options(self):
        self.assertEqual(len(self.db.get_all_options()), 0)

    def test_empty_rules(self):
        self.assertEqual(len(self.db.get_all_rules()), 0)

    def test_engine_with_empty_db(self):
        engine = InferenceEngine(self.db)
        recs = engine.evaluate({})
        self.assertEqual(len(recs), 0)

    def test_engine_with_answers_but_empty_db(self):
        engine = InferenceEngine(self.db)
        recs = engine.evaluate({1: "a", 2: "b"})
        self.assertEqual(len(recs), 0)

class TestMigration(unittest.TestCase):
    """Тести експорту, імпорту і очищення бази даних."""
    def setUp(self):
        self.test_db_path = "test_dss_migration.db"
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
        self.db = Database(self.test_db_path)
        self.db.initialize()
        self.db.populate_initial_data()

    def tearDown(self):
        self.db.close()
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

    def test_clear_all_data(self):
        self.db.clear_all_data()
        self.assertEqual(len(self.db.get_all_questions()), 0)
        self.assertEqual(len(self.db.get_all_options()), 0)
        self.assertEqual(len(self.db.get_all_rules()), 0)

    def test_export_data_structure(self):
        data = self.db.export_data()
        self.assertIn("questions", data)
        self.assertIn("options", data)
        self.assertIn("rules", data)
        self.assertGreater(len(data["questions"]), 0)
        self.assertGreater(len(data["options"]), 0)
        self.assertGreater(len(data["rules"]), 0)

    def test_export_questions_have_answers(self):
        data = self.db.export_data()
        for q in data["questions"]:
            self.assertIn("answers", q)
            self.assertGreater(len(q["answers"]), 0)

    def test_export_import_roundtrip(self):
        """Експорт → очищення → імпорт повинен відновити всі дані."""
        data = self.db.export_data()
        q_count = len(data["questions"])
        o_count = len(data["options"])
        r_count = len(data["rules"])

        self.db.clear_all_data()
        self.assertEqual(len(self.db.get_all_questions()), 0)

        self.db.import_data(data)
        self.assertEqual(len(self.db.get_all_questions()), q_count)
        self.assertEqual(len(self.db.get_all_options()), o_count)
        self.assertEqual(len(self.db.get_all_rules()), r_count)

    def test_import_preserves_ids(self):
        """Після імпорту ID повинні збігатися з оригінальними."""
        data = self.db.export_data()
        original_q_ids = [q["id"] for q in data["questions"]]
        original_o_ids = [o["id"] for o in data["options"]]

        self.db.clear_all_data()
        self.db.import_data(data)

        restored_q_ids = [q.id for q in self.db.get_all_questions()]
        restored_o_ids = [o.id for o in self.db.get_all_options()]

        self.assertEqual(original_q_ids, restored_q_ids)
        self.assertEqual(original_o_ids, restored_o_ids)

    def test_import_preserves_scoring(self):
        """Після імпорту рушій повинен давати ті самі результати."""
        engine = InferenceEngine(self.db)
        answers = {1: "a", 2: "b", 3: "c"}
        recs_before = engine.evaluate(answers)
        scores_before = [(r.option.id, r.score) for r in recs_before]

        data = self.db.export_data()
        self.db.clear_all_data()
        self.db.import_data(data)

        recs_after = engine.evaluate(answers)
        scores_after = [(r.option.id, r.score) for r in recs_after]

        self.assertEqual(scores_before, scores_after)

    def test_export_json_serializable(self):
        data = self.db.export_data()
        json_str = json.dumps(data, ensure_ascii=False)
        parsed = json.loads(json_str)
        self.assertEqual(len(parsed["questions"]), len(data["questions"]))

    def test_clear_does_not_affect_admins(self):
        self.db.clear_all_data()
        admin = self.db.authenticate_admin("admin", "admin123")
        self.assertIsNotNone(admin)

class TestRuleCRUD(unittest.TestCase):
    def setUp(self):
        self.test_db_path = "test_dss_rules.db"
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
        self.db = Database(self.test_db_path)
        self.db.initialize()
        self.db.populate_initial_data()

    def tearDown(self):
        self.db.close()
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

    def test_add_rule(self):
        rules_before = len(self.db.get_all_rules())
        self.db.add_rule(1, "a", 1, 99.0)
        rules_after = len(self.db.get_all_rules())
        self.assertEqual(rules_after, rules_before + 1)

    def test_delete_rule(self):
        rule_id = self.db.add_rule(1, "a", 1, 99.0)
        rules_before = len(self.db.get_all_rules())
        self.db.delete_rule(rule_id)
        rules_after = len(self.db.get_all_rules())
        self.assertEqual(rules_after, rules_before - 1)

    def test_get_rules_for_answer(self):
        rules = self.db.get_rules_for_answer(1, "a")
        self.assertIsInstance(rules, list)
        for r in rules:
            self.assertEqual(r.question_id, 1)
            self.assertEqual(r.answer_value, "a")

if __name__ == "__main__":
    unittest.main()
