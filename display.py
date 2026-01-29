"""Display helpers: formatting, colors, and ASCII art for the quiz game."""

import sys
import os
import time

# Enable ANSI on Windows
if os.name == "nt":
    os.system("")

# ANSI color codes
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
ITALIC = "\033[3m"
UNDERLINE = "\033[4m"
BLINK = "\033[5m"

# Foreground colors
BLACK = "\033[30m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"

# Background colors
BG_BLACK = "\033[40m"
BG_RED = "\033[41m"
BG_GREEN = "\033[42m"
BG_YELLOW = "\033[43m"
BG_BLUE = "\033[44m"
BG_MAGENTA = "\033[45m"
BG_CYAN = "\033[46m"
BG_WHITE = "\033[47m"


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def _print(text: str):
    """Print with utf-8 encoding support."""
    sys.stdout.buffer.write((text + "\n").encode("utf-8"))
    sys.stdout.flush()


def slow_print(text: str, delay: float = 0.02):
    """Print text character by character for effect."""
    for char in text:
        sys.stdout.buffer.write(char.encode("utf-8"))
        sys.stdout.flush()
        time.sleep(delay)
    print()


def banner():
    """Print the quiz game banner with ASCII art."""
    clear_screen()
    art = f"""
{CYAN}{BOLD}
    +==============================================================+
    |                                                              |
    |    {YELLOW}  ___  _   _ ___ _____   {MAGENTA}__  __    _    ____ _____ _____ ____  {CYAN} |
    |    {YELLOW} / _ \\| | | |_ _|__  /  {MAGENTA}|  \\/  |  / \\  / ___|_   _| ____|  _ \\ {CYAN} |
    |    {YELLOW}| | | | | | || |  / /   {MAGENTA}| |\\/| | / _ \\ \\___ \\ | | |  _| | |_) |{CYAN} |
    |    {YELLOW}| |_| | |_| || | / /_   {MAGENTA}| |  | |/ ___ \\ ___) || | | |___|  _ < {CYAN} |
    |    {YELLOW} \\__\\_\\\\___/|___/____|  {MAGENTA}|_|  |_/_/   \\_\\____/ |_| |_____|_| \\_\\{CYAN} |
    |                                                              |
    +==============================================================+
{RESET}
{DIM}                    Test Your Knowledge Across 6 Categories!{RESET}
{DIM}                       360 Questions | 3 Difficulty Levels{RESET}
"""
    _print(art)


def print_box(title: str, content: list[str] = None, width: int = 50):
    """Print content in a stylized box."""
    _print(f"\n{CYAN}    +{'=' * (width - 2)}+{RESET}")
    _print(f"{CYAN}    |{BOLD}{WHITE} {title.center(width - 4)} {RESET}{CYAN}|{RESET}")
    _print(f"{CYAN}    +{'-' * (width - 2)}+{RESET}")
    if content:
        for line in content:
            padding = width - 4 - len(line.replace(YELLOW, '').replace(RESET, '').replace(GREEN, '').replace(RED, '').replace(CYAN, '').replace(BOLD, '').replace(MAGENTA, ''))
            _print(f"{CYAN}    |{RESET} {line}{' ' * max(0, padding)} {CYAN}|{RESET}")
        _print(f"{CYAN}    +{'=' * (width - 2)}+{RESET}")
    print()


def print_menu(options: list[str], numbered: bool = True):
    """Print a styled numbered menu."""
    for i, option in enumerate(options, 1):
        if numbered:
            _print(f"      {YELLOW}{BOLD}[{i}]{RESET} {WHITE}{option}{RESET}")
        else:
            _print(f"      {CYAN}>{RESET} {WHITE}{option}{RESET}")
    print()


def print_question_box(question_num: int, total: int, text: str, difficulty: str):
    """Print a question in a styled box."""
    diff_color = {
        "easy": GREEN,
        "medium": YELLOW,
        "hard": RED
    }.get(difficulty, WHITE)

    _print(f"\n{MAGENTA}    {'*' * 56}{RESET}")
    _print(f"{MAGENTA}    *{RESET}  {BOLD}Question {question_num}/{total}{RESET}                    {diff_color}[{difficulty.upper()}]{RESET}  {MAGENTA}*{RESET}")
    _print(f"{MAGENTA}    {'*' * 56}{RESET}")
    _print(f"\n      {CYAN}{BOLD}{text}{RESET}\n")


def print_choices(choices: list[str]):
    """Print answer choices in a grid."""
    for i, choice in enumerate(choices):
        letter = chr(65 + i)  # A, B, C, D
        _print(f"        {YELLOW}{BOLD}[{i + 1}]{RESET} {letter}. {WHITE}{choice}{RESET}")
    print()


def print_correct():
    """Print correct answer feedback."""
    art = f"""
    {GREEN}{BOLD}
     ██████╗ ██████╗ ██████╗ ██████╗ ███████╗ ██████╗████████╗██╗
    ██╔════╝██╔═══██╗██╔══██╗██╔══██╗██╔════╝██╔════╝╚══██╔══╝██║
    ██║     ██║   ██║██████╔╝██████╔╝█████╗  ██║        ██║   ██║
    ██║     ██║   ██║██╔══██╗██╔══██╗██╔══╝  ██║        ██║   ╚═╝
    ╚██████╗╚██████╔╝██║  ██║██║  ██║███████╗╚██████╗   ██║   ██╗
     ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝   ╚═╝   ╚═╝
    {RESET}"""
    _print(art)


