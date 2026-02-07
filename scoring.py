"""Score tracking and high score leaderboard."""

import json
from datetime import datetime
from pathlib import Path

SCORES_FILE = Path(__file__).parent / "data" / "scores.json"
HISTORY_FILE = Path(__file__).parent / "data" / "history.json"

DIFFICULTY_MULTIPLIER = {"easy": 1, "medium": 2, "hard": 3}


class ScoreTracker:
    """Tracks score during a single game session with streak bonuses."""

    def __init__(self):
        self.correct = 0
        self.total = 0
        self.points = 0
        self.streak = 0
        self.best_streak = 0

    def record(self, is_correct: bool, difficulty: str = "medium") -> dict:
        """Record an answer and return scoring details."""
        self.total += 1
        details = {"streak_bonus": 0, "difficulty_bonus": 0, "points_earned": 0}

        if is_correct:
            self.correct += 1
            self.streak += 1
            if self.streak > self.best_streak:
                self.best_streak = self.streak

            base = 10
            diff_mult = DIFFICULTY_MULTIPLIER.get(difficulty, 1)
            diff_bonus = base * (diff_mult - 1)
            streak_bonus = min(self.streak - 1, 5) * 5  # max +25 streak bonus

            earned = base + diff_bonus + streak_bonus
            self.points += earned

            details["difficulty_bonus"] = diff_bonus
            details["streak_bonus"] = streak_bonus
            details["points_earned"] = earned
        else:
            self.streak = 0

        return details

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


def save_high_score(name: str, score: int, total: int, category: str,
                    points: int = 0, best_streak: int = 0):
    """Save a new high score entry."""
    scores = load_high_scores()
    scores.append({
        "name": name,
        "score": score,
        "total": total,
        "percentage": round((score / total) * 100, 1) if total else 0,
        "points": points,
        "best_streak": best_streak,
        "category": category,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
    })
    # Keep top 10 by points (then percentage as tiebreaker)
    scores.sort(key=lambda s: (s.get("points", 0), s["percentage"]), reverse=True)
    scores = scores[:10]
    SCORES_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(SCORES_FILE, "w", encoding="utf-8") as f:
        json.dump(scores, f, indent=2)


def get_top_scores(n: int = 5) -> list[dict]:
    """Return top n scores."""
    return load_high_scores()[:n]


def save_game_history(name: str, score: int, total: int, category: str,
                      points: int = 0, best_streak: int = 0):
    """Save a game to the history log (keeps all games)."""
    history = load_game_history()
    history.append({
        "name": name,
        "score": score,
        "total": total,
        "percentage": round((score / total) * 100, 1) if total else 0,
        "points": points,
        "best_streak": best_streak,
        "category": category,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
    })
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)


def load_game_history() -> list[dict]:
    """Load full game history from file."""
    if not HISTORY_FILE.exists():
        return []
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
