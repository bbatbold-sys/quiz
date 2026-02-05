"""Quiz Master - Main game loop and user interface."""

import time
from display import (
    banner, print_menu, get_input, print_header, print_correct, print_wrong,
    _print, clear_screen, print_box, print_question_box, print_choices,
    print_score_bar, print_results, print_countdown, print_loading,
    print_welcome_animation, print_player_turn, print_multiplayer_results,
    CYAN, RESET, BOLD, YELLOW, GREEN, RED, MAGENTA, WHITE, DIM
)
from questions import (
    load_questions, get_categories, get_difficulties,
    filter_questions, pick_questions
)
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
    clear_screen()
    _print(f"""
{CYAN}{BOLD}
    ╔═══════════════════════════════════════════════════════╗
    ║                  HOW TO PLAY                          ║
    ╠═══════════════════════════════════════════════════════╣
{RESET}
    {BOLD}1.{RESET} Choose a category (or play all categories)
    {BOLD}2.{RESET} Select your difficulty level
    {BOLD}3.{RESET} Pick how many questions you want
    {BOLD}4.{RESET} Answer by typing the option number (1-4)
    {BOLD}5.{RESET} Your score is saved to the leaderboard

{CYAN}{BOLD}    ╠═══════════════════════════════════════════════════════╣
    ║                  SCORING SYSTEM                       ║
    ╠═══════════════════════════════════════════════════════╣{RESET}

    {GREEN}Base Points:{RESET}      10 points per correct answer
    {YELLOW}Difficulty Bonus:{RESET} Easy x1 | Medium x2 | Hard x3
    {RED}Streak Bonus:{RESET}     Up to +25 points for consecutive wins

{CYAN}{BOLD}    ╠═══════════════════════════════════════════════════════╣
    ║                  GAME MODES                           ║
    ╠═══════════════════════════════════════════════════════╣{RESET}

    {YELLOW}[1] Normal Mode:{RESET}  Take your time, no pressure
    {RED}[2] Timed Mode:{RESET}   15 seconds per question!

{CYAN}{BOLD}    ╠═══════════════════════════════════════════════════════╣
    ║                  CATEGORIES                           ║
    ╠═══════════════════════════════════════════════════════╣{RESET}

    {MAGENTA}Geography{RESET} | {CYAN}Science{RESET} | {YELLOW}History{RESET}
    {GREEN}Literature{RESET} | {RED}Art{RESET} | {BOLD}Technology{RESET}

{CYAN}{BOLD}    ╚═══════════════════════════════════════════════════════╝{RESET}
""")
    get_input("Press ENTER to go back...")


def show_stats():
    """Show overall statistics from saved scores."""
    clear_screen()
    scores = get_top_scores(100)

    if not scores:
        print_header("STATISTICS")
        _print(f"    {DIM}No games played yet. Start playing to see stats!{RESET}\n")
        get_input("Press ENTER to go back...")
        return

    total_games = len(scores)
    avg_pct = sum(s["percentage"] for s in scores) / total_games
    best = scores[0]
    total_points = sum(s.get("points", 0) for s in scores)

    _print(f"""
{CYAN}{BOLD}
    ╔═══════════════════════════════════════════════════════╗
    ║                   YOUR STATISTICS                     ║
    ╠═══════════════════════════════════════════════════════╣{RESET}

    {BOLD}Total Games Played:{RESET}    {CYAN}{total_games}{RESET}

    {BOLD}Total Points Earned:{RESET}   {YELLOW}{total_points}{RESET}

    {BOLD}Average Score:{RESET}         {GREEN}{avg_pct:.1f}%{RESET}

    {BOLD}Best Performance:{RESET}      {best['name']} - {best['percentage']}%

    {BOLD}Top Category:{RESET}          {best['category']}

{CYAN}{BOLD}    ╚═══════════════════════════════════════════════════════╝{RESET}
""")
    get_input("Press ENTER to go back...")