def print_wrong(correct_answer: str):
    """Print wrong answer feedback."""
    art = f"""
    {RED}{BOLD}
    ██╗    ██╗██████╗  ██████╗ ███╗   ██╗ ██████╗ ██╗
    ██║    ██║██╔══██╗██╔═══██╗████╗  ██║██╔════╝ ██║
    ██║ █╗ ██║██████╔╝██║   ██║██╔██╗ ██║██║  ███╗██║
    ██║███╗██║██╔══██╗██║   ██║██║╚██╗██║██║   ██║╚═╝
    ╚███╔███╔╝██║  ██║╚██████╔╝██║ ╚████║╚██████╔╝██╗
     ╚══╝╚══╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚═╝
    {RESET}
      {DIM}The correct answer was: {CYAN}{correct_answer}{RESET}
"""
    _print(art)


def print_score_bar(current: int, total: int, points: int, streak: int):
    """Print a visual score bar."""
    if total == 0:
        pct = 0
    else:
        pct = int((current / total) * 20)

    bar = f"{GREEN}{'█' * pct}{DIM}{'░' * (20 - pct)}{RESET}"
    streak_display = f"{YELLOW}🔥 x{streak}{RESET}" if streak > 1 else ""

    _print(f"\n    {BOLD}Score:{RESET} [{bar}] {current}/{total}  |  {BOLD}Points:{RESET} {CYAN}{points}{RESET}  {streak_display}\n")


def print_header(text: str):
    """Print a section header."""
    _print(f"\n{CYAN}    {'=' * 50}{RESET}")
    _print(f"    {BOLD}{WHITE}{text.center(50)}{RESET}")
    _print(f"{CYAN}    {'=' * 50}{RESET}\n")


def print_results(correct: int, total: int, points: int, streak: int, percentage: float):
    """Print final results with style."""
    clear_screen()

    if percentage >= 80:
        grade = f"{GREEN}{BOLD}EXCELLENT!{RESET}"
        stars = f"{YELLOW}★ ★ ★ ★ ★{RESET}"
    elif percentage >= 60:
        grade = f"{CYAN}{BOLD}GREAT JOB!{RESET}"
        stars = f"{YELLOW}★ ★ ★ ★{RESET} ☆"
    elif percentage >= 40:
        grade = f"{YELLOW}{BOLD}GOOD EFFORT!{RESET}"
        stars = f"{YELLOW}★ ★ ★{RESET} ☆ ☆"
    elif percentage >= 20:
        grade = f"{MAGENTA}{BOLD}KEEP TRYING!{RESET}"
        stars = f"{YELLOW}★ ★{RESET} ☆ ☆ ☆"
    else:
        grade = f"{RED}{BOLD}STUDY MORE!{RESET}"
        stars = f"{YELLOW}★{RESET} ☆ ☆ ☆ ☆"

    art = f"""
{CYAN}{BOLD}
    ╔═══════════════════════════════════════════════════════╗
    ║                                                       ║
    ║                   GAME OVER                           ║
    ║                                                       ║
    ╠═══════════════════════════════════════════════════════╣
    ║                                                       ║
    ║      {stars}                              ║
    ║                                                       ║
    ║      {grade}                                      ║
    ║                                                       ║
    ╠═══════════════════════════════════════════════════════╣
{RESET}
    {BOLD}          FINAL SCORE:{RESET} {GREEN}{correct}{RESET}/{total} ({percentage:.0f}%)

    {BOLD}          TOTAL POINTS:{RESET} {CYAN}{points}{RESET}

    {BOLD}          BEST STREAK:{RESET} {YELLOW}{streak}{RESET}
{CYAN}{BOLD}
    ╚═══════════════════════════════════════════════════════╝
{RESET}
"""
    _print(art)


def print_countdown(seconds: int = 3):
    """Print a countdown before starting."""
    for i in range(seconds, 0, -1):
        _print(f"\n{BOLD}    Starting in... {CYAN}{i}{RESET}")
        time.sleep(0.5)
        clear_screen()
    _print(f"\n{GREEN}{BOLD}    GO!{RESET}\n")
    time.sleep(0.3)


def print_timer_warning(seconds_left: int):
    """Print timer warning."""
    if seconds_left <= 5:
        _print(f"    {RED}{BOLD}>>> {seconds_left} seconds remaining! <<<{RESET}")


def get_input(prompt: str) -> str:
    """Get user input with colored prompt."""
    return input(f"    {YELLOW}{BOLD}>{RESET} {prompt} ")


def print_loading(text: str = "Loading", duration: float = 1.0):
    """Print a loading animation."""
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r    {CYAN}{frames[i % len(frames)]}{RESET} {text}...")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write(f"\r    {GREEN}✓{RESET} {text}... Done!\n")
    sys.stdout.flush()


def print_welcome_animation():
    """Print welcome animation."""
    frames = [
        "Q",
        "QU",
        "QUI",
        "QUIZ",
        "QUIZ ",
        "QUIZ M",
        "QUIZ MA",
        "QUIZ MAS",
        "QUIZ MAST",
        "QUIZ MASTE",
        "QUIZ MASTER",
        "QUIZ MASTER!",
    ]
    for frame in frames:
        sys.stdout.write(f"\r    {CYAN}{BOLD}>>> {frame} <<<{RESET}    ")
        sys.stdout.flush()
        time.sleep(0.1)
    print("\n")
