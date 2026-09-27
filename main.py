#!/usr/bin/env python3
"""
CyberLearn -- a free, offline, no-sign-in, Duolingo-style app for learning
hacking & cybersecurity fundamentals plus Python programming.

Usage:
    python main.py

Requires only the Python standard library. On most systems that includes
tkinter already. If you get "No module named tkinter":
    Windows / macOS (python.org installer): tkinter is already included --
        reinstall Python and make sure "tcl/tk" is checked during setup.
    Debian / Ubuntu / Mint:  sudo apt install python3-tk
    Fedora:                  sudo dnf install python3-tkinter
    Arch:                    sudo pacman -S tk
"""

import sys


def main():
    try:
        import tkinter  # noqa: F401
    except ImportError:
        print(
            "CyberLearn needs tkinter, which isn't installed for this Python.\n"
            "  Debian/Ubuntu/Mint:  sudo apt install python3-tk\n"
            "  Fedora:              sudo dnf install python3-tkinter\n"
            "  Arch:                sudo pacman -S tk\n"
            "  Windows/macOS:       reinstall Python from python.org and make\n"
            "                       sure the 'tcl/tk' option is checked.",
            file=sys.stderr,
        )
        sys.exit(1)

    from app import CyberLearnApp

    app = CyberLearnApp()
    app.mainloop()


if __name__ == "__main__":
    main()
