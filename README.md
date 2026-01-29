# Quiz Master

A terminal-based quiz game with multiple categories, difficulty levels, scoring system, and leaderboard.

## Features

- **6 Categories**: Geography, Science, History, Literature, Art, Technology
- **3 Difficulty Levels**: Easy, Medium, Hard
- **360 Questions**: 20 questions per category per difficulty
- **Points System**: Base points + difficulty multipliers + streak bonuses
- **Timed Mode**: 15 seconds per question
- **Leaderboard**: Top 10 scores saved locally
- **Statistics**: Track your overall performance
- **Colored Output**: ANSI colors for better visibility

## Project Structure

```
quiz_game/
├── main.py           # Game loop, menus, quiz flow
├── questions.py      # Question class, loading, filtering
├── scoring.py        # Points system, streaks, leaderboard
├── display.py        # Colored output, formatting helpers
└── data/
    └── questions.json  # 360 questions database
```

## How to Run

```bash
cd quiz_game
python main.py
```

## How to Play

1. Choose a category (or play all)
2. Select a difficulty level
3. Pick how many questions you want
4. Answer by typing the option number
5. Your score is saved to the leaderboard

## Scoring

- **Base**: 10 points per correct answer
- **Difficulty Bonus**: Easy x1, Medium x2, Hard x3
- **Streak Bonus**: Up to +25 points for consecutive correct answers

## Requirements

- Python 3.10+

## License

MIT
