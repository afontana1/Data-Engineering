import os


def clear_console():
    if os.name == "nt":  # Windows
        _ = os.system("cls")
    else:  # Unix/Linux
        _ = os.system("clear")
