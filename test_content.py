"""
test_content.py
Pure-stdlib sanity tests for lesson content and progress logic.
Deliberately does NOT import tkinter/app.py, so this runs anywhere,
including headless CI, with just:  python -m unittest test_content.py
"""

import tempfile
import unittest
from pathlib import Path
from unittest import mock

import content
import progress as progress_mod
import theme as theme_mod


class TestContentIntegrity(unittest.TestCase):
    def test_every_track_has_chapters_and_lessons(self):
        for track_id, track in content.TRACKS.items():
            self.assertTrue(track["chapters"], f"{track_id} has no chapters")
            for chapter in track["chapters"]:
                self.assertTrue(
                    chapter["lessons"], f"{track_id}/{chapter['id']} has no lessons"
                )

    def test_lesson_ids_are_globally_unique(self):
        ids = []
        for track in content.TRACKS.values():
            for chapter in track["chapters"]:
                for lesson in chapter["lessons"]:
                    ids.append(lesson["id"])
        self.assertEqual(len(ids), len(set(ids)), "duplicate lesson id found")

    def test_chapter_ids_unique_within_track(self):
        for track_id, track in content.TRACKS.items():
            chap_ids = [c["id"] for c in track["chapters"]]
            self.assertEqual(len(chap_ids), len(set(chap_ids)), track_id)

    def test_every_lesson_has_required_fields(self):
        required = {"id", "title", "minute", "question", "choices",
                    "correct", "explain", "xp"}
        for track in content.TRACKS.values():
            for chapter in track["chapters"]:
                for lesson in chapter["lessons"]:
                    missing = required - lesson.keys()
                    self.assertFalse(missing, f"{lesson.get('id')} missing {missing}")

    def test_correct_index_is_valid(self):
        for track in content.TRACKS.values():
            for chapter in track["chapters"]:
                for lesson in chapter["lessons"]:
                    self.assertTrue(
                        0 <= lesson["correct"] < len(lesson["choices"]),
                        f"{lesson['id']} has an out-of-range correct index",
                    )

    def test_at_least_two_choices_per_question(self):
        for track in content.TRACKS.values():
            for chapter in track["chapters"]:
                for lesson in chapter["lessons"]:
                    self.assertGreaterEqual(len(lesson["choices"]), 2, lesson["id"])

    def test_no_empty_strings_in_core_fields(self):
        for track in content.TRACKS.values():
            for chapter in track["chapters"]:
                for lesson in chapter["lessons"]:
                    for field in ("title", "minute", "question", "explain"):
                        self.assertTrue(lesson[field].strip(), f"{lesson['id']}.{field}")

    def test_find_lesson_roundtrip(self):
        for track_id, track in content.TRACKS.items():
            for chapter in track["chapters"]:
                for lesson in chapter["lessons"]:
                    found_track, found_chapter, found_lesson = content.find_lesson(
                        lesson["id"]
                    )
                    self.assertEqual(found_track, track_id)
                    self.assertEqual(found_chapter, chapter["id"])
                    self.assertEqual(found_lesson["id"], lesson["id"])

    def test_find_lesson_missing_returns_none(self):
        t, c, l = content.find_lesson("this_id_does_not_exist")
        self.assertIsNone(t)
        self.assertIsNone(c)
        self.assertIsNone(l)

    def test_total_lesson_count_matches_sum(self):
        total = sum(
            len(content.all_lesson_ids_for_track(tid)) for tid in content.TRACKS
        )
        self.assertEqual(total, content.total_lesson_count())

    def test_every_track_has_a_style_entry(self):
        for track_id in content.TRACKS:
            self.assertIn(track_id, theme_mod.TRACK_STYLE, track_id)


