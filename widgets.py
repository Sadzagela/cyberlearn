"""
widgets.py
Small, dependency-free, hand-drawn UI components used throughout the app.
Everything here is pure tkinter + tkinter.Canvas -- no image files, no
third-party packages -- so the app stays 100% self-contained and portable.
"""

from __future__ import annotations

import math
import random
import tkinter as tk
from typing import Callable, Optional


# ---------------------------------------------------------------------------
# Rounded rectangle primitive
# ---------------------------------------------------------------------------
def rounded_rect(canvas: tk.Canvas, x1, y1, x2, y2, radius=18, **kwargs):
    """Draw a rounded rectangle on a canvas using a smoothed polygon."""
    points = [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1,
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)


# ---------------------------------------------------------------------------
# RoundedButton -- a canvas-based button with hover/press feedback
# ---------------------------------------------------------------------------
class RoundedButton(tk.Frame):
    def __init__(self, parent, text: str, command: Optional[Callable] = None,
                 bg="#16212c", fg="#eef3f8", accent="#58cc02",
                 hover_accent=None, width=220, height=50,
                 font=("Segoe UI", 12, "bold"), disabled=False,
                 subtle=False, **kwargs):
        parent_bg = kwargs.pop("parent_bg", None)
        super().__init__(parent, bg=parent_bg or parent.cget("bg"))

        self._command = command
        self._accent = accent
        self._hover_accent = hover_accent or accent
        self._bg = bg
        self._fg = fg
        self._disabled = disabled
        self._subtle = subtle

        # Do NOT use self._w or self._h.
        # Tkinter uses self._w internally.
        self._width = width
        self._height = height

        self.canvas = tk.Canvas(
            self,
            width=width,
            height=height,
            highlightthickness=0,
            bg=parent_bg or parent.cget("bg")
        )
        self.canvas.pack()

        self._text = text

        self._draw(
            fill=self._bg if not subtle else parent_bg or parent.cget("bg"),
            outline=accent
        )

        if not disabled:
            self.canvas.bind("<Enter>", self._on_enter)
            self.canvas.bind("<Leave>", self._on_leave)
            self.canvas.bind("<Button-1>", self._on_click)
            self.canvas.configure(cursor="hand2")

    def _draw(self, fill, outline, text_color=None):
        self.canvas.delete("all")

        rounded_rect(
            self.canvas,
            2,
            2,
            self._width - 2,
            self._height - 2,
            radius=self._height // 2,
            fill=fill,
            outline=outline,
            width=2
        )

        tcolor = text_color or self._fg

        self.canvas.create_text(
            self._width // 2,
            self._height // 2,
            text=self._text,
            fill=tcolor,
            font=("Segoe UI", 12, "bold")
        )

    def _on_enter(self, _evt=None):
        if self._disabled:
            return

        self._draw(
            fill=self._hover_accent,
            outline=self._hover_accent,
            text_color="#0f1720" if self._subtle else self._fg
        )

    def _on_leave(self, _evt=None):
        if self._disabled:
            return

        self._draw(
            fill=self._bg if not self._subtle else self.canvas.cget("bg"),
            outline=self._accent
        )

    def _on_click(self, _evt=None):
        if self._disabled or self._command is None:
            return

        self._command()

    def set_text(self, text: str):
        self._text = text
        self._on_leave()

    def set_disabled(self, disabled: bool):
        self._disabled = disabled

        if disabled:
            self._draw(
                fill="#33414f",
                outline="#33414f",
                text_color="#7a8a99"
            )
            self.canvas.unbind("<Enter>")
            self.canvas.unbind("<Leave>")
            self.canvas.unbind("<Button-1>")
            self.canvas.configure(cursor="arrow")
        else:
            self.canvas.bind("<Enter>", self._on_enter)
            self.canvas.bind("<Leave>", self._on_leave)
            self.canvas.bind("<Button-1>", self._on_click)
            self.canvas.configure(cursor="hand2")
            self._on_leave()


