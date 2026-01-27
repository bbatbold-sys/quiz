"""Quiz Master - Main game loop and user interface."""

from display import banner, print_menu, get_input, print_header


def main():
    """Main menu loop."""
    banner()
    options = ["Start Quiz", "View High Scores", "Quit"]

    while True:
        print_header("Main Menu")
        print_menu(options)
        choice = get_input("Choose an option:")

        if choice == "1":
            print("\n  [Quiz not yet implemented]\n")
        elif choice == "2":
            print("\n  [High scores not yet implemented]\n")
        elif choice == "3":
            print("\n  Thanks for playing! Goodbye.\n")
            break
        else:
            print("\n  Invalid choice. Try again.\n")


if __name__ == "__main__":
    main()
