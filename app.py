"""
app.py
CyberLearn -- a free, offline, no-sign-in, Duolingo-style learning app for
cybersecurity fundamentals and Python programming.

Everything runs locally: no network calls, no accounts, no telemetry.
Progress is saved to ~/.cyberlearn/progress.json (see progress.py) and
persists forever between runs until the player deletes that folder.

Run with:  python main.py
"""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox
from typing import Optional

import content
import progress as progress_mod
import theme as theme_mod
from widgets import (
    RoundedButton, LessonNode, AnimatedProgressBar, Confetti,
    draw_logo, Toast, ScrollableFrame,
)

APP_TITLE = "CyberLearn -- Learn Hacking & Cybersecurity"
WINDOW_SIZE = "1180x760"
MIN_SIZE = (980, 640)


# =============================================================================
# Application controller
# =============================================================================
class CyberLearnApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(WINDOW_SIZE)
        self.minsize(*MIN_SIZE)

        self.progress: progress_mod.Progress = progress_mod.load()
        self.progress.refill_hearts_if_needed()
        self.theme: theme_mod.Theme = theme_mod.THEMES.get(
            self.progress.theme, theme_mod.DARK
        )

        self.configure(bg=self.theme.bg)
        self.container = tk.Frame(self, bg=self.theme.bg)
        self.container.pack(fill="both", expand=True)

        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self.show_home()

    # ---- persistence -------------------------------------------------
    def save(self):
        progress_mod.save(self.progress)

    def _on_close(self):
        self.save()
        self.destroy()

    # ---- theme ---------------------------------------------------------
    def toggle_theme(self):
        new_name = "light" if self.theme.name == "dark" else "dark"
        self.theme = theme_mod.THEMES[new_name]
        self.progress.theme = new_name
        self.configure(bg=self.theme.bg)
        self.container.configure(bg=self.theme.bg)
        self.save()
        self.show_home()

    # ---- navigation ------------------------------------------------------
    def _clear_container(self):
        for child in self.container.winfo_children():
            child.destroy()

    def show_home(self):
        self._clear_container()
        HomeScreen(self.container, self).pack(fill="both", expand=True)

    def show_track(self, track_id: str):
        self._clear_container()
        TrackScreen(self.container, self, track_id).pack(fill="both", expand=True)

    def show_lesson(self, track_id: str, lesson_id: str):
        self._clear_container()
        LessonScreen(self.container, self, track_id, lesson_id).pack(
            fill="both", expand=True
        )