def play_quiz(timed: bool = False):
    """Run a single quiz session."""
    clear_screen()
    print_loading("Loading questions", 0.5)

    questions = load_questions()

    # Choose category
    categories = get_categories(questions)
    print_header("SELECT CATEGORY")
    all_options = ["All Categories"] + categories
    print_menu(all_options)
    cat_idx = get_choice("Enter your choice:", len(all_options), default=1)
    category = None if cat_idx == 1 else categories[cat_idx - 2]

    # Choose difficulty
    clear_screen()
    print_header("SELECT DIFFICULTY")
    difficulties = get_difficulties()
    diff_display = [
        f"{GREEN}Easy{RESET}    - Warm up your brain",
        f"{YELLOW}Medium{RESET}  - A fair challenge",
        f"{RED}Hard{RESET}    - For true masters"
    ]
    for i, d in enumerate(diff_display, 1):
        _print(f"      {YELLOW}{BOLD}[{i}]{RESET} {d}")
    print()
    diff_idx = get_choice("Enter your choice:", 3, default=1)
    difficulty = difficulties[diff_idx - 1]

    # Filter and pick questions
    pool = filter_questions(questions, category, difficulty)
    if not pool:
        _print(f"\n    {RED}No questions match your filters. Try again.{RESET}\n")
        time.sleep(1.5)
        return

    # Ask how many questions
    clear_screen()
    print_header("HOW MANY QUESTIONS?")
    _print(f"    {DIM}Available: {len(pool)} questions{RESET}\n")
    default_count = min(10, len(pool))
    count = get_choice(f"Enter number (1-{len(pool)}, default {default_count}):",
                       len(pool), default=default_count)

    selected = pick_questions(pool, count)
    tracker = ScoreTracker()
    time_limit = 15 if timed else None

    # Countdown
    clear_screen()
    cat_label = category or "All Categories"
    _print(f"\n    {BOLD}Category:{RESET} {CYAN}{cat_label}{RESET}")
    _print(f"    {BOLD}Difficulty:{RESET} {YELLOW}{difficulty.capitalize()}{RESET}")
    _print(f"    {BOLD}Questions:{RESET} {GREEN}{count}{RESET}")
    if timed:
        _print(f"    {BOLD}Mode:{RESET} {RED}TIMED (15s per question){RESET}")
    print_countdown(3)

    # Quiz loop
    for i, q in enumerate(selected, 1):
        clear_screen()
        print_question_box(i, len(selected), q.text, q.difficulty)
        print_choices(q.choices)

        if timed:
            _print(f"    {RED}{BOLD}>>> You have {time_limit} seconds! <<<{RESET}\n")
            start = time.time()
            choice_idx = get_choice("Your answer:", len(q.choices)) - 1
            elapsed = time.time() - start
            if elapsed > time_limit:
                _print(f"\n    {RED}{BOLD}TIME'S UP!{RESET} ({elapsed:.1f}s)")
                correct = False
            else:
                _print(f"\n    {DIM}Answered in {elapsed:.1f}s{RESET}")
                correct = q.check(choice_idx)
        else:
            choice_idx = get_choice("Your answer:", len(q.choices)) - 1
            correct = q.check(choice_idx)

        details = tracker.record(correct, q.difficulty)

        if correct:
            print_correct()
            bonus_parts = []
            if details["difficulty_bonus"]:
                bonus_parts.append(f"difficulty +{details['difficulty_bonus']}")
            if details["streak_bonus"]:
                bonus_parts.append(f"streak x{tracker.streak} +{details['streak_bonus']}")
            bonus_str = f" ({', '.join(bonus_parts)})" if bonus_parts else ""
            _print(f"    {GREEN}{BOLD}+{details['points_earned']} points{bonus_str}{RESET}")
        else:
            print_wrong(q.correct_answer)
            if tracker.best_streak > 0:
                _print(f"    {RED}Streak broken!{RESET}")

        print_score_bar(tracker.correct, tracker.total, tracker.points, tracker.streak)

        if i < len(selected):
            get_input("Press ENTER for next question...")

    # Final results
    print_results(tracker.correct, tracker.total, tracker.points,
                  tracker.best_streak, tracker.percentage)

    # Save score
    name = get_input("Enter your name for the leaderboard:")
    if name.strip():
        save_high_score(name.strip(), tracker.correct, tracker.total, cat_label,
                        tracker.points, tracker.best_streak)
        _print(f"\n    {GREEN}{BOLD}Score saved to leaderboard!{RESET}\n")
        time.sleep(1)


