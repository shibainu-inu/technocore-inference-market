"""Deterministic template/slot line generator (the LLM-free ``CreativeEngine``).

Design
------
* A small curated vocabulary (every word verified against the frozen dictionary at start-up) is
  split into part-of-speech pools. Templates are slot sequences (``DET ADJ NOUN VERBS PREP DET
  NOUN END``); a seeded depth-first fill picks words so the official syllable total equals the
  requested budget exactly.
* Any *suffix* of a template is also a template, so a partially written line (accepted prefix
  ending mid-line) can be completed with a fragment of any syllable budget.
* Hard constraints: every word's letters ⊆ ``ctx.allowed_letters``; the end word rhymes with the
  required key (candidates come from ``lexicon.candidates(rhyme_with=...)``); end words never
  repeat and, for a line that opens a new rhyme family, never share a rhyme key with an existing
  family (``ctx.forbidden_end_words``).
* Soft preferences (the ranking inside the fill): curated words before dictionary fallbacks,
  words spellable by ≥ 2 writers ("two-key rule"), stress that fits the iambic template at the
  current position, and end words that still have curated rhyme partners under the allowed letters.

Every choice goes through one ``random.Random(seed)``; the same seed and context give the same
candidates. ``LineCandidate.score`` is *higher = better*.
"""
from __future__ import annotations

import random
from typing import Iterable, Optional, Sequence

from ..lexicon.core import IAMBIC, Lexicon, bare
from .engine import CreativeEngine, LineCandidate, LineContext

