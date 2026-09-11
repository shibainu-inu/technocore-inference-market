import hashlib
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import prosody as P  # noqa: E402
import sonnet_validate as sv  # noqa: E402  (via prosody's sys.path insertion)

LEX = P.lexicon()
PRONS = P.prons()
EXAMPLE = (HERE / "format-poem.txt").read_text(encoding="utf-8")
EXAMPLE_LINES = [l for l in EXAMPLE.splitlines() if l.strip()]

SYNTH = [
    "The morning lays its gold upon the stone,",
    "And wakes the fields beneath a silver sky.",
    "I walk the path that once I walked alone,",
    "And watch the last of night's pale shadows die.",
    "Your voice returns within the waking light,",
    "A song the patient river seems to know.",
    "It keeps a little warmth against the night,",
    "And follows where the quiet waters flow.",
    "The years may take the roses from the wall,",
    "And leave the gate to rust beneath the rain.",
    "Yet still I turn whenever sparrows call,",
    "As though your step might cross the path again.",
    "What time has taken, words can hold in trust;",
    "A breath of love can rise above the dust.",
]


class Syllables(unittest.TestCase):
    def test_matches_official(self):
        for w in ["the", "today", "compare", "summer's", "extraterrestrial"]:
            self.assertEqual(P.line_syllables([w]), sv.word_syllables(w, LEX))

    def test_unknown_raises(self):
        with self.assertRaises(ValueError):
            P.line_syllables(["zzzqqq"])


class Stress(unittest.TestCase):
    def test_today(self):
        self.assertIn((0, 1), P.stress_patterns("today"))

    def test_iambic_line(self):
        line = "Shall I compare thee to a summer's day"
        self.assertGreaterEqual(P.iambic_fit(P.split_words(line)), 0.8)

    def test_trochaic_line_scores_lower(self):
        iambic = P.iambic_fit(P.split_words("Shall I compare thee to a summer's day"))
        trochaic = P.iambic_fit(P.split_words("Tiger tiger burning bright forest"))
        self.assertLess(trochaic, iambic)


class Rhyme(unittest.TestCase):
    def test_rhymes(self):
        self.assertTrue(P.rhymes("day", "away"))
        self.assertTrue(P.rhymes("stone,", "alone"))
        self.assertFalse(P.rhymes("day", "dog"))
        self.assertFalse(P.rhymes("day", "Day."))

    def test_report(self):
        r = P.rhyme_report(SYNTH)
        self.assertTrue(r["all_pairs_rhyme"], r)
        self.assertTrue(r["families_distinct"], r)
        self.assertEqual(r["end_words"][0], "stone")


class Canonical(unittest.TestCase):
    def test_text_and_hash(self):
        text = P.canonical_text(EXAMPLE_LINES)
        expected = "\n".join(EXAMPLE_LINES[0:4]) + "\n\n" + "\n".join(EXAMPLE_LINES[4:8]) + "\n\n" \
            + "\n".join(EXAMPLE_LINES[8:12]) + "\n\n" + "\n".join(EXAMPLE_LINES[12:14])
        self.assertEqual(text, expected)
        self.assertFalse(text.endswith("\n"))
        self.assertEqual(P.poem_sha256(EXAMPLE_LINES), hashlib.sha256(expected.encode()).hexdigest())

    def test_official_validator_accepts_example(self):
        counts = sv.validate_poem(EXAMPLE, LEX, exact_ten=True)
        self.assertEqual(counts, [10] * 14)


class Candidates(unittest.TestCase):
    def test_letters_respected(self):
        allowed = P.did_letters("did:key:z6MkmG1MiumCr8Jk6vL5qt2A1XzEst6CVT5rwRHUHYwKPvqA")
        self.assertEqual(sorted(set("abcdefghijklmnopqrstuvwxyz") - allowed), list("bfno"))
        words = P.candidates(None, allowed, 2)
        self.assertTrue(words)
        for w in words:
            self.assertTrue(P.word_letters(w) <= allowed, w)
            self.assertLessEqual(LEX[w], 2)

    def test_stress_and_rhyme_filters(self):
        allowed = set("abcdefghijklmnopqrstuvwxyz")
        words = P.candidates(None, allowed, 2, need_stress=(0, 1), rhyme_with="day")
        self.assertIn("away", words)
        self.assertNotIn("day", words)
        for w in words:
            self.assertIn((0, 1), P.stress_patterns(w))
            self.assertTrue(P.rhymes(w, "day"))


if __name__ == "__main__":
    unittest.main()