# ---------------------------------------------------------------------------
# LessonNode -- the circular numbered node on a chapter path (Duolingo-style)
# ---------------------------------------------------------------------------
class LessonNode(tk.Canvas):
    STATE_LOCKED = "locked"
    STATE_AVAILABLE = "available"
    STATE_DONE = "done"

    def __init__(self, parent, index: int, state: str, accent: str,
                 command: Optional[Callable] = None, size=64, parent_bg="#0f1720"):
        super().__init__(parent, width=size, height=size,
                          highlightthickness=0, bg=parent_bg)
        self.size = size
        self.index = index
        self.state = state
        self.accent = accent
        self._command = command
        self._draw()
        if state != self.STATE_LOCKED and command is not None:
            self.bind("<Button-1>", lambda e: command())
            self.bind("<Enter>", lambda e: self._draw(hover=True))
            self.bind("<Leave>", lambda e: self._draw(hover=False))
            self.configure(cursor="hand2")

    def _draw(self, hover=False):
        self.delete("all")
        s = self.size
        pad = 4
        if self.state == self.STATE_LOCKED:
            fill, outline, glyph = "#1e2d3a", "#33414f", "🔒"
            text_color = "#5b6b7a"
        elif self.state == self.STATE_DONE:
            fill, outline, glyph = self.accent, self.accent, "✓"
            text_color = "#0f1720"
        else:  # available
            fill = self.accent if hover else "#1e2d3a"
            outline = self.accent
            glyph = str(self.index)
            text_color = "#0f1720" if hover else self.accent
        self.create_oval(pad, pad, s - pad, s - pad, fill=fill, outline=outline, width=3)
        self.create_text(s // 2, s // 2, text=glyph, fill=text_color,
                          font=("Segoe UI", 16, "bold"))


# ---------------------------------------------------------------------------
# AnimatedProgressBar -- smooth fill animation, no external deps
# ---------------------------------------------------------------------------
class AnimatedProgressBar(tk.Canvas):
    def __init__(self, parent, width=220, height=14, track_color="#1e2d3a",
                 fill_color="#58cc02", value=0.0, **kwargs):

        super().__init__(
            parent,
            width=width,
            height=height,
            highlightthickness=0,
            bg=parent.cget("bg"),
            **kwargs
        )

        self._width = width
        self._height = height

        self._track_color = track_color
        self._fill_color = fill_color
        self._value = 0.0
        self._target = max(0.0, min(1.0, value))

        self._draw(self._value)

        if self._target > 0:
            self.set_value(value, animate=False)

    def _draw(self, frac):
        self.delete("all")

        rounded_rect(
            self,
            0,
            0,
            self._width,
            self._height,
            radius=self._height // 2,
            fill=self._track_color,
            outline=""
        )

        fw = max(
            self._height,
            frac * self._width
        ) if frac > 0 else 0

        if fw > 0:
            rounded_rect(
                self,
                0,
                0,
                fw,
                self._height,
                radius=self._height // 2,
                fill=self._fill_color,
                outline=""
            )

    def set_value(self, frac: float, animate=True):
        frac = max(0.0, min(1.0, frac))
        self._target = frac

        if not animate:
            self._value = frac
            self._draw(frac)
            return

        self._animate_step()

    def _animate_step(self):
        diff = self._target - self._value

        if abs(diff) < 0.01:
            self._value = self._target
            self._draw(self._value)
            return

        self._value += diff * 0.25
        self._draw(self._value)
        self.after(16, self._animate_step)



# ---------------------------------------------------------------------------
# Confetti burst -- a small celebratory particle animation on a canvas
# ---------------------------------------------------------------------------
class Confetti:
    COLORS = ["#58cc02", "#ffc800", "#ff4b4b", "#2b8fe0", "#8b5cf6", "#22c1a4"]

    def __init__(self, canvas: tk.Canvas, x: int, y: int, count: int = 26):
        self.canvas = canvas
        self.particles = []
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2.5, 7.0)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed - 3.5
            size = random.randint(4, 8)
            color = random.choice(self.COLORS)
            item = canvas.create_rectangle(x, y, x + size, y + size,
                                            fill=color, outline="")
            self.particles.append([item, vx, vy, 0.0])
        self._frame = 0
        self._tick()

    def _tick(self):
        self._frame += 1
        alive = False
        for p in self.particles:
            item, vx, vy, rot = p
            vy += 0.35  # gravity
            p[2] = vy
            self.canvas.move(item, vx, vy)
            if self._frame < 40:
                alive = True
        if alive:
            self.canvas.after(16, self._tick)
        else:
            for p in self.particles:
                try:
                    self.canvas.delete(p[0])
                except tk.TclError:
                    pass