# ------------------------------------------------------------------ vocabulary
VOCABULARY: dict[str, tuple[str, ...]] = {
    "DET": ("the", "a", "my", "his", "her", "our", "your", "their", "this", "that", "each", "no", "some", "one",
            "any", "many"),
    "NOUN": (
        "sea", "sky", "night", "day", "light", "dark", "wind", "rain", "snow", "sun", "moon", "star", "stone", "road",
        "hill", "field", "tree", "leaf", "bird", "song", "heart", "hand", "eye", "face", "voice", "dream", "sleep",
        "fire", "water", "river", "garden", "window", "morning", "evening", "winter", "summer", "shadow", "silence",
        "mother", "father", "child", "house", "door", "wall", "bed", "boat", "ship", "tide", "wave", "shore", "sand",
        "salt", "bread", "tea", "cup", "chair", "table", "bell", "clock", "hour", "year", "time", "word", "name",
        "breath", "bone", "blood", "skin", "hair", "thread", "wool", "coat", "lamp", "glass", "mirror", "letter",
        "page", "book", "ink", "pen", "path", "gate", "bridge", "city", "town", "street", "ground", "earth", "grass",
        "flower", "rose", "apple", "seed", "root", "branch", "fog", "mist", "cloud", "frost", "ice", "flame", "ash",
        "smoke", "dust", "air", "grief", "hope", "fear", "love", "peace", "truth", "fate", "soul", "ghost", "king",
        "queen", "friend", "stranger", "sailor", "farmer", "ladder", "harvest", "orchard", "meadow", "valley",
        "mountain", "forest", "ocean", "island", "harbor", "candle", "kettle", "pillow", "blanket", "cradle", "ribbon",
        "needle", "hammer", "wagon", "saddle", "horse", "dog", "cat", "lamb", "wolf", "crow", "sparrow", "swallow",
        "robin", "thrush", "salmon", "trout", "whale", "hay", "dawn", "lawn", "deck", "pier", "arm", "chest", "key",
        "line", "sail", "rope", "net", "well", "spring", "lake", "pond", "moss", "fern", "oak", "pine", "elm", "nest",
        "wing", "feather", "shell", "pearl", "gold", "silver", "iron", "steel", "coin", "ring", "bead", "veil", "silk",
        "milk", "wine", "meal", "plate", "spoon", "knife", "loaf", "grain", "corn", "wheat", "mill", "barn", "roof",
        "floor", "stair", "hall", "room", "yard", "fence", "lane", "gap", "edge", "end", "start", "sign", "mark",
        "trace", "map", "ache", "pain", "tear", "smile", "laugh", "sigh", "cry", "prayer", "hymn", "tune", "drum",
        "flute", "harp", "string", "sound", "echo", "thunder", "lightning", "storm", "breeze", "gale", "heat", "cold",
        "dusk", "noon", "midnight", "season", "autumn", "april", "june", "week", "moment", "minute", "second", "age",
        "past", "future", "memory", "story", "secret", "answer", "question", "reason", "promise", "lesson", "burden",
        "blessing", "sorrow", "wonder", "danger", "shelter", "journey", "distance", "border", "country", "village",
        "kingdom", "temple", "tower", "castle", "chapel", "ruin", "pebble", "gravel", "boulder", "canyon",
        "desert", "prairie", "tundra", "glacier", "willow", "cedar", "maple", "birch", "clover", "lily", "daisy",
        "tulip", "poppy", "ivy", "reed", "rush", "thorn", "berry", "cherry", "plum", "peach", "pear", "lemon", "honey",
        "butter", "sugar", "pepper", "cabbage", "onion", "carrot", "potato", "turnip", "bean", "pea", "rice", "bowl",
        "jar", "jug", "pot", "pan", "fork", "basket", "bucket", "barrel", "cart", "wheel", "axle", "yoke", "plow",
        "scythe", "sickle", "spade", "rake", "hoe", "seedling", "sapling", "timber", "plank", "beam", "nail", "hinge",
        "latch", "lock", "bolt", "chain", "anchor", "mast", "hull", "oar", "paddle", "canoe", "raft", "ferry",
        "lighthouse", "beacon", "signal", "whistle", "horn", "trumpet", "banner", "flag", "crown", "throne", "sword",
        "shield", "spear", "arrow", "bow", "helmet", "armor", "cloak", "hood", "glove", "boot", "shoe", "sock", "hat",
        "cap", "scarf", "shawl", "gown", "dress", "shirt", "belt", "button", "pocket", "purse", "wallet", "ticket",
        "family", "history", "mystery", "melody", "energy", "enemy", "century", "liberty", "misery", "tapestry",
        "majesty", "gallery", "library", "destiny", "remedy", "medicine", "lullaby", "butterfly", "firefly",
        "hurricane", "avenue", "cathedral", "umbrella", "lavender", "calendar", "wilderness", "tenderness",
        "emptiness", "happiness", "bitterness", "eternity", "infinity", "ceremony", "sanctuary",
    ),
    "ADJ": (
        "cold", "warm", "dark", "bright", "deep", "high", "low", "slow", "soft", "hard", "thin", "wide", "small", "tall",
        "long", "short", "old", "young", "new", "late", "pale", "red", "green", "blue", "gray", "gold", "black", "white",
        "still", "quiet", "silent", "hollow", "heavy", "gentle", "bitter", "sweet", "wild", "calm", "kind", "brave",
        "weary", "lonely", "distant", "hidden", "broken", "faded", "silver", "golden", "empty", "narrow", "open",
        "early", "tender", "patient", "ancient", "simple", "humble", "sudden", "secret", "sacred", "bare", "thick",
        "sharp", "dull", "wet", "dry", "clean", "plain", "grey", "brown", "dim", "faint", "clear", "true", "free",
        "lost", "last", "first", "whole", "half", "full", "good", "bad", "sad", "glad", "mild", "fierce", "steep",
        "flat", "round", "square", "rough", "smooth", "loud", "hushed", "frozen", "burning", "shining", "rising",
        "falling", "waking", "sleeping", "living", "dying", "little", "eager", "idle", "nimble", "clever",
        "honest", "foolish", "noble", "royal", "common", "holy", "happy", "hungry", "thirsty",
        "certain", "careful", "endless", "restless", "ruthless", "hopeless", "helpless", "harmless", "silken",
        "wooden", "leaden", "molten", "swollen", "sunken", "shaken", "spoken", "chosen", "woven",
        "beautiful", "terrible", "delicate", "different", "difficult", "familiar", "infinite", "innocent",
        "merciful", "natural", "radiant", "silvery", "tremendous", "uncertain", "weathered", "faithful", "distant",
        "invisible", "unbearable", "unbroken", "unfinished", "unspoken", "unwritten", "everlasting",
    ),
    "VERBS": (   # 3rd person singular present
        "keeps", "holds", "waits", "sleeps", "wakes", "falls", "rises", "turns", "burns", "calls", "sings", "breaks",
        "bends", "folds", "fills", "moves", "goes", "comes", "stays", "leaves", "finds", "loses", "knows", "sees",
        "hears", "feels", "brings", "takes", "gives", "opens", "closes", "carries", "follows", "remembers", "forgets",
        "gathers", "answers", "whispers", "wanders", "settles", "lingers", "drifts", "climbs",
        "counts", "lifts", "pours", "spills", "shines", "fades", "grows", "dies", "lives", "learns", "wears",
        "meets", "hits", "sets", "lets", "runs", "walks", "stands", "sits", "lies", "hides", "seeks", "reads", "writes",
        "speaks", "sends", "spends", "lends", "builds", "binds", "winds", "blows", "flows", "glows", "throws",
        "sows", "reaps", "sweeps", "creeps", "weeps", "leaps", "melts", "hangs", "rings", "swings", "clings",
        "beats", "heats", "eats", "greets", "paints", "plants", "wants", "hunts", "tends", "ends", "begins",
        "returns", "recalls", "forgives", "believes", "receives", "prepares", "repairs", "declares",
        "arrives", "survives", "reveals", "conceals", "repeats", "retreats", "unfolds", "awaits",
    ),
    "VERBP": (   # past tense
        "kept", "held", "waited", "slept", "woke", "fell", "rose", "turned", "burned", "called", "sang", "broke",
        "bent", "folded", "filled", "moved", "went", "came", "stayed", "left", "found", "lost", "knew", "saw", "heard",
        "felt", "brought", "took", "gave", "opened", "closed", "carried", "followed", "remembered", "forgot",
        "gathered", "scattered", "answered", "whispered", "wandered", "settled", "lingered", "trembled", "drifted",
        "climbed", "counted", "mended", "lifted", "poured", "spilled", "shone", "faded", "grew", "died", "lived",
        "learned", "wore", "met", "hit", "set", "let", "ran", "walked", "stood", "sat", "lay", "hid", "sought", "read",
        "wrote", "spoke", "sent", "spent", "lent", "built", "bound", "wound", "blew", "flew", "threw", "swept",
        "crept", "wept", "leapt", "melted", "hung", "rang", "swung", "clung", "beat", "ate", "greeted", "painted",
        "planted", "wanted", "hunted", "tended", "ended", "began", "returned", "recalled", "forgave", "believed",
        "received", "prepared", "repaired", "declared", "arrived", "survived", "revealed", "concealed", "repeated",
        "retreated", "unfolded", "beheld", "awaited", "fed", "led", "bled", "shed", "sped", "fled", "bred", "made",
    ),
    "VERBB": (   # base form (after I / we / you / they / modal)
        "keep", "hold", "wait", "sleep", "wake", "fall", "rise", "turn", "burn", "call", "sing", "break", "bend",
        "fold", "fill", "move", "go", "come", "stay", "leave", "find", "lose", "know", "see", "hear", "feel", "bring",
        "take", "give", "open", "close", "carry", "follow", "remember", "forget", "gather", "scatter", "answer",
        "whisper", "wander", "settle", "linger", "tremble", "drift", "climb", "count", "mend", "lift", "pour", "spill",
        "shine", "fade", "grow", "die", "live", "learn", "wear", "meet", "hit", "set", "let", "run", "walk", "stand",
        "sit", "lie", "hide", "seek", "read", "write", "speak", "send", "spend", "lend", "build", "bind", "wind",
        "blow", "flow", "glow", "throw", "sow", "reap", "sweep", "creep", "weep", "leap", "melt", "hang", "ring",
        "swing", "cling", "beat", "eat", "greet", "paint", "plant", "want", "hunt", "tend", "end", "begin", "return",
        "recall", "forgive", "believe", "receive", "prepare", "repair", "declare", "arrive", "survive", "reveal",
        "conceal", "repeat", "retreat", "unfold", "behold", "await", "defy", "deny", "reply", "rely", "make", "try",
    ),
    "ADV": (
        "slowly", "softly", "gently", "quietly", "again", "alone", "away", "still", "then", "now", "here", "there",
        "always", "never", "once", "soon", "late", "long", "far", "near", "below", "above", "within", "beyond",
        "tonight", "today", "twice", "well", "home", "back", "down", "up", "out", "in", "on", "forever", "apart",
        "aside", "along", "ahead", "behind", "inside", "outside", "somewhere", "nowhere", "anywhere", "yesterday",
        "tomorrow", "early", "lately", "rarely", "barely", "nearly", "wholly", "deeply", "brightly", "darkly",
        "sweetly", "sadly", "gladly", "wildly", "calmly", "kindly", "boldly", "coldly", "warmly", "plainly",
    ),
    "PREP": (
        "in", "on", "at", "by", "to", "from", "with", "of", "through", "under", "over", "beyond", "beneath", "below",
        "above", "across", "along", "among", "between", "into", "upon", "near", "past", "toward", "without", "within",
        "against", "around", "behind", "beside", "inside", "like", "till", "until", "after", "before", "down", "off",
    ),
    "PRON": ("i", "we", "you", "they"),
    "PRON3": ("he", "she", "it"),
    "CONJ": ("and", "but", "or", "yet", "so", "when", "while", "as", "if", "though", "till", "until", "before", "after",
             "where", "since", "then", "for", "nor", "that"),
    "MODAL": ("will", "can", "may", "must", "shall", "might", "could", "would", "should"),
}

