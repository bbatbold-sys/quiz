"""Question bank: loading, categorizing, and serving quiz questions."""

import json
import random
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data" / "questions.json"


class Question:
    """Represents a single quiz question."""

    def __init__(self, text: str, choices: list[str], answer: int,
                 category: str = "General", difficulty: str = "medium"):
        self.text = text
        self.choices = choices
        self.answer = answer          # 0-based index into choices
        self.category = category
        self.difficulty = difficulty

    @property
    def correct_answer(self) -> str:
        return self.choices[self.answer]

    def check(self, choice_index: int) -> bool:
        return choice_index == self.answer


def load_questions() -> list[Question]:
    """Load questions from the JSON data file."""
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Question(**q) for q in data["questions"]]


def get_categories(questions: list[Question]) -> list[str]:
    """Return sorted list of unique categories."""
    return sorted({q.category for q in questions})


def get_difficulties() -> list[str]:
    return ["easy", "medium", "hard"]


def filter_questions(questions: list[Question],
                     category: str | None = None,
                     difficulty: str | None = None) -> list[Question]:
    """Filter questions by category and/or difficulty."""
    result = questions
    if category:
        result = [q for q in result if q.category == category]
    if difficulty:
        result = [q for q in result if q.difficulty == difficulty]
    return result


def pick_questions(questions: list[Question], count: int = 5) -> list[Question]:
    """Pick a random subset of questions."""
    count = min(count, len(questions))
    return random.sample(questions, count)
