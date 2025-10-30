# search_engine.py
import sys
import os

def _get_char():
    """Platform-independent single-character reader (no Enter)."""
    if os.name == "nt":  # Windows
        import msvcrt
        ch = msvcrt.getwch()
        return ch
    else:  # Unix / Mac
        import termios, tty
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


def search_loop(bst):
    print("Start typing... (Backspace = delete, ESC = quit)\n")
    prefix = ""
    while True:
        ch = _get_char()

        # ESC to quit
        if ord(ch) == 27:
            print("\nExiting...")
            break

        # Handle Enter (ignored)
        if ch in ("\r", "\n"):
            continue

        # Handle backspace
        if ch in ("\b", "\x7f"):
            prefix = prefix[:-1]
        else:
            prefix += ch

        # Clear screen before reprinting (optional)
        os.system("cls" if os.name == "nt" else "clear")

        print(f"Prefix: '{prefix}'")
        if prefix:
            suggestions = bst.autocomplete(prefix)
            if suggestions:
                print("Suggestions:")
                for w in suggestions[:10]:
                    print("  -", w)
                if len(suggestions) > 10:
                    print(f"  ... and {len(suggestions) - 10} more")
            else:
                print("(no results)")
        else:
            print("(type something)")