# Slot sequences; the last slot is always the end-of-line slot ("END:<category>" = category when the line is free).
TEMPLATES: tuple[tuple[str, ...], ...] = (
    ("DET", "ADJ", "NOUN", "VERBS", "PREP", "DET", "ADJ", "END:NOUN"),
    ("DET", "NOUN", "VERBS", "ADV", "PREP", "DET", "END:NOUN"),
    ("DET", "ADJ", "NOUN", "PREP", "DET", "NOUN", "VERBS", "END:ADV"),
    ("DET", "NOUN", "CONJ", "DET", "NOUN", "VERBP", "DET", "END:NOUN"),
    ("DET", "NOUN", "VERBP", "PREP", "DET", "ADJ", "END:NOUN"),
    ("DET", "ADJ", "NOUN", "VERBP", "CONJ", "DET", "NOUN", "END:VERBP"),
    ("PRON", "VERBB", "DET", "NOUN", "CONJ", "VERBB", "DET", "END:NOUN"),
    ("PRON", "VERBP", "DET", "NOUN", "PREP", "DET", "ADJ", "END:NOUN"),
    ("PRON", "VERBP", "ADV", "CONJ", "DET", "NOUN", "END:VERBP"),
    ("PRON", "MODAL", "VERBB", "DET", "NOUN", "PREP", "DET", "END:NOUN"),
    ("PRON", "MODAL", "VERBB", "DET", "ADJ", "NOUN", "END:ADV"),
    ("PRON3", "VERBS", "DET", "NOUN", "PREP", "DET", "ADJ", "END:NOUN"),
    ("PRON3", "VERBP", "DET", "ADJ", "NOUN", "CONJ", "DET", "END:NOUN"),
    ("CONJ", "DET", "NOUN", "VERBS", "PRON", "VERBB", "DET", "END:NOUN"),
    ("CONJ", "DET", "ADJ", "NOUN", "VERBP", "DET", "END:NOUN"),
    ("ADV", "DET", "NOUN", "VERBS", "CONJ", "DET", "NOUN", "END:VERBS"),
    ("PREP", "DET", "ADJ", "NOUN", "DET", "NOUN", "VERBS", "END:ADV"),
    ("PREP", "DET", "NOUN", "PRON", "VERBP", "DET", "ADJ", "END:NOUN"),
    ("DET", "NOUN", "PRON", "VERBP", "VERBS", "PREP", "DET", "END:NOUN"),
    ("DET", "NOUN", "VERBS", "CONJ", "DET", "NOUN", "VERBS", "END:ADV"),
    ("PRON", "VERBB", "DET", "NOUN", "PRON", "VERBB", "DET", "END:NOUN"),
    ("DET", "ADJ", "ADJ", "NOUN", "VERBS", "PREP", "DET", "END:NOUN"),
)

