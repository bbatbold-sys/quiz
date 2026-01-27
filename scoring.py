"""Score tracking and high score leaderboard."""

import json
from datetime import datetime
from pathlib import Path

SCORES_FILE = Path(__file__).parent / "data" / "scores.json"


class ScoreTracker:
    """Tracks score during a single game session."""

    def __init__(self):
        self.correct = 0
        self.total = 0

    def record(self, is_correct: bool):
        self.total += 1
        if is_correct:
            self.correct += 1

    @property
    def percentage(self) -> float:
        if self.total == 0:
            return 0.0
        return (self.correct / self.total) * 100


def load_high_scores() -> list[dict]:
    """Load high scores from file."""
    if not SCORES_FILE.exists():
        return []
    with open(SCORES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_high_score(name: str, score: int, total: int, category: str):
    """Save a new high score entry."""
    scores = load_high_scores()
    scores.append({
        "name": name,
        "score": score,
        "total": total,
        "percentage": round((score / total) * 100, 1) if total else 0,
        "category": category,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
    })
    # Keep top 10 by percentage
    scores.sort(key=lambda s: s["percentage"], reverse=True)
    scores = scores[:10]
    SCORES_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(SCORES_FILE, "w", encoding="utf-8") as f:
        json.dump(scores, f, indent=2)


def get_top_scores(n: int = 5) -> list[dict]:
    """Return top n scores."""
    return load_high_scores()[:n]
