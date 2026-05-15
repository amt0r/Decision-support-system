from dataclasses import dataclass, field
from typing import List

@dataclass
class Question:
    id: int
    text: str
    category: str

@dataclass
class QuestionAnswer:
    id: int
    question_id: int
    value: str
    label: str

@dataclass
class Option:
    id: int
    text: str
    description: str
    base_score: float

@dataclass
class Rule:
    id: int
    question_id: int
    answer_value: str
    option_id: int
    score_adjustment: float

@dataclass
class Admin:
    id: int
    username: str
    password_hash: str

@dataclass
class Recommendation:
    option: Option
    score: float
    percentage: float
    explanations: List[str] = field(default_factory=list)
