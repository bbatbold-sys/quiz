"""Quiz Master - Main game loop and user interface."""

import time
from display import (banner, print_menu, get_input, print_header,
                     print_correct, print_wrong, print_score, _print,
                     CYAN, RESET, BOLD, YELLOW, GREEN, RED, BLUE)
from questions import (load_questions, get_categories, get_difficulties,
                       filter_questions, pick_questions)
from scoring import ScoreTracker, save_high_score, get_top_scores


def get_choice(prompt: str, max_val: int, default: int | None = None) -> int:
    """Get a validated integer choice from 1 to max_val."""
    raw = get_input(prompt)
    try:
        val = int(raw)
        if 1 <= val <= max_val:
            return val
    except ValueError:
        pass
    if default is not None:
        return default
    return 1


def show_help():
    """Display help and game instructions."""
    print_header("How to Play")
    _print(f"  {BOLD}Quiz Master{RESET} tests your knowledge across multiple categories.\n")
    _print(f"  {YELLOW}1.{RESET} Choose a category (or play all)")
    _print(f"  {YELLOW}2.{RESET} Select a difficulty level")
    _print(f"  {YELLOW}3.{RESET} Pick how many questions you want")
    _print(f"  {YELLOW}4.{RESET} Answer by typing the option number")
    _print(f"  {YELLOW}5.{RESET} Your score is saved to the leaderboard\n")
    _print(f"  {BOLD}Timed Mode:{RESET} You have 15 seconds per question.")
    _print(f"  If time runs out, the question is marked wrong.\n")
    _print(f"  {BOLD}Categories:{RESET} Geography, Science, History, Literature,")
    _print(f"  Art, Technology\n")
    _print(f"  {BOLD}Difficulties:{RESET} Easy, Medium, Hard\n")


def show_stats():
    """Show overall statistics from saved scores."""
    scores = get_top_scores(100)
    print_header("Statistics")
    if not scores:
        _print("  No games played yet.\n")
        return
    total_games = len(scores)
    avg_pct = sum(s["percentage"] for s in scores) / total_games
    best = scores[0]
    _print(f"  {BOLD}Total games recorded:{RESET} {total_games}")
    _print(f"  {BOLD}Average score:{RESET}        {avg_pct:.1f}%")
    _print(f"  {BOLD}Best score:{RESET}           {best['name']} - {best['percentage']}%")
    _print(f"  {BOLD}Best category:{RESET}        {best['category']}\n")


def play_quiz(timed: bool = False):
    """Run a single quiz session."""
    questions = load_questions()

    # Choose category
    categories = get_categories(questions)
    print_header("Choose Category")
    all_options = ["All Categories"] + categories
    print_menu(all_options)
    cat_idx = get_choice("Category number:", len(all_options), default=1)
    category = None if cat_idx == 1 else categories[cat_idx - 2]

    # Choose difficulty
    difficulties = get_difficulties()
    print_header("Choose Difficulty")
    diff_options = ["All Difficulties"] + [d.capitalize() for d in difficulties]
    print_menu(diff_options)
    diff_idx = get_choice("Difficulty number:", len(diff_options), default=1)
    difficulty = None if diff_idx == 1 else difficulties[diff_idx - 2]

    # Filter and pick questions
    pool = filter_questions(questions, category, difficulty)
    if not pool:
        _print("\n  No questions match your filters. Try again.\n")
        return

    # Ask how many questions
    print_header("How Many Questions?")
    default_count = min(5, len(pool))
    count = get_choice(f"Number (1-{len(pool)}, default {default_count}):",
                       len(pool), default=default_count)

    selected = pick_questions(pool, count)
    tracker = ScoreTracker()
    time_limit = 15 if timed else None

    # Quiz loop
    cat_label = category or "All"
    mode_label = " [TIMED]" if timed else ""
    print_header(f"Quiz: {cat_label} ({difficulty or 'all'} difficulty){mode_label}")

    if timed:
        _print(f"  {RED}{BOLD}You have {time_limit} seconds per question!{RESET}\n")

    for i, q in enumerate(selected, 1):
        _print(f"  {BOLD}Question {i}/{len(selected)}{RESET}")
        _print(f"  {CYAN}{q.text}{RESET}\n")
        print_menu(q.choices)

        if timed:
            start = time.time()
            choice_idx = get_choice("Your answer (number):", len(q.choices)) - 1
            elapsed = time.time() - start
            if elapsed > time_limit:
                _print(f"  {RED}Time's up! ({elapsed:.1f}s){RESET}")
                correct = False
            else:
                _print(f"  {BLUE}Answered in {elapsed:.1f}s{RESET}")
                correct = q.check(choice_idx)
        else:
            choice_idx = get_choice("Your answer (number):", len(q.choices)) - 1
            correct = q.check(choice_idx)

        tracker.record(correct)
        if correct:
            print_correct()
        else:
            print_wrong(q.correct_answer)
        print_score(tracker.correct, tracker.total)

    # Final results
    print_header("Results")
    _print(f"  {BOLD}Final Score: {tracker.correct}/{tracker.total} "
           f"({tracker.percentage:.0f}%){RESET}\n")

    # Save score
    name = get_input("Enter your name for the leaderboard:")
    if name.strip():
        save_high_score(name.strip(), tracker.correct, tracker.total, cat_label)
        _print(f"\n  {GREEN}Score saved!{RESET}\n")


def show_high_scores():
    """Display the leaderboard."""
    scores = get_top_scores(5)
    print_header("Leaderboard - Top 5")
    if not scores:
        _print("  No scores yet. Play a game first!\n")
        return
    _print(f"  {BOLD}{'#':<4}{'Name':<15}{'Score':<10}{'%':<8}{'Date':<16}{'Category'}{RESET}")
    _print(f"  {'-' * 65}")
    for i, s in enumerate(scores, 1):
        _print(f"  {YELLOW}{i:<4}{RESET}{s['name']:<15}"
               f"{s['score']}/{s['total']:<8}"
               f"{s['percentage']:<8}"
               f"{s['date']:<16}"
               f"{s['category']}")
    print()


def main():
    """Main menu loop."""
    banner()
    options = ["Start Quiz", "Timed Quiz", "View High Scores",
               "Statistics", "Help", "Quit"]

    while True:
        print_header("Main Menu")
        print_menu(options)
        choice = get_input("Choose an option:")

        if choice == "1":
            play_quiz()
        elif choice == "2":
            play_quiz(timed=True)
        elif choice == "3":
            show_high_scores()
        elif choice == "4":
            show_stats()
        elif choice == "5":
            show_help()
        elif choice == "6":
            _print("\n  Thanks for playing! Goodbye.\n")
            break
        else:
            _print("\n  Invalid choice. Try again.\n")


if __name__ == "__main__":
    main()