# =============================================================================
# Home screen -- dashboard + track picker
# =============================================================================
class HomeScreen(tk.Frame):
    def __init__(self, parent, app: CyberLearnApp):
        t = app.theme
        super().__init__(parent, bg=t.bg)
        self.app = app
        self.t = t

        self._build_header()
        self._build_stats_bar()
        self._build_track_grid()
        self._build_footer()

    # -- header with logo + title + theme toggle -----------------------
    def _build_header(self):
        t = self.t
        header = tk.Frame(self, bg=t.bg)
        header.pack(fill="x", padx=32, pady=(24, 8))

        left = tk.Frame(header, bg=t.bg)
        left.pack(side="left")

        logo_canvas = tk.Canvas(left, width=48, height=48, bg=t.bg,
                                 highlightthickness=0)
        logo_canvas.pack(side="left", padx=(0, 12))
        draw_logo(logo_canvas, 24, 24, 40, t.accent, t.bg)

        title_frame = tk.Frame(left, bg=t.bg)
        title_frame.pack(side="left")
        tk.Label(title_frame, text="CyberLearn", bg=t.bg, fg=t.fg,
                 font=(t.font_family, 22, "bold")).pack(anchor="w")
        tk.Label(title_frame, text="Learn hacking & cybersecurity, one minute at a time",
                 bg=t.bg, fg=t.fg_muted,
                 font=(t.font_family, 10)).pack(anchor="w")

        right = tk.Frame(header, bg=t.bg)
        right.pack(side="right")
        theme_label = "☀ Light" if t.name == "dark" else "🌙 Dark"
        RoundedButton(right, text=theme_label, command=self.app.toggle_theme,
                      bg=t.bg_alt, fg=t.fg, accent=t.border,
                      hover_accent=t.accent, width=120, height=40,
                      parent_bg=t.bg).pack(side="right")

    # -- XP / streak / rank / hearts strip ------------------------------
    def _build_stats_bar(self):
        t = self.t
        p = self.app.progress
        bar = tk.Frame(self, bg=t.bg_alt)
        bar.pack(fill="x", padx=32, pady=(12, 20))

        inner = tk.Frame(bar, bg=t.bg_alt)
        inner.pack(fill="x", padx=20, pady=16)

        threshold, rank_name, rank_icon = theme_mod.rank_for_xp(p.xp)
        self._stat(inner, f"{rank_icon}", f"{p.xp} XP", rank_name)
        self._stat(inner, "🔥", f"{p.streak} day streak",
                    "keep it going!" if p.streak else "start today")
        self._stat(inner, "❤️", f"{p.hearts}/5 hearts",
                    "regenerate over time")

        total = content.total_lesson_count()
        done = len(p.completed_lessons)
        self._stat(inner, "📘", f"{done}/{total} lessons",
                    "across every track")

    def _stat(self, parent, icon, main, sub):
        t = self.t
        box = tk.Frame(parent, bg=t.bg_alt)
        box.pack(side="left", padx=24)
        tk.Label(box, text=icon, bg=t.bg_alt, fg=t.fg,
                 font=(t.font_family, 20)).pack()
        tk.Label(box, text=main, bg=t.bg_alt, fg=t.fg,
                 font=(t.font_family, 13, "bold")).pack()
        tk.Label(box, text=sub, bg=t.bg_alt, fg=t.fg_muted,
                 font=(t.font_family, 9)).pack()

    # -- scrollable grid of track cards ------------------------------------
    def _build_track_grid(self):
        t = self.t
        wrapper = tk.Frame(self, bg=t.bg)
        wrapper.pack(fill="both", expand=True, padx=32, pady=(0, 12))

        tk.Label(wrapper, text="Choose a track", bg=t.bg, fg=t.fg,
                 font=(t.font_family, 15, "bold")).pack(anchor="w", pady=(0, 10))

        scroller = ScrollableFrame(wrapper, bg=t.bg)
        scroller.pack(fill="both", expand=True)

        grid = tk.Frame(scroller.body, bg=t.bg)
        grid.pack(fill="both", expand=True)

        cols = 3
        for i, (track_id, track) in enumerate(content.TRACKS.items()):
            r, c = divmod(i, cols)
            grid.grid_columnconfigure(c, weight=1, uniform="col")
            card = self._build_track_card(grid, track_id, track)
            card.grid(row=r, column=c, padx=10, pady=10, sticky="nsew")

    def _build_track_card(self, parent, track_id, track):
        t = self.t
        style = theme_mod.TRACK_STYLE.get(track_id, {"color": t.accent, "icon": "📘"})
        color = style["color"]
        p = self.app.progress

        ids = content.all_lesson_ids_for_track(track_id)
        frac = p.track_progress(ids)

        card = tk.Frame(parent, bg=t.bg_alt, highlightbackground=t.border,
                         highlightthickness=1)

        def on_enter(_e=None):
            card.configure(highlightbackground=color, highlightthickness=2)

        def on_leave(_e=None):
            card.configure(highlightbackground=t.border, highlightthickness=1)

        def on_click(_e=None):
            self.app.show_track(track_id)

        inner = tk.Frame(card, bg=t.bg_alt)
        inner.pack(fill="both", expand=True, padx=18, pady=16)

        tk.Label(inner, text=style["icon"], bg=t.bg_alt, fg=color,
                 font=(t.font_family, 28)).pack(anchor="w")
        tk.Label(inner, text=track["name"], bg=t.bg_alt, fg=t.fg,
                 font=(t.font_family, 14, "bold"), wraplength=220,
                 justify="left").pack(anchor="w", pady=(6, 2))
        tk.Label(inner, text=track["tagline"], bg=t.bg_alt, fg=t.fg_muted,
                 font=(t.font_family, 9), wraplength=220,
                 justify="left").pack(anchor="w", pady=(0, 10))

        pbar = AnimatedProgressBar(inner, width=220, height=10,
                                    track_color=t.border, fill_color=color,
                                    value=frac)
        pbar.pack(anchor="w")
        done_count = sum(1 for lid in ids if p.is_completed(lid))
        tk.Label(inner, text=f"{done_count}/{len(ids)} lessons complete",
                 bg=t.bg_alt, fg=t.fg_muted,
                 font=(t.font_family, 8)).pack(anchor="w", pady=(4, 0))

        for widget in (card, inner, *inner.winfo_children()):
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            widget.bind("<Button-1>", on_click)
            widget.configure(cursor="hand2")

        return card

    # -- footer with reset link -----------------------------------------
    def _build_footer(self):
        t = self.t
        footer = tk.Frame(self, bg=t.bg)
        footer.pack(fill="x", padx=32, pady=(0, 16))
        tk.Label(footer, text="100% free & offline -- no account, no tracking, no ads.",
                 bg=t.bg, fg=t.fg_muted, font=(t.font_family, 9)).pack(side="left")

        reset_lbl = tk.Label(footer, text="Reset all progress",
                              bg=t.bg, fg=t.fg_muted, font=(t.font_family, 9, "underline"),
                              cursor="hand2")
        reset_lbl.pack(side="right")
        reset_lbl.bind("<Button-1>", lambda e: self._confirm_reset())

    def _confirm_reset(self):
        if messagebox.askyesno(
            "Reset progress?",
            "This deletes all XP, streaks, and completed lessons. "
            "This can't be undone. Continue?",
        ):
            self.app.progress = progress_mod.Progress()
            self.app.save()
            self.app.show_home()