def run_player_quiz(player_name: str, player_num: int, questions: list,
                    difficulty: str) -> tuple:
    """Run a quiz for one player in multiplayer. Returns (correct, points, best_streak)."""
    tracker = ScoreTracker()

    clear_screen()
    print_player_turn(player_name, player_num)
    get_input("Press ENTER when ready...")
    print_countdown(3)

    for i, q in enumerate(questions, 1):
        clear_screen()
        _print(f"\n    {CYAN}{BOLD}Player {player_num}: {player_name}{RESET}\n")
        print_question_box(i, len(questions), q.text, q.difficulty)
        print_choices(q.choices)

        choice_idx = get_choice("Your answer:", len(q.choices)) - 1
        correct = q.check(choice_idx)
        details = tracker.record(correct, q.difficulty)

        if correct:
            print_correct()
            _print(f"    {GREEN}{BOLD}+{details['points_earned']} points{RESET}")
        else:
            print_wrong(q.correct_answer)

        print_score_bar(tracker.correct, tracker.total, tracker.points, tracker.streak)

        if i < len(questions):
            get_input("Press ENTER for next question...")

    return tracker.correct, tracker.points, tracker.best_streak


def play_multiplayer():
    """Run a 2-player multiplayer quiz session."""
    clear_screen()
    print_header("MULTIPLAYER MODE")
    _print(f"    {CYAN}Two players will answer the same questions.{RESET}")
    _print(f"    {CYAN}Player 1 goes first, then Player 2.{RESET}")
    _print(f"    {CYAN}Highest points wins!{RESET}\n")

    # Get player names
    p1_name = get_input("Enter Player 1 name:").strip() or "Player 1"
    p2_name = get_input("Enter Player 2 name:").strip() or "Player 2"

    print_loading("Loading questions", 0.5)
    questions = load_questions()

    # Choose category
    clear_screen()
    categories = get_categories(questions)
    print_header("SELECT CATEGORY")
    all_options = ["All Categories"] + categories
    print_menu(all_options)
    cat_idx = get_choice("Enter your choice:", len(all_options), default=1)
    category = None if cat_idx == 1 else categories[cat_idx - 2]

    # Choose difficulty
    clear_screen()
    print_header("SELECT DIFFICULTY")
    difficulties = get_difficulties()
    diff_display = [
        f"{GREEN}Easy{RESET}    - Warm up your brain",
        f"{YELLOW}Medium{RESET}  - A fair challenge",
        f"{RED}Hard{RESET}    - For true masters"
    ]
    for i, d in enumerate(diff_display, 1):
        _print(f"      {YELLOW}{BOLD}[{i}]{RESET} {d}")
    print()
    diff_idx = get_choice("Enter your choice:", 3, default=1)
    difficulty = difficulties[diff_idx - 1]

    # Filter and pick questions
    pool = filter_questions(questions, category, difficulty)
    if not pool:
        _print(f"\n    {RED}No questions match your filters. Try again.{RESET}\n")
        time.sleep(1.5)
        return

    # Ask how many questions
    clear_screen()
    print_header("HOW MANY QUESTIONS?")
    _print(f"    {DIM}Available: {len(pool)} questions{RESET}\n")
    default_count = min(10, len(pool))
    count = get_choice(f"Enter number (1-{len(pool)}, default {default_count}):",
                       len(pool), default=default_count)

    selected = pick_questions(pool, count)

    # Player 1's turn
    _print(f"\n    {YELLOW}{BOLD}Player 2 ({p2_name}): Please look away!{RESET}\n")
    time.sleep(2)
    p1_correct, p1_points, p1_streak = run_player_quiz(p1_name, 1, selected, difficulty)

    # Transition
    clear_screen()
    _print(f"\n    {GREEN}{BOLD}{p1_name} has finished!{RESET}")
    _print(f"\n    {YELLOW}{BOLD}Now it's {p2_name}'s turn.{RESET}")
    _print(f"\n    {YELLOW}{BOLD}Player 1 ({p1_name}): Please look away!{RESET}\n")
    get_input("Press ENTER when Player 2 is ready...")

    # Player 2's turn
    p2_correct, p2_points, p2_streak = run_player_quiz(p2_name, 2, selected, difficulty)

    # Show results
    print_multiplayer_results(p1_name, p1_correct, p1_points,
                              p2_name, p2_correct, p2_points, len(selected))

    get_input("Press ENTER to continue...")


