import platform
import sys
from dataclasses import dataclass
from enum import Enum

if platform.system() == "Windows":
    import msvcrt
else:
    import termios
    import tty


@dataclass
class Choice:
    value: str
    label: str | None = None
    meta: str | None = None


class Color(Enum):
    """ANSI color codes"""

    GREEN = "\033[32m"
    CYAN = "\033[36m"
    DIM = "\033[2m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


class Command(Enum):
    """ANSI terminal commands"""

    CLEAR_LINE = "\033[2K"
    MOVE_UP = "\033[F"
    CURSOR_UP = "\033[A"


def colored(text: str, color: Color) -> str:
    return f"{color.value}{text}{Color.RESET.value}"


def format_question(question: str, default: str | None = None) -> str:
    question = f"{colored('?', Color.GREEN)} {question}{Color.DIM.value}"
    if default:
        question += f" ({default})"
    question += f" > {Color.RESET.value}"
    return question


def format_answer(question: str, answer: str) -> str:
    return f"{colored('✓', Color.GREEN)} {question}{colored(' - ', Color.DIM)}{colored(answer, Color.GREEN)}"


def print_questions(choices: list[Choice], index):
    for i, choice in enumerate(choices):
        selected = i == index
        prefix = "> " if selected else "  "

        sys.stdout.write(Command.CLEAR_LINE.value)
        if selected:
            sys.stdout.write(
                colored(
                    prefix + (choice.label or choice.value.capitalize()), Color.GREEN
                )
            )
            if choice.meta:
                sys.stdout.write(colored(f" ({choice.meta})", Color.DIM))
        else:
            sys.stdout.write(f"{prefix}{choice.label or choice.value.capitalize()}")
        sys.stdout.write("\n")
    sys.stdout.flush()


def read_key_windows():
    """Read a single key press on Windows"""
    while True:
        if msvcrt.kbhit():
            ch = msvcrt.getch()

            # Handle special keys (arrow keys return two bytes)
            if ch in (b"\x00", b"\xe0"):
                ch2 = msvcrt.getch()
                if ch2 == b"H":
                    return "up"
                elif ch2 == b"P":
                    return "down"
            elif ch == b"\r":
                return "enter"
            elif ch == b"\x03":  # Ctrl-C
                return "ctrl-c"

            # Decode and return the character
            char = ch.decode("utf-8", errors="ignore")
            return char.lower() if char else None


def read_key_unix():
    """Read a single key press on Unix"""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)

        # Handle arrow keys (escape sequences)
        if ch == "\x1b":
            ch2 = sys.stdin.read(1)
            if ch2 == "[":
                ch3 = sys.stdin.read(1)
                if ch3 == "A":
                    return "up"
                elif ch3 == "B":
                    return "down"
        elif ch == "\r" or ch == "\n":
            return "enter"
        elif ch == "\x03":  # Ctrl-C
            return "ctrl-c"

        return ch.lower() if ch else None
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def read_key():
    """Read a single key press (OS-agnostic)"""
    if platform.system() == "Windows":
        return read_key_windows()
    else:
        return read_key_unix()


def ask(question: str, default: str | None = None) -> str:
    """
    Ask a question with a default value.
    Returns the user's answer or the default if empty.
    """
    prompt = format_question(question, default)
    answer = input(prompt).strip() or default

    assert answer is not None

    # Move cursor up one line and clear it
    sys.stdout.write(Command.MOVE_UP.value)
    sys.stdout.write(Command.CLEAR_LINE.value)

    # Print final result
    # We use print here because we want to end with \n
    print(format_answer(question, answer))

    return answer


def choose(question: str, default: bool = False) -> bool:
    """
    Ask a yes/no question.
    Returns True for yes, False for no.
    Press 'y' for yes, 'n' for no, or Enter for default.
    """
    suffix = " [Y/n]" if default else " [y/N]"
    prompt = format_question(question + colored(suffix, Color.DIM))

    # Print the prompt
    sys.stdout.write(prompt)
    sys.stdout.flush() # Write directly

    while True:
        key = read_key()
        if key == "y":
            result = True
            break
        elif key == "n":
            result = False
            break
        elif key == "enter":
            result = default
            break

    # Move cursor to beginning of the line and clear it
    sys.stdout.write("\r")
    sys.stdout.write(Command.CLEAR_LINE.value)

    # Print final result
    answer_text = "Yes" if result else "No"
    print(format_answer(question, answer_text))

    return result


def select(question: str, choices: list[Choice]):
    """
    Display an interactive selection menu.
    """
    index = 0
    prompt = format_question(question)

    def render():
        # Move cursor to start of menu
        sys.stdout.write(Command.MOVE_UP.value * (len(choices) + 1))

        # Render question
        sys.stdout.write(Command.CLEAR_LINE.value)
        print(prompt)

        # Render choices
        print_questions(choices, index)

    # Initial render - print all lines first
    print(prompt)
    print_questions(choices, index)

    while True:
        key = read_key()

        if key == "up":
            index = (index - 1) % len(choices)
            render()
        elif key == "down":
            index = (index + 1) % len(choices)
            render()
        elif key == "enter":
            answer = choices[index]

            # Clear the menu
            sys.stdout.write(Command.MOVE_UP.value * (len(choices) + 1))
            for _ in range(len(choices) + 1):
                sys.stdout.write(Command.CLEAR_LINE.value + "\n")
            sys.stdout.write(Command.MOVE_UP.value * (len(choices) + 1))

            # Print final result
            # We use print here because we want to end with \n
            print(format_answer(question, answer.label or answer.value.capitalize()))

            return answer.value