# =============================================================================
# Track screen -- chapters + the lesson path
# =============================================================================
class TrackScreen(tk.Frame):
    def __init__(self, parent, app: CyberLearnApp, track_id: str):
        t = app.theme
        super().__init__(parent, bg=t.bg)
        self.app = app
        self.t = t
        self.track_id = track_id
        self.track = content.TRACKS[track_id]
        self.style = theme_mod.TRACK_STYLE.get(
            track_id, {"color": t.accent, "icon": "📘"}
        )

        self._build_header()
        self._build_path()

    def _build_header(self):
        t, style = self.t, self.style
        header = tk.Frame(self, bg=t.bg)
        header.pack(fill="x", padx=32, pady=(24, 10))

        RoundedButton(header, text="← Back", command=self.app.show_home,
                      bg=t.bg_alt, fg=t.fg, accent=t.border,
                      hover_accent=t.accent, width=100, height=36,
                      parent_bg=t.bg).pack(anchor="w", pady=(0, 14))

        title_row = tk.Frame(header, bg=t.bg)
        title_row.pack(fill="x")
        tk.Label(title_row, text=style["icon"], bg=t.bg, fg=style["color"],
                 font=(t.font_family, 30)).pack(side="left", padx=(0, 12))

        text_col = tk.Frame(title_row, bg=t.bg)
        text_col.pack(side="left", fill="x", expand=True)
        tk.Label(text_col, text=self.track["name"], bg=t.bg, fg=t.fg,
                 font=(t.font_family, 20, "bold")).pack(anchor="w")
        tk.Label(text_col, text=self.track["tagline"], bg=t.bg, fg=t.fg_muted,
                 font=(t.font_family, 10)).pack(anchor="w")

        ids = content.all_lesson_ids_for_track(self.track_id)
        p = self.app.progress
        frac = p.track_progress(ids)
        done_count = sum(1 for lid in ids if p.is_completed(lid))

        progress_col = tk.Frame(header, bg=t.bg)
        progress_col.pack(fill="x", pady=(14, 0))
        AnimatedProgressBar(progress_col, width=400, height=12,
                             track_color=t.bg_alt, fill_color=style["color"],
                             value=frac).pack(anchor="w")
        tk.Label(progress_col, text=f"{done_count}/{len(ids)} lessons complete "
                                     f"({int(frac * 100)}%)",
                 bg=t.bg, fg=t.fg_muted,
                 font=(t.font_family, 9)).pack(anchor="w", pady=(4, 0))

    def _build_path(self):
        t, style = self.t, self.style
        p = self.app.progress

        wrapper = tk.Frame(self, bg=t.bg)
        wrapper.pack(fill="both", expand=True, padx=32, pady=(10, 20))

        scroller = ScrollableFrame(wrapper, bg=t.bg)
        scroller.pack(fill="both", expand=True)
        body = scroller.body

        all_ids = content.all_lesson_ids_for_track(self.track_id)

        for chapter in self.track["chapters"]:
            chap_frame = tk.Frame(body, bg=t.bg)
            chap_frame.pack(fill="x", pady=(4, 18))

            tk.Label(chap_frame, text=chapter["title"].upper(), bg=t.bg,
                     fg=t.fg_muted, font=(t.font_family, 10, "bold")).pack(
                anchor="w", pady=(0, 8)
            )

            row = tk.Frame(chap_frame, bg=t.bg)
            row.pack(fill="x")

            for lesson in chapter["lessons"]:
                idx_in_track = all_ids.index(lesson["id"])
                state = self._lesson_state(all_ids, idx_in_track, p)

                node_box = tk.Frame(row, bg=t.bg)
                node_box.pack(side="left", padx=10)

                node = LessonNode(
                    node_box, index=idx_in_track + 1, state=state,
                    accent=style["color"], parent_bg=t.bg,
                    command=(lambda lid=lesson["id"]: self._open_lesson(lid))
                    if state != LessonNode.STATE_LOCKED else None,
                )
                node.pack()
                tk.Label(node_box, text=lesson["title"], bg=t.bg, fg=t.fg_muted,
                         font=(t.font_family, 8), wraplength=90,
                         justify="center").pack(pady=(4, 0))

    @staticmethod
    def _lesson_state(all_ids, idx, p: progress_mod.Progress) -> str:
        lid = all_ids[idx]
        if p.is_completed(lid):
            return LessonNode.STATE_DONE
        if idx == 0 or p.is_completed(all_ids[idx - 1]):
            return LessonNode.STATE_AVAILABLE
        return LessonNode.STATE_LOCKED

    def _open_lesson(self, lesson_id: str):
        self.app.show_lesson(self.track_id, lesson_id)


