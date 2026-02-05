"""Challenge system for Quiz Master - Create and share quiz challenges."""

import json
import random
import string
import hashlib
from datetime import datetime
from pathlib import Path

CHALLENGES_FILE = Path(__file__).parent / "data" / "challenges.json"


def generate_challenge_code() -> str:
    """Generate a unique 6-character challenge code."""
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choices(chars, k=6))


def load_challenges() -> dict:
    """Load challenges from file."""
    if not CHALLENGES_FILE.exists():
        return {}
    with open(CHALLENGES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_challenges(challenges: dict):
    """Save challenges to file."""
    CHALLENGES_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CHALLENGES_FILE, "w", encoding="utf-8") as f:
        json.dump(challenges, f, indent=2)


def create_challenge(creator_name: str, category: str, difficulty: str,
                     question_indices: list, score: int, points: int,
                     total: int) -> str:
    """
    Create a new challenge and return the challenge code.

    Args:
        creator_name: Name of the person creating the challenge
        category: Quiz category (or "All")
        difficulty: Difficulty level
        question_indices: List of question indices used
        score: Creator's number of correct answers
        points: Creator's total points
        total: Total number of questions

    Returns:
        The challenge code
    """
    challenges = load_challenges()

    # Generate unique code
    code = generate_challenge_code()
    while code in challenges:
        code = generate_challenge_code()

    challenges[code] = {
        "creator": creator_name,
        "category": category,
        "difficulty": difficulty,
        "questions": question_indices,
        "creator_score": score,
        "creator_points": points,
        "total": total,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "attempts": []
    }

    save_challenges(challenges)
    return code


def get_challenge(code: str) -> dict | None:
    """Get a challenge by its code. Returns None if not found."""
    challenges = load_challenges()
    return challenges.get(code.upper())


def record_attempt(code: str, player_name: str, score: int, points: int):
    """Record a player's attempt at a challenge."""
    challenges = load_challenges()
    code = code.upper()

    if code not in challenges:
        return False

    challenges[code]["attempts"].append({
        "player": player_name,
        "score": score,
        "points": points,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    })

    save_challenges(challenges)
    return True


def get_challenge_leaderboard(code: str) -> list:
    """Get the leaderboard for a challenge, sorted by points."""
    challenge = get_challenge(code)
    if not challenge:
        return []

    # Include creator
    leaderboard = [{
        "player": challenge["creator"] + " (Creator)",
        "score": challenge["creator_score"],
        "points": challenge["creator_points"]
    }]

    # Add attempts
    for attempt in challenge["attempts"]:
        leaderboard.append({
            "player": attempt["player"],
            "score": attempt["score"],
            "points": attempt["points"]
        })

    # Sort by points descending
    leaderboard.sort(key=lambda x: x["points"], reverse=True)
    return leaderboard


def get_my_challenges(player_name: str) -> list:
    """Get all challenges created by a player."""
    challenges = load_challenges()
    my_challenges = []

    for code, data in challenges.items():
        if data["creator"].lower() == player_name.lower():
            my_challenges.append({
                "code": code,
                "category": data["category"],
                "difficulty": data["difficulty"],
                "score": data["creator_score"],
                "total": data["total"],
                "attempts": len(data["attempts"]),
                "created": data["created"]
            })

    return my_challenges