# ---------------------------------------------------------------------------
# Logo -- a small vector shield-and-lock mark, drawn with canvas primitives
# ---------------------------------------------------------------------------
def draw_logo(canvas: tk.Canvas, cx: int, cy: int, size: int, color: str,
              bg: str):
    """Draws a simple shield-with-lock logo centered at (cx, cy)."""
    half = size / 2
    shield = [
        cx, cy - half,
        cx + half * 0.85, cy - half * 0.55,
        cx + half * 0.85, cy + half * 0.15,
        cx, cy + half,
        cx - half * 0.85, cy + half * 0.15,
        cx - half * 0.85, cy - half * 0.55,
    ]
    canvas.create_polygon(shield, fill=color, outline=color, smooth=True)
    # lock body
    lw, lh = size * 0.32, size * 0.26
    lx, ly = cx - lw / 2, cy - lh / 4
    canvas.create_rectangle(lx, ly, lx + lw, ly + lh, fill=bg, outline=bg)
    # lock shackle
    canvas.create_arc(cx - lw * 0.35, ly - lh * 0.9, cx + lw * 0.35, ly + lh * 0.3,
                       start=0, extent=180, style="arc", outline=bg, width=max(2, int(size * 0.05)))


# ---------------------------------------------------------------------------
# Toast -- a small transient notification banner
# ---------------------------------------------------------------------------
class Toast:
    def __init__(self, parent: tk.Widget, text: str, bg="#58cc02", fg="#0f1720",
                 duration_ms=1800):
        self.top = tk.Toplevel(parent)
        self.top.overrideredirect(True)
        self.top.attributes("-topmost", True)
        try:
            self.top.attributes("-alpha", 0.96)
        except tk.TclError:
            pass
        frame = tk.Frame(self.top, bg=bg, padx=18, pady=10)
        frame.pack()
        tk.Label(frame, text=text, bg=bg, fg=fg,
                 font=("Segoe UI", 11, "bold")).pack()

        parent.update_idletasks()
        px = parent.winfo_rootx() + parent.winfo_width() // 2
        py = parent.winfo_rooty() + 40
        self.top.update_idletasks()
        w = self.top.winfo_width()
        self.top.geometry(f"+{px - w // 2}+{py}")
        self.top.after(duration_ms, self._close)

    def _close(self):
        try:
            self.top.destroy()
        except tk.TclError:
            pass


# ---------------------------------------------------------------------------
# ScrollableFrame -- a vertically scrollable container (mouse-wheel aware)
# ---------------------------------------------------------------------------
class ScrollableFrame(tk.Frame):
    """A Frame that can hold more content than fits on screen, with a
    working scrollbar and mouse-wheel support. Access `.body` to add
    child widgets -- everything placed inside `.body` scrolls together."""

    def __init__(self, parent, bg="#0f1720"):
        super().__init__(parent, bg=bg)
        self.canvas = tk.Canvas(self, bg=bg, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical",
                                       command=self.canvas.yview)
        self.body = tk.Frame(self.canvas, bg=bg)

        self.body.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        self._window = self.canvas.create_window((0, 0), window=self.body, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.bind("<Configure>", self._on_canvas_resize)
        self.bind_mousewheel(self.canvas)
        self.bind_mousewheel(self.body)

    def _on_canvas_resize(self, event):
        self.canvas.itemconfig(self._window, width=event.width)

    def bind_mousewheel(self, widget):
        widget.bind("<Enter>", lambda e: self._activate_wheel())
        widget.bind("<Leave>", lambda e: self._deactivate_wheel())

    def _activate_wheel(self):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)   # Windows/macOS
        self.canvas.bind_all("<Button-4>", self._on_mousewheel_linux)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel_linux)

    def _deactivate_wheel(self):
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_mousewheel_linux(self, event):
        direction = -1 if event.num == 4 else 1
        self.canvas.yview_scroll(direction, "units")
