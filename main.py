"""Quiz Master - Main game loop and user interface."""

import time
from display import (
    banner, print_menu, get_input, print_header, print_correct, print_wrong,
    _print, clear_screen, print_box, print_question_box, print_choices,
    print_score_bar, print_results, print_countdown, print_loading,
    print_welcome_animation, CYAN, RESET, BOLD, YELLOW, GREEN, RED, MAGENTA, WHITE, DIM
)
from questions import (
    load_questions, get_categories, get_difficulties,
    filter_questions, pick_questions
)
from scoring import ScoreTracker, save_high_score, get_top_scores
from challenges import (
    create_challenge, get_challenge, record_attempt,
    get_challenge_leaderboard
)


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


def play_challenge():
    """Accept and play a challenge from a friend."""
    clear_screen()
    print_header("ACCEPT CHALLENGE")

    code = get_input("Enter challenge code (6 characters):").strip().upper()

    if len(code) != 6:
        _print(f"\n    {RED}Invalid code format. Must be 6 characters.{RESET}")
        time.sleep(1.5)
        return

    challenge = get_challenge(code)
    if not challenge:
        _print(f"\n    {RED}Challenge not found. Check the code and try again.{RESET}")
        time.sleep(1.5)
        return

    # Show challenge info
    clear_screen()
    print_header("CHALLENGE FOUND!")
    _print(f"\n    {BOLD}Creator:{RESET} {CYAN}{challenge['creator']}{RESET}")
    _print(f"    {BOLD}Category:{RESET} {challenge['category']}")
    _print(f"    {BOLD}Difficulty:{RESET} {challenge['difficulty'].capitalize()}")
    _print(f"    {BOLD}Questions:{RESET} {challenge['total']}")
    _print(f"    {BOLD}Score to beat:{RESET} {YELLOW}{challenge['creator_points']} points{RESET}")
    _print(f"\n    {DIM}Can you beat {challenge['creator']}'s score?{RESET}\n")

    confirm = get_input("Accept this challenge? (y/n):").strip().lower()
    if confirm != 'y':
        return

    player_name = get_input("Enter your name:").strip() or "Challenger"

    # Load and get the specific questions
    all_questions = load_questions()
    selected = [all_questions[i] for i in challenge['questions'] if i < len(all_questions)]

    if not selected:
        _print(f"\n    {RED}Error loading challenge questions.{RESET}")
        time.sleep(1.5)
        return

    tracker = ScoreTracker()

    # Countdown
    clear_screen()
    _print(f"\n    {BOLD}Challenge from:{RESET} {CYAN}{challenge['creator']}{RESET}")
    _print(f"    {BOLD}Beat their score:{RESET} {YELLOW}{challenge['creator_points']} points{RESET}")
    print_countdown(3)

    # Quiz loop
    for i, q in enumerate(selected, 1):
        clear_screen()
        _print(f"\n    {MAGENTA}{BOLD}CHALLENGE MODE{RESET} - Beat {challenge['creator_points']} pts!\n")
        print_question_box(i, len(selected), q.text, q.difficulty)
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

        if i < len(selected):
            get_input("Press ENTER for next question...")

    # Results
    print_results(tracker.correct, tracker.total, tracker.points,
                  tracker.best_streak, tracker.percentage)

    # Compare with creator
    if tracker.points > challenge['creator_points']:
        _print(f"\n    {GREEN}{BOLD}YOU WON! You beat {challenge['creator']}!{RESET}")
        _print(f"    Your points: {tracker.points} vs Their points: {challenge['creator_points']}")
    elif tracker.points == challenge['creator_points']:
        _print(f"\n    {YELLOW}{BOLD}IT'S A TIE!{RESET}")
    else:
        _print(f"\n    {RED}You lost! {challenge['creator']} wins this time.{RESET}")
        _print(f"    Your points: {tracker.points} vs Their points: {challenge['creator_points']}")

    # Record attempt
    record_attempt(code, player_name, tracker.correct, tracker.points)

    # Show leaderboard
    _print(f"\n    {CYAN}{BOLD}Challenge Leaderboard:{RESET}")
    leaderboard = get_challenge_leaderboard(code)
    for i, entry in enumerate(leaderboard[:5], 1):
        _print(f"    {i}. {entry['player']}: {entry['points']} pts")

    get_input("\nPress ENTER to continue...")


def create_quiz_challenge():
    """Create a challenge after completing a quiz."""
    clear_screen()
    print_header("CREATE CHALLENGE")
    _print(f"    {CYAN}Play a quiz and create a challenge for friends!{RESET}")
    _print(f"    {CYAN}They'll get the same questions and try to beat your score.{RESET}\n")

    creator_name = get_input("Enter your name:").strip() or "Anonymous"

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
        _print(f"\n    {RED}No questions match your filters.{RESET}")
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

    # Get indices for challenge
    all_q_list = list(questions)
    question_indices = []
    for q in selected:
        for idx, orig_q in enumerate(all_q_list):
            if q.text == orig_q.text:
                question_indices.append(idx)
                break

    tracker = ScoreTracker()
    cat_label = category or "All Categories"

    # Countdown
    clear_screen()
    _print(f"\n    {BOLD}Creating challenge as:{RESET} {CYAN}{creator_name}{RESET}")
    _print(f"    {BOLD}Category:{RESET} {cat_label}")
    _print(f"    {BOLD}Difficulty:{RESET} {difficulty.capitalize()}")
    print_countdown(3)

    # Quiz loop
    for i, q in enumerate(selected, 1):
        clear_screen()
        print_question_box(i, len(selected), q.text, q.difficulty)
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

        if i < len(selected):
            get_input("Press ENTER for next question...")

    # Results
    print_results(tracker.correct, tracker.total, tracker.points,
                  tracker.best_streak, tracker.percentage)

    # Create challenge
    code = create_challenge(
        creator_name=creator_name,
        category=cat_label,
        difficulty=difficulty,
        question_indices=question_indices,
        score=tracker.correct,
        points=tracker.points,
        total=tracker.total
    )

    _print(f"""
    {GREEN}{BOLD}CHALLENGE CREATED!{RESET}

    {YELLOW}{BOLD}Share this code with your friends:{RESET}

    +==================+
    |   {CYAN}{BOLD}   {code}   {RESET}    |
    +==================+

    They can enter this code to play your challenge
    and try to beat your score of {YELLOW}{tracker.points} points{RESET}!
""")

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
        f"{MAGENTA}Challenge{RESET}       - Create a challenge for friends",
        f"{CYAN}Accept Challenge{RESET} - Play a friend's challenge",
        f"{YELLOW}Leaderboard{RESET}     - View top scores",
        f"{WHITE}Statistics{RESET}      - Your performance stats",
        f"{DIM}How to Play{RESET}     - Game instructions",
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
            create_quiz_challenge()
        elif choice == "4":
            play_challenge()
        elif choice == "5":
            show_high_scores()
        elif choice == "6":
            show_stats()
        elif choice == "7":
            show_help()
        elif choice == "8":
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