class TestProgress(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self._home_patch = mock.patch(
            "progress.Path.home", return_value=Path(self.tmpdir.name)
        )
        self._home_patch.start()

    def tearDown(self):
        self._home_patch.stop()
        self.tmpdir.cleanup()

    def test_fresh_progress_defaults(self):
        p = progress_mod.Progress()
        self.assertEqual(p.xp, 0)
        self.assertEqual(p.streak, 0)
        self.assertEqual(p.hearts, 5)
        self.assertEqual(p.completed_lessons, [])

    def test_mark_completed_correct_awards_full_xp(self):
        p = progress_mod.Progress()
        p.mark_completed("net_01_01", 10, correct=True)
        self.assertEqual(p.xp, 10)
        self.assertTrue(p.is_completed("net_01_01"))
        self.assertEqual(p.lesson_best_score["net_01_01"], 1)

    def test_mark_completed_incorrect_awards_partial_xp(self):
        p = progress_mod.Progress()
        p.mark_completed("net_01_01", 10, correct=False)
        self.assertEqual(p.xp, 2)  # max(1, 10 // 4)
        self.assertTrue(p.is_completed("net_01_01"))
        self.assertEqual(p.lesson_best_score["net_01_01"], 0)

    def test_completing_same_lesson_twice_does_not_duplicate_id(self):
        p = progress_mod.Progress()
        p.mark_completed("net_01_01", 10, correct=True)
        p.mark_completed("net_01_01", 10, correct=True)
        self.assertEqual(p.completed_lessons.count("net_01_01"), 1)

    def test_track_progress_fraction(self):
        p = progress_mod.Progress()
        ids = ["a", "b", "c", "d"]
        p.mark_completed("a", 10, True)
        p.mark_completed("b", 10, True)
        self.assertAlmostEqual(p.track_progress(ids), 0.5)

    def test_track_progress_empty_list_is_zero(self):
        p = progress_mod.Progress()
        self.assertEqual(p.track_progress([]), 0.0)

    def test_save_and_load_roundtrip(self):
        p = progress_mod.Progress()
        p.mark_completed("py_01_01", 10, True)
        p.xp = 42
        p.streak = 3
        progress_mod.save(p)

        loaded = progress_mod.load()
        self.assertEqual(loaded.xp, 42)
        self.assertEqual(loaded.streak, 3)
        self.assertTrue(loaded.is_completed("py_01_01"))

    def test_load_with_no_file_returns_fresh_progress(self):
        p = progress_mod.load()
        self.assertEqual(p.xp, 0)

    def test_load_with_corrupted_file_recovers(self):
        data_dir = Path(self.tmpdir.name) / ".cyberlearn"
        data_dir.mkdir(parents=True, exist_ok=True)
        (data_dir / "progress.json").write_text("{not valid json", encoding="utf-8")
        p = progress_mod.load()
        self.assertEqual(p.xp, 0)  # recovered gracefully, not crashed

    def test_hearts_never_go_negative(self):
        p = progress_mod.Progress()
        for _ in range(10):
            p.lose_heart()
        self.assertEqual(p.hearts, 0)

    def test_hearts_cap_at_five(self):
        p = progress_mod.Progress(hearts=5)
        p.hearts_last_refill = 0  # force "a long time ago"
        p.refill_hearts_if_needed()
        self.assertLessEqual(p.hearts, 5)


class TestTheme(unittest.TestCase):
    def test_rank_for_xp_starts_at_zero(self):
        threshold, name, icon = theme_mod.rank_for_xp(0)
        self.assertEqual(threshold, 0)

    def test_rank_for_xp_increases_with_xp(self):
        _, low_name, _ = theme_mod.rank_for_xp(0)
        _, high_name, _ = theme_mod.rank_for_xp(999999)
        self.assertNotEqual(low_name, high_name)

    def test_both_themes_define_same_fields(self):
        dark_fields = set(theme_mod.DARK.__dataclass_fields__)
        light_fields = set(theme_mod.LIGHT.__dataclass_fields__)
        self.assertEqual(dark_fields, light_fields)


if __name__ == "__main__":
    unittest.main()
