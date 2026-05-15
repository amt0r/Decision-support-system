from typing import Dict, List
from core.models import Question, QuestionAnswer, Option, Rule, Recommendation
from core.database import Database

class InferenceEngine:
    def __init__(self, db: Database):
        self._db = db

    def _calculate_absolute_max_scores(self, options: List[Option], questions: Dict[int, Question]) -> Dict[int, float]:
        max_scores = {opt.id: opt.base_score for opt in options}
        all_rules = self._db.get_all_rules()
        option_question_max_adj = {}
        for rule in all_rules:
            if rule.score_adjustment > 0:
                key = (rule.option_id, rule.question_id)
                current_max = option_question_max_adj.get(key, 0)
                if rule.score_adjustment > current_max:
                    option_question_max_adj[key] = rule.score_adjustment
        for (option_id, question_id), max_adj in option_question_max_adj.items():
            if option_id in max_scores and question_id in questions:
                max_scores[option_id] += max_adj
        for opt_id in max_scores:
            if max_scores[opt_id] <= 0:
                max_scores[opt_id] = 1.0
        return max_scores

    def evaluate(self, answers: Dict[int, str]) -> List[Recommendation]:
        options = self._db.get_all_options()
        questions = {q.id: q for q in self._db.get_all_questions()}
        scores = {opt.id: opt.base_score for opt in options}
        explanations: Dict[int, List[tuple]] = {opt.id: [] for opt in options}

        for question_id, answer_value in answers.items():
            if answer_value == "dk":
                continue

            question = questions.get(question_id)
            if not question:
                continue

            rules = self._db.get_rules_for_answer(question_id, answer_value)
            q_answers = self._db.get_question_answers(question_id)
            answer_label = ""
            for qa in q_answers:
                if qa.value == answer_value:
                    answer_label = qa.label
                    break

            for rule in rules:
                score_adj = rule.score_adjustment
                scores[rule.option_id] = scores.get(rule.option_id, 0) + score_adj
                if score_adj != 0:
                    explanations[rule.option_id].append((score_adj, question.category, answer_label))

        max_possible_scores = self._calculate_absolute_max_scores(options, questions)

        recommendations = []
        for opt in options:
            score = scores.get(opt.id, 0)
            max_score = max_possible_scores.get(opt.id, 1)
            
            if score <= 0:
                percentage = 0.0
            else:
                percentage = min(100.0, (score / max_score) * 100.0)
                
            opt_explanations = explanations.get(opt.id, [])
            opt_explanations.sort(key=lambda x: x[0], reverse=True)
            
            formatted_exps = []
            for score_adj, category, answer_label in opt_explanations:
                cat = category.capitalize()
                if score_adj > 0:
                    formatted_exps.append(f"✅ {cat}: {answer_label} (+{int(score_adj)} балів)")
                else:
                    formatted_exps.append(f"❌ {cat}: {answer_label} ({int(score_adj)} балів)")

            recommendations.append(Recommendation(
                option=opt,
                score=score,
                percentage=round(percentage, 1),
                explanations=formatted_exps
            ))

        recommendations.sort(key=lambda r: r.percentage, reverse=True)
        return recommendations

    def get_top_recommendations(self, answers: Dict[int, str], top_n: int = 3) -> List[Recommendation]:
        all_recs = self.evaluate(answers)
        positive = [r for r in all_recs if r.score > 0]
        return positive[:top_n]
