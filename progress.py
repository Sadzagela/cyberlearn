"""
progress.py
Fully local, offline, no-account progress tracking.

Everything is stored in a single JSON file in the user's home directory
under ~/.cyberlearn/progress.json. No network calls are made anywhere in
this module, or anywhere in the app. Progress persists forever between
runs until the player deletes that folder themselves.
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, List, Set


def _data_dir() -> Path:
    home = Path.home()
    d = home / ".cyberlearn"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _data_file() -> Path:
    return _data_dir() / "progress.json"


@dataclass
class Progress:
    xp: int = 0
    streak: int = 0
    last_active_date: str = ""          # ISO date string, e.g. "2026-09-27"
    completed_lessons: List[str] = field(default_factory=list)   # lesson ids
    lesson_best_score: Dict[str, int] = field(default_factory=dict)  # id -> 0/1
    theme: str = "dark"
    active_track: str = ""
    unlocked_tracks: List[str] = field(default_factory=lambda: ["networking"])
    hearts: int = 5
    hearts_last_refill: float = field(default_factory=lambda: time.time())

    # ---- derived helpers -------------------------------------------------
    def completed_set(self) -> Set[str]:
        return set(self.completed_lessons)

    def is_completed(self, lesson_id: str) -> bool:
        return lesson_id in self.completed_lessons

    def mark_completed(self, lesson_id: str, xp_reward: int, correct: bool) -> None:
        if lesson_id not in self.completed_lessons:
            self.completed_lessons.append(lesson_id)
        if correct:
            self.xp += xp_reward
            self.lesson_best_score[lesson_id] = 1
        else:
            # still small xp for attempting, encourages retrying without punishing
            self.xp += max(1, xp_reward // 4)
            self.lesson_best_score.setdefault(lesson_id, 0)
        self._touch_streak()

    def _touch_streak(self) -> None:
        today = time.strftime("%Y-%m-%d")
        if self.last_active_date == today:
            return
        if self.last_active_date:
            try:
                last = time.strptime(self.last_active_date, "%Y-%m-%d")
                last_epoch = time.mktime(last)
                today_epoch = time.mktime(time.strptime(today, "%Y-%m-%d"))
                gap_days = round((today_epoch - last_epoch) / 86400)
            except ValueError:
                gap_days = 999
            if gap_days == 1:
                self.streak += 1
            elif gap_days > 1:
                self.streak = 1
            # gap_days == 0 handled above
        else:
            self.streak = 1
        self.last_active_date = today

    def unlock_track(self, track_id: str) -> None:
        if track_id not in self.unlocked_tracks:
            self.unlocked_tracks.append(track_id)

    def refill_hearts_if_needed(self) -> None:
        """One heart regenerates every 20 minutes, capped at 5. Hearts only
        gate 'accuracy mode'; they never block a player from continuing to
        learn (see app.py) -- they're a light game-feel layer, not a paywall."""
        now = time.time()
        elapsed = now - self.hearts_last_refill
        regen_seconds = 20 * 60
        if self.hearts < 5 and elapsed >= regen_seconds:
            gained = int(elapsed // regen_seconds)
            self.hearts = min(5, self.hearts + gained)
            self.hearts_last_refill = now
        elif self.hearts >= 5:
            self.hearts_last_refill = now

    def lose_heart(self) -> None:
        self.hearts = max(0, self.hearts - 1)

    def track_progress(self, lesson_ids: List[str]) -> float:
        if not lesson_ids:
            return 0.0
        done = sum(1 for lid in lesson_ids if self.is_completed(lid))
        return done / len(lesson_ids)


def load() -> Progress:
    f = _data_file()
    if not f.exists():
        return Progress()
    try:
        raw = json.loads(f.read_text(encoding="utf-8"))
        known = {k: v for k, v in raw.items() if k in Progress.__dataclass_fields__}
        return Progress(**known)
    except (json.JSONDecodeError, TypeError, OSError):
        # Corrupted file -> back it up and start fresh rather than crash.
        try:
            f.rename(f.with_suffix(".corrupt.json"))
        except OSError:
            pass
        return Progress()


def save(progress: Progress) -> None:
    f = _data_file()
    tmp = f.with_suffix(".tmp")
    tmp.write_text(json.dumps(asdict(progress), indent=2), encoding="utf-8")
    os.replace(tmp, f)  # atomic on POSIX and Windows