def show_high_scores():
    """Display the leaderboard."""
    clear_screen()
    scores = get_top_scores(10)

    _print(f"""
{YELLOW}{BOLD}
    ╔═══════════════════════════════════════════════════════════════════╗
    ║                        LEADERBOARD                                ║
    ╠═══════════════════════════════════════════════════════════════════╣{RESET}
""")

    if not scores:
        _print(f"    {DIM}No scores yet. Be the first to play!{RESET}")
    else:
        _print(f"    {BOLD}{'#':<4}{'Name':<15}{'Score':<10}{'Points':<10}{'Streak':<10}{'Category'}{RESET}")
        _print(f"    {'-' * 63}")
        for i, s in enumerate(scores, 1):
            medal = ""
            if i == 1:
                medal = f"{YELLOW}🥇{RESET}"
            elif i == 2:
                medal = f"{WHITE}🥈{RESET}"
            elif i == 3:
                medal = f"{RED}🥉{RESET}"

            _print(f"    {medal}{CYAN}{i:<4}{RESET}"
                   f"{s['name']:<15}"
                   f"{s['score']}/{s['total']:<8}"
                   f"{YELLOW}{s.get('points', 0):<10}{RESET}"
                   f"{GREEN}{s.get('best_streak', 0):<10}{RESET}"
                   f"{s['category']}")

    _print(f"""
{YELLOW}{BOLD}
    ╚═══════════════════════════════════════════════════════════════════╝{RESET}
""")
    get_input("Press ENTER to go back...")


def main():
    """Main menu loop."""
    banner()
    print_welcome_animation()
    time.sleep(0.5)

    menu_options = [
        f"{GREEN}Start Quiz{RESET}      - Normal mode, take your time",
        f"{RED}Timed Quiz{RESET}      - 15 seconds per question!",
        f"{MAGENTA}Multiplayer{RESET}     - 2 Player Battle",
        f"{YELLOW}Leaderboard{RESET}     - View top scores",
        f"{CYAN}Statistics{RESET}      - Your performance stats",
        f"{WHITE}How to Play{RESET}     - Game instructions",
        f"{DIM}Quit{RESET}            - Exit the game"
    ]

    while True:
        clear_screen()
        banner()
        print_header("MAIN MENU")
        print_menu(menu_options)
        choice = get_input("Enter your choice:")

        if choice == "1":
            play_quiz()
        elif choice == "2":
            play_quiz(timed=True)
        elif choice == "3":
            play_multiplayer()
        elif choice == "4":
            show_high_scores()
        elif choice == "5":
            show_stats()
        elif choice == "6":
            show_help()
        elif choice == "7":
            clear_screen()
            _print(f"""
{CYAN}{BOLD}
    ╔═══════════════════════════════════════════════════════╗
    ║                                                       ║
    ║           Thanks for playing Quiz Master!             ║
    ║                                                       ║
    ║                    See you next time!                 ║
    ║                                                       ║
    ╚═══════════════════════════════════════════════════════╝
{RESET}
""")
            break
        else:
            _print(f"\n    {RED}Invalid choice. Please try again.{RESET}")
            time.sleep(1)


if __name__ == "__main__":
    main()
