"""Display helpers: formatting, colors, and ASCII art for the quiz game."""

import sys
import os

# Enable ANSI on Windows
if os.name == "nt":
    os.system("")

# ANSI color codes
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"


def _print(text: str):
    """Print with utf-8 encoding support."""
    sys.stdout.buffer.write((text + "\n").encode("utf-8"))
    sys.stdout.flush()


def banner():
    """Print the quiz game banner."""
    art = (
        f"{CYAN}{BOLD}"
        "+===================================+\n"
        "|       *  QUIZ MASTER  *           |\n"
        "|   Test your knowledge!            |\n"
        f"+===================================+{RESET}"
    )
    _print(art)


def print_menu(options: list[str]):
    """Print a numbered menu."""
    for i, option in enumerate(options, 1):
        _print(f"  {YELLOW}{i}.{RESET} {option}")
    print()


def print_correct():
    _print(f"\n  {GREEN}{BOLD}[OK] Correct!{RESET}\n")


def print_wrong(correct_answer: str):
    _print(f"\n  {RED}{BOLD}[X] Wrong!{RESET} The answer was: {CYAN}{correct_answer}{RESET}\n")


def print_score(current: int, total: int):
    _print(f"  {BLUE}Score: {current}/{total}{RESET}")


def print_header(text: str):
    width = len(text) + 4
    _print(f"\n{BOLD}  {'-' * width}")
    _print(f"  | {text} |")
    _print(f"  {'-' * width}{RESET}\n")


def get_input(prompt: str) -> str:
    """Get user input with colored prompt."""
    return input(f"  {YELLOW}> {prompt}{RESET} ")