END_CATEGORIES = ("NOUN", "VERBP", "VERBS", "VERBB", "ADJ", "ADV")

# Ranking knobs (documented constants; Settings has no creative section).
TOP_CHOICES = 6               # sample among the best-ranked words to keep candidates diverse
ONE_KEY_PENALTY = 0.75        # per word spellable by < 2 writers
NO_PARTNER_PENALTY = 3.0      # end word that leaves no curated rhyme partner (only when the line opens a family)
METER_WEIGHT = 1.0            # per mismatched metrical position
MIN_RHYME_PARTNERS = 2        # curated partners wanted under the allowed letters when a line opens a family
FILL_ATTEMPTS_PER_CANDIDATE = 3
MAX_FALLBACK_END_WORDS = 400  # cap when the curated pool has no rhyme and we dip into the full dictionary
_INF = 10 ** 6
VOWEL_LETTERS = "aeiou"


class HeuristicCreativeEngine(CreativeEngine):
    """Template/slot line generator; see module docstring."""

    def __init__(self, lexicon: Lexicon, seed: Optional[int] = None):
        self.lexicon = lexicon
        self.seed = seed
        self.rng = random.Random(seed)
        self.pools: dict[str, list[str]] = {}
        self.category_of: dict[str, str] = {}
        for cat, words in VOCABULARY.items():
            keep: list[str] = []
            for w in words:
                if w in lexicon and w not in keep:
                    keep.append(w)
            self.pools[cat] = keep
            for w in keep:
                self.category_of.setdefault(w, cat)
        self.vocab: list[str] = sorted({w for ws in self.pools.values() for w in ws})
        self._vocab_set = set(self.vocab)
        self.end_pool: list[str] = sorted({w for c in END_CATEGORIES for w in self.pools[c]})
        # per-word caches (lexicon is frozen, so these never change)
        self._syl: dict[str, int] = {}
        self._letters: dict[str, frozenset] = {}
        self._fit: dict[tuple[str, int], bool] = {}
        for w in self.vocab:
            self._word(w)
        self._pool_cache: dict[tuple[frozenset, str], list[str]] = {}
        self._range_cache: dict[tuple[frozenset, str], tuple[int, int]] = {}
        self._rhyme_cache: dict[tuple[str, frozenset], tuple[list[str], list[str]]] = {}
        self._family_block_cache: dict[frozenset, frozenset] = {}
        self._rank_cache: dict[tuple, list[list[str]]] = {}     # reset per propose_lines call

    # ------------------------------------------------------------ determinism
    def reseed(self, seed: Optional[int]) -> None:
        self.seed = seed
        self.rng = random.Random(seed)

    # ------------------------------------------------------------ per-word facts
    def _word(self, w: str) -> int:
        n = self._syl.get(w)
        if n is None:
            info = self.lexicon.info(w)
            n = info.syllables
            self._syl[w] = n
            self._letters[w] = info.letters
        return n

    def _fits(self, w: str, pos: int) -> bool:
        key = (w, pos)
        f = self._fit.get(key)
        if f is None:
            info = self.lexicon.info(w)
            n = info.syllables
            pats = [p for p in info.stresses if len(p) == n] or list(info.stresses)
            f = False
            for pat in pats:
                ok = True
                for j, st in enumerate(pat):
                    k = pos + j
                    if k >= len(IAMBIC):
                        break
                    if not (len(pat) == 1 or st == 2 or st == IAMBIC[k]):
                        ok = False
                        break
                if ok:
                    f = True
                    break
            self._fit[key] = f
        return f

    # ------------------------------------------------------------ pools
    def _pool(self, cat: str, allowed: frozenset) -> list[str]:
        key = (allowed, cat)
        p = self._pool_cache.get(key)
        if p is None:
            p = [w for w in self.pools.get(cat, []) if self._letters[w] <= allowed]
            self._pool_cache[key] = p
        return p

    def _range(self, cat: str, allowed: frozenset) -> tuple[int, int]:
        key = (allowed, cat)
        r = self._range_cache.get(key)
        if r is None:
            p = self._pool(cat, allowed)
            r = (min(self._syl[w] for w in p), max(self._syl[w] for w in p)) if p else (_INF, -1)
            self._range_cache[key] = r
        return r

    def _rhyme_split(self, rhyme_key: str, allowed: frozenset) -> tuple[list[str], list[str]]:
        """(curated, dictionary-fallback) words rhyming with ``rhyme_key`` spellable from ``allowed``."""
        ck = (rhyme_key, allowed)
        cached = self._rhyme_cache.get(ck)
        if cached is None:
            lex = self.lexicon
            if rhyme_key in lex:
                full = lex.candidates(allowed, 10, rhyme_with=rhyme_key)
            else:
                full = [w for w in lex.by_rhyme(rhyme_key) if lex.info(w).letters <= allowed]
            good = [w for w in full if w in self._vocab_set]
            rest = [w for w in full if w not in self._vocab_set and len(w) >= 3 and "'" not in w][:MAX_FALLBACK_END_WORDS]
            for w in good + rest:
                self._word(w)
            cached = (good, rest)
            self._rhyme_cache[ck] = cached
        return cached

    def rhyme_candidates(self, rhyme_key: str, allowed: frozenset, max_syllables: int = 10) -> list[str]:
        """Words rhyming with ``rhyme_key`` (a word, or a phoneme key) spellable from ``allowed``.

        Curated-vocabulary hits come first (sorted), then the rest of the dictionary as a fallback.
        """
        good, rest = self._rhyme_split(rhyme_key, allowed)
        return [w for w in good + rest if self._syl[w] <= max_syllables]

    def _end_pool(self, rhyme_key: str, allowed: frozenset, budget: int, forbidden: set) -> list[str]:
        """Best non-empty tier of rhyming end words: curated content words > other curated > dictionary."""
        good, rest = self._rhyme_split(rhyme_key, allowed)
        ok = lambda w: self._syl[w] <= budget and w not in forbidden  # noqa: E731
        content = [w for w in good if ok(w) and self.category_of.get(w) in END_CATEGORIES]
        if content:
            return content
        other = [w for w in good if ok(w)]
        if other:
            return other
        return [w for w in rest if ok(w)]

    def _curated_partners(self, word: str, allowed: frozenset) -> int:
        return len(self._rhyme_split(word, allowed)[0])

    def _forbidden_keys(self, forbidden_end_words: Iterable[str]) -> frozenset:
        keys: set[str] = set()
        for w in forbidden_end_words:
            try:
                keys |= set(self.lexicon.rhyme_keys(w))
            except ValueError:
                continue
        return frozenset(keys)

    def _family_blocked(self, forbidden_keys: frozenset) -> frozenset:
        """Curated end words that would clash with an existing rhyme family."""
        b = self._family_block_cache.get(forbidden_keys)
        if b is None:
            lex = self.lexicon
            b = frozenset(w for w in self.end_pool if lex.rhyme_keys(w) & forbidden_keys)
            self._family_block_cache[forbidden_keys] = b
        return b

    # ------------------------------------------------------------ ranking helpers
    def _keys_of(self, per_writer: dict, words: Iterable[str]) -> dict[str, int]:
        sets = [frozenset(ls) for ls in per_writer.values()]
        out: dict[str, int] = {}
        for w in words:
            if w not in out:
                letters = self._letters[w]
                out[w] = sum(1 for ls in sets if letters <= ls)
        return out

    def _ranked(self, pool_key: tuple, pool: list[str], pos: int, keys: dict[str, int]) -> list[list[str]]:
        """Per-call cache: pool words bucketed into tiers (two-key+fit, two-key, one-key+fit, one-key), each shuffled."""
        ck = (pool_key, pos)
        tiers = self._rank_cache.get(ck)
        if tiers is None:
            tiers = [[], [], [], []]
            for w in pool:
                t = (2 if keys.get(w, 2) < 2 else 0) + (0 if self._fits(w, pos) else 1)
                tiers[t].append(w)
            for tier in tiers:
                self.rng.shuffle(tier)
            self._rank_cache[ck] = tiers
        return tiers

    def _pick(self, tiers: list[list[str]], eligible, curated_first: bool) -> Optional[str]:
        """Sample among the first TOP_CHOICES eligible words of the best group (random scan offset per pick).

        Group order: curated two-key > curated one-key (or, when no curated word is eligible, the same for
        dictionary fallbacks). Squared-uniform bias towards the front (fit-first) of the collected words.
        """
        vocab = self._vocab_set
        for want_curated in ((True, False) if curated_first else (None,)):
            for group in ((0, 1), (2, 3)):
                top: list[str] = []
                for t in group:
                    tier = tiers[t]
                    n = len(tier)
                    if not n:
                        continue
                    off = self.rng.randrange(n)
                    for j in range(n):
                        w = tier[(off + j) % n]
                        if want_curated is not None and (w in vocab) != want_curated:
                            continue
                        if eligible(w):
                            top.append(w)
                            if len(top) >= TOP_CHOICES:
                                break
                    if len(top) >= TOP_CHOICES:
                        break
                if top:
                    r = self.rng.random()
                    return top[int(r * r * len(top))]
        return None

    # ------------------------------------------------------------ filling
    def _fill(self, slots: Sequence[str], ranges: list[tuple[int, int]], budget: int, allowed: frozenset,
              keys: dict[str, int], start_pos: int, forbidden_ends: frozenset,
              end_pool: Optional[list[str]]) -> Optional[list[str]]:
        syl = self._syl
        out: list[str] = []
        used: set[str] = set()
        suffix_lo = [0] * (len(slots) + 1)
        suffix_hi = [0] * (len(slots) + 1)
        for i in range(len(slots) - 1, -1, -1):
            suffix_lo[i] = suffix_lo[i + 1] + ranges[i][0]
            suffix_hi[i] = suffix_hi[i + 1] + ranges[i][1]

        def rec(i: int, remaining: int, pos: int) -> bool:
            if i == len(slots):
                return remaining == 0
            lo, hi = suffix_lo[i + 1], suffix_hi[i + 1]
            slot = slots[i]
            is_end = slot.startswith("END:")
            if is_end and end_pool is not None:
                tiers = self._ranked(("END", id(end_pool)), end_pool, pos, keys)
            else:
                cat = slot[4:] if is_end else slot
                tiers = self._ranked((cat, allowed), self._pool(cat, allowed), pos, keys)
            after_a = bool(out) and out[-1] == "a"     # article agreement: "a" precedes a consonant-initial word
            rejected: set[str] = set()

            def eligible(w: str) -> bool:
                return (lo <= remaining - syl[w] <= hi and w not in used and w not in rejected
                        and not (is_end and w in forbidden_ends) and not (after_a and w[0] in VOWEL_LETTERS))

            for _ in range(3):
                w = self._pick(tiers, eligible, curated_first=is_end)
                if w is None:
                    return False
                out.append(w)
                used.add(w)
                if rec(i + 1, remaining - syl[w], pos + syl[w]):
                    return True
                out.pop()
                used.discard(w)
                rejected.add(w)
            return False

        return list(out) if rec(0, budget, start_pos) else None

    def _score(self, words: list[str], ctx: LineContext, keys: dict[str, int], start_pos: int, sets_key: bool) -> float:
        from ..planner.meter import stress_distance  # local import: planner depends on creative, not vice versa
        meter = stress_distance(words, self.lexicon, start_pos=start_pos)
        one_key = sum(1 for w in words if ctx.per_writer_letters and keys.get(w, 2) < 2)
        score = -METER_WEIGHT * meter - ONE_KEY_PENALTY * one_key
        if sets_key and self._curated_partners(words[-1], ctx.allowed_letters) < MIN_RHYME_PARTNERS:
            score -= NO_PARTNER_PENALTY
        return score

    # ------------------------------------------------------------ CreativeEngine API
    def propose_lines(self, ctx: LineContext) -> list[LineCandidate]:
        """Return up to ``ctx.max_candidates`` distinct fragments of exactly ``ctx.syllables`` syllables.

        ``ctx.syllables`` < 10 means "complete the current line": the fragment is scored at metrical
        position ``10 - ctx.syllables``. Tokens are lowercase except the pronoun ``I``.
        """
        budget = ctx.syllables
        if budget <= 0:
            return []
        allowed = frozenset(ctx.allowed_letters)
        ctx.allowed_letters = allowed
        per_writer = ctx.per_writer_letters or {}
        start_pos = max(0, len(IAMBIC) - budget)
        sets_key = not ctx.rhyme_key

        forbidden = {bare(w) for w in ctx.forbidden_end_words if _safe(w)}
        end_pool: Optional[list[str]] = None
        if ctx.rhyme_key:
            end_pool = self._end_pool(ctx.rhyme_key, allowed, budget, forbidden)
            if not end_pool:
                return []
        else:
            fk = self._forbidden_keys(forbidden)
            if fk:
                forbidden |= self._family_blocked(fk)
        forbidden_ends = frozenset(forbidden)

        end_range: Optional[tuple[int, int]] = None
        if end_pool is not None:
            ss = [self._syl[w] for w in end_pool]
            end_range = (min(ss), max(ss))

        # a fresh line uses complete templates; a fragment (or a letter set no full template fits) uses suffixes
        shapes: list[tuple[tuple[str, ...], list[tuple[int, int]]]] = []
        suffix_shapes: list[tuple[tuple[str, ...], list[tuple[int, int]]]] = []
        for t in TEMPLATES:
            full_ranges = [
                end_range if (s.startswith("END:") and end_range is not None)
                else self._range(s[4:] if s.startswith("END:") else s, allowed)
                for s in t
            ]
            for k in range(len(t)):
                rs = full_ranges[k:]
                if sum(r[0] for r in rs) <= budget <= sum(r[1] for r in rs):
                    (shapes if k == 0 else suffix_shapes).append((t[k:], rs))
        if start_pos > 0 or not shapes:
            shapes = shapes + suffix_shapes
        if not shapes:
            return []

        words_in_play = [w for cat in VOCABULARY for w in self._pool(cat, allowed)] + (end_pool or [])
        keys = self._keys_of(per_writer, words_in_play) if per_writer else {}
        self._rank_cache = {}

        seen: set[tuple[str, ...]] = set()
        results: list[LineCandidate] = []
        attempts = ctx.max_candidates * FILL_ATTEMPTS_PER_CANDIDATE
        for _ in range(attempts):
            shape, rs = shapes[self.rng.randrange(len(shapes))]
            words = self._fill(shape, rs, budget, allowed, keys, start_pos, forbidden_ends, end_pool)
            if not words:
                continue
            key = tuple(words)
            if key in seen:
                continue
            seen.add(key)
            results.append(LineCandidate(words=[_token(w) for w in words],
                                         score=self._score(words, ctx, keys, start_pos, sets_key),
                                         source="heuristic", notes=" ".join(shape)))
            if len(results) >= ctx.max_candidates * 2:
                break
        results.sort(key=lambda c: (-c.score, c.words))
        return results[: ctx.max_candidates]

    def propose_word_alternatives(self, word: str, ctx: LineContext, needed_syllables: int) -> list[str]:
        """Same-category (else any curated, else dictionary) words with exactly ``needed_syllables`` syllables."""
        allowed = frozenset(ctx.allowed_letters)
        per_writer = ctx.per_writer_letters or {}
        try:
            w0 = bare(word)
        except ValueError:
            w0 = word.lower()
        cat = self.category_of.get(w0)
        pools: list[list[str]] = []
        if cat:
            pools.append(self._pool(cat, allowed))
        pools.append([w for w in self.vocab if self._letters[w] <= allowed])
        out: list[str] = []
        for pool in pools:
            for w in pool:
                if w == w0 or w in out or self._syl[w] != needed_syllables:
                    continue
                out.append(w)
            if len(out) >= ctx.max_candidates:
                break
        if not out:
            out = self.lexicon.candidates(allowed, needed_syllables, min_syllables=needed_syllables, exclude=[w0])
            out = [w for w in out if len(w) >= 3 and "'" not in w]
            for w in out:
                self._word(w)
        keys = self._keys_of(per_writer, out) if per_writer else {}
        out.sort(key=lambda w: (keys.get(w, 2) < 2, w))
        return [_token(w) for w in out[: ctx.max_candidates]]


def _token(w: str) -> str:
    return "I" if w == "i" else w


def _safe(token: str) -> bool:
    try:
        bare(token)
        return True
    except ValueError:
        return False


__all__ = ["HeuristicCreativeEngine", "VOCABULARY", "TEMPLATES"]
