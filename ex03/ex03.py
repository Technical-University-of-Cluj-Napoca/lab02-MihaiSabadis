# ex03.py
from datetime import datetime
import os

# ANSI colors
COLORS = {
    "INFO": "\033[94m",     # blue
    "DEBUG": "\033[90m",    # gray
    "WARNING": "\033[93m",  # yellow
    "ERROR": "\033[91m",    # red
    "RESET": "\033[0m",
}

def _strip_ansi(s: str) -> str:
    # simple, safe strip since we only use known codes above
    for code in COLORS.values():
        s = s.replace(code, "")
    return s

def smart_log(*args, **kwargs):
    """
    smart_log(message_parts..., level='info', colored=True, timestamp=True,
              date=False, save_to=None)

    Prints: HH:MM:SS [LEVEL] message...
    - Only the [LEVEL] and message are colored (time stays default).
    - If save_to is provided, appends the same line WITHOUT colors.
    """
    level = str(kwargs.get("level", "info")).upper()
    if level not in ("INFO", "DEBUG", "WARNING", "ERROR"):
        level = "INFO"

    colored = bool(kwargs.get("colored", True))
    show_time = bool(kwargs.get("timestamp", True))
    show_date = bool(kwargs.get("date", False))
    save_to = kwargs.get("save_to", None)

    now = datetime.now()
    prefix_parts = []
    if show_date:
        prefix_parts.append(now.strftime("%Y-%m-%d"))
    if show_time:
        prefix_parts.append(now.strftime("%H:%M:%S"))
    time_str = " ".join(prefix_parts)

    msg = " ".join(str(a) for a in args)

    # Build visible line
    level_tag = f"[{level}]"
    colored_chunk = f"{level_tag} {msg}"
    if colored:
        color = COLORS[level]
        colored_chunk = f"{color}{colored_chunk}{COLORS['RESET']}"

    line = f"{time_str} {colored_chunk}" if time_str else colored_chunk
    print(line)

    # Save to file (no colors)
    if save_to:
        os.makedirs(os.path.dirname(save_to) or ".", exist_ok=True)
        plain = _strip_ansi(f"{time_str} {level_tag} {msg}" if time_str else f"{level_tag} {msg}")
        with open(save_to, "a", encoding="utf-8") as f:
            f.write(plain + "\n")


# Demo
if __name__ == "__main__":
    smart_log("System started successfully.", level="info")
    smart_log("User alice logged in", level="debug")
    smart_log("Low disk space detected!", level="warning")
    smart_log("Model training failed!", level="error")
    smart_log("Process end", level="info")
