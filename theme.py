"""
theme.py
Color palettes and visual theme definitions for CyberLearn.

Two built-in themes (dark / light), plus one accent color per track so the
app feels alive and each track has its own visual identity, Duolingo-style.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Theme:
    name: str
    bg: str            # main window background
    bg_alt: str         # panel / card background
    bg_elevated: str     # elevated card (hover / selected)
    fg: str              # primary text
    fg_muted: str         # secondary text
    border: str
    accent: str          # default accent (buttons, progress bar)
    success: str
    error: str
    warning: str
    font_family: str = "Segoe UI"
    font_family_mono: str = "Consolas"


DARK = Theme(
    name="dark",
    bg="#0f1720",
    bg_alt="#16212c",
    bg_elevated="#1e2d3a",
    fg="#eef3f8",
    fg_muted="#93a4b5",
    border="#26374a",
    accent="#58cc02",       # duolingo-esque green
    success="#58cc02",
    error="#ff4b4b",
    warning="#ffc800",
    font_family="Segoe UI",
    font_family_mono="Consolas",
)

LIGHT = Theme(
    name="light",
    bg="#f7fafc",
    bg_alt="#ffffff",
    bg_elevated="#eef2f6",
    fg="#1b2733",
    fg_muted="#5b6b7a",
    border="#d9e2ea",
    accent="#2b70e0",
    success="#2fae4a",
    error="#e0392b",
    warning="#d68b00",
    font_family="Segoe UI",
    font_family_mono="Consolas",
)

THEMES = {"dark": DARK, "light": LIGHT}

# Each track gets its own accent color + emoji glyph, independent of the
# global light/dark theme, so the track picker screen looks colorful and
# the player always knows which "hat" they're in.
TRACK_STYLE = {
    "blue_team": {"color": "#2b8fe0", "glow": "#0d3a5c", "icon": "🛡️"},
    "red_team":  {"color": "#e0392b", "glow": "#5c140d", "icon": "🗡️"},
    "white_hat": {"color": "#e8e8e8", "glow": "#4a4a4a", "icon": "⚪"},
    "black_hat": {"color": "#8b5cf6", "glow": "#2e1a4d", "icon": "🕶️"},
    "python":    {"color": "#f2c14e", "glow": "#5c4a12", "icon": "🐍"},
    "networking": {"color": "#22c1a4", "glow": "#0d4a3d", "icon": "🌐"},
    "tools":     {"color": "#ff8c42", "glow": "#5c320d", "icon": "🧰"},
}

RANK_THRESHOLDS = [
    (0, "Script Kiddie", "🥚"),
    (150, "Recruit", "🔰"),
    (400, "Analyst", "🧭"),
    (800, "Operator", "⚙️"),
    (1500, "Specialist", "🎯"),
    (2600, "Expert", "🧠"),
    (4200, "Veteran", "🏅"),
    (6500, "Elite", "💎"),
    (10000, "Legend", "👑"),
]


def rank_for_xp(xp: int):
    current = RANK_THRESHOLDS[0]
    for threshold, name, icon in RANK_THRESHOLDS:
        if xp >= threshold:
            current = (threshold, name, icon)
        else:
            break
    return current