# =============================================================================
# Lesson screen -- ~1 minute explanation, then a one-question check
# =============================================================================
class LessonScreen(tk.Frame):
    """Two-phase lesson: READ (the minute-explanation) then QUIZ (one
    multiple-choice check). Answering advances progress and offers a
    direct 'Next lesson' continuation so a whole chapter can be played
    through without returning to the track map every time."""

    PHASE_READ = "read"
    PHASE_QUIZ = "quiz"
    PHASE_RESULT = "result"

    def __init__(self, parent, app: CyberLearnApp, track_id: str, lesson_id: str):
        t = app.theme
        super().__init__(parent, bg=t.bg)
        self.app = app
        self.t = t
        self.track_id = track_id
        self.track = content.TRACKS[track_id]
        self.style = theme_mod.TRACK_STYLE.get(
            track_id, {"color": t.accent, "icon": "📘"}
        )
        _, chapter_id, lesson = content.find_lesson(lesson_id)
        self.chapter_id = chapter_id
        self.lesson = lesson
        self.phase = self.PHASE_READ
        self.selected_index: Optional[int] = None

        self._build_header()
        self.body = tk.Frame(self, bg=t.bg)
        self.body.pack(fill="both", expand=True, padx=32, pady=(10, 24))
        self._render_phase()

    # -- shared header ---------------------------------------------------
    def _build_header(self):
        t, style = self.t, self.style
        header = tk.Frame(self, bg=t.bg)
        header.pack(fill="x", padx=32, pady=(20, 4))

        RoundedButton(header, text="← Track", command=self._back_to_track,
                      bg=t.bg_alt, fg=t.fg, accent=t.border,
                      hover_accent=t.accent, width=100, height=34,
                      parent_bg=t.bg).pack(side="left")

        crumb = tk.Frame(header, bg=t.bg)
        crumb.pack(side="left", padx=16)
        chapter_title = next(
            c["title"] for c in self.track["chapters"] if c["id"] == self.chapter_id
        )
        tk.Label(crumb, text=f"{style['icon']} {self.track['name']} · {chapter_title}",
                 bg=t.bg, fg=t.fg_muted,
                 font=(t.font_family, 10)).pack(anchor="w")

    def _back_to_track(self):
        self.app.show_track(self.track_id)

    # -- phase rendering ---------------------------------------------------
    def _clear_body(self):
        for w in self.body.winfo_children():
            w.destroy()

    def _render_phase(self):
        self._clear_body()
        if self.phase == self.PHASE_READ:
            self._render_read_phase()
        elif self.phase == self.PHASE_QUIZ:
            self._render_quiz_phase()
        else:
            self._render_result_phase()

    def _card(self, parent, **kwargs):
        t = self.t
        card = tk.Frame(parent, bg=t.bg_alt, highlightbackground=t.border,
                         highlightthickness=1, **kwargs)
        return card

    # -- Phase 1: the ~1 minute explanation --------------------------------
    def _render_read_phase(self):
        t, style = self.t, self.style

        title = tk.Label(self.body, text=self.lesson["title"], bg=t.bg, fg=t.fg,
                          font=(t.font_family, 22, "bold"))
        title.pack(anchor="w", pady=(4, 16))

        card = self._card(self.body)
        card.pack(fill="both", expand=True)
        inner = tk.Frame(card, bg=t.bg_alt)
        inner.pack(fill="both", expand=True, padx=28, pady=26)

        badge = tk.Label(inner, text="⏱  ABOUT 1 MINUTE", bg=t.bg_alt,
                          fg=style["color"], font=(t.font_family, 9, "bold"))
        badge.pack(anchor="w", pady=(0, 14))

        text = tk.Label(inner, text=self.lesson["minute"], bg=t.bg_alt, fg=t.fg,
                         font=(t.font_family, 13), justify="left",
                         wraplength=760)
        text.pack(anchor="w", fill="both", expand=True)

        btn_row = tk.Frame(self.body, bg=t.bg)
        btn_row.pack(fill="x", pady=(20, 0))
        RoundedButton(btn_row, text="Continue to check  →",
                      command=self._go_to_quiz,
                      bg=style["color"], fg="#0f1720", accent=style["color"],
                      hover_accent=self._lighten(style["color"]),
                      width=240, height=52, parent_bg=t.bg).pack(anchor="e")

    def _go_to_quiz(self):
        self.phase = self.PHASE_QUIZ
        self.selected_index = None
        self._render_phase()

    # -- Phase 2: the multiple-choice check --------------------------------
    def _render_quiz_phase(self):
        t, style = self.t, self.style

        title = tk.Label(self.body, text="Quick check", bg=t.bg, fg=t.fg,
                          font=(t.font_family, 20, "bold"))
        title.pack(anchor="w", pady=(4, 16))

        card = self._card(self.body)
        card.pack(fill="both", expand=True)
        inner = tk.Frame(card, bg=t.bg_alt)
        inner.pack(fill="both", expand=True, padx=28, pady=26)

        tk.Label(inner, text=self.lesson["question"], bg=t.bg_alt, fg=t.fg,
                 font=(t.font_family, 14, "bold"), justify="left",
                 wraplength=760).pack(anchor="w", pady=(0, 18))

        self.choice_buttons = []
        for i, choice in enumerate(self.lesson["choices"]):
            btn = RoundedButton(
                inner, text=f"{chr(65 + i)}.  {choice}",
                command=(lambda idx=i: self._select_choice(idx)),
                bg=t.bg, fg=t.fg, accent=t.border, hover_accent=style["color"],
                width=720, height=48, parent_bg=t.bg_alt,
            )
            btn.pack(anchor="w", pady=6, fill="x")
            self.choice_buttons.append(btn)

    def _select_choice(self, idx: int):
        self.selected_index = idx
        correct = idx == self.lesson["correct"]

        # lock all choice buttons and recolor to show right/wrong
        for i, btn in enumerate(self.choice_buttons):
            btn.set_disabled(True)
            if i == self.lesson["correct"]:
                btn._draw(fill=self.t.success, outline=self.t.success,
                          text_color="#0f1720")
            elif i == idx:
                btn._draw(fill=self.t.error, outline=self.t.error,
                          text_color="#ffffff")

        p = self.app.progress
        already_done = p.is_completed(self.lesson["id"])
        p.mark_completed(self.lesson["id"], self.lesson["xp"], correct)
        p.refill_hearts_if_needed()
        if not correct:
            p.lose_heart()
        self.app.save()

        self.phase = self.PHASE_RESULT
        self._last_correct = correct
        self._first_completion = correct and not already_done
        self.after(500, self._render_phase)

    # -- Phase 3: result + explanation + continue ---------------------------
    def _render_result_phase(self):
        t, style = self.t, self.style
        correct = getattr(self, "_last_correct", False)
        first_completion = getattr(self, "_first_completion", False)

        if first_completion:
            # Confetti gets its own reserved strip of the layout rather than
            # floating over other widgets, since tkinter canvases are opaque
            # and would otherwise hide whatever's underneath them.
            fx = tk.Canvas(self.body, height=70, bg=t.bg, highlightthickness=0)
            fx.pack(fill="x")
            fx.update_idletasks()
            cx = fx.winfo_width() // 2 or 380
            Confetti(fx, cx, 35, count=30)

        banner_color = t.success if correct else t.error
        banner_text = "✓ Correct!" if correct else "✗ Not quite"

        banner = tk.Frame(self.body, bg=banner_color)
        banner.pack(fill="x", pady=(4, 16))
        tk.Label(banner, text=f"{banner_text}   (+{self.lesson['xp'] if correct else max(1, self.lesson['xp'] // 4)} XP)",
                 bg=banner_color, fg="#0f1720" if correct else "#ffffff",
                 font=(t.font_family, 14, "bold")).pack(padx=18, pady=12, anchor="w")

        card = self._card(self.body)
        card.pack(fill="both", expand=True)
        inner = tk.Frame(card, bg=t.bg_alt)
        inner.pack(fill="both", expand=True, padx=28, pady=26)

        tk.Label(inner, text="Why", bg=t.bg_alt, fg=style["color"],
                 font=(t.font_family, 10, "bold")).pack(anchor="w", pady=(0, 8))
        tk.Label(inner, text=self.lesson["explain"], bg=t.bg_alt, fg=t.fg,
                 font=(t.font_family, 13), justify="left",
                 wraplength=760).pack(anchor="w")

        btn_row = tk.Frame(self.body, bg=t.bg)
        btn_row.pack(fill="x", pady=(20, 0))

        next_lesson_id = self._next_lesson_id()
        if next_lesson_id:
            RoundedButton(btn_row, text="Next lesson  →",
                          command=lambda: self.app.show_lesson(self.track_id, next_lesson_id),
                          bg=style["color"], fg="#0f1720", accent=style["color"],
                          hover_accent=self._lighten(style["color"]),
                          width=220, height=52, parent_bg=t.bg).pack(side="right")
        else:
            RoundedButton(btn_row, text="🎉 Finish track",
                          command=self._back_to_track,
                          bg=style["color"], fg="#0f1720", accent=style["color"],
                          hover_accent=self._lighten(style["color"]),
                          width=220, height=52, parent_bg=t.bg).pack(side="right")

        RoundedButton(btn_row, text="Back to path", command=self._back_to_track,
                      bg=t.bg_alt, fg=t.fg, accent=t.border,
                      hover_accent=t.accent, width=160, height=52,
                      parent_bg=t.bg).pack(side="right", padx=(0, 12))

    def _next_lesson_id(self) -> Optional[str]:
        all_ids = content.all_lesson_ids_for_track(self.track_id)
        idx = all_ids.index(self.lesson["id"])
        if idx + 1 < len(all_ids):
            return all_ids[idx + 1]
        return None

    @staticmethod
    def _lighten(hex_color: str) -> str:
        hex_color = hex_color.lstrip("#")
        if len(hex_color) != 6:
            return "#ffffff"
        r, g, b = (int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        r = min(255, int(r + (255 - r) * 0.25))
        g = min(255, int(g + (255 - g) * 0.25))
        b = min(255, int(b + (255 - b) * 0.25))
        return f"#{r:02x}{g:02x}{b:02x}"
