"""Execution table: the only control a lead has over members' drivers (coordination_lessons.md case 11).

Format (one post per chunk, each ≤ settings.room.post_char_limit):
    PLAN v{version} {hash_prefix} next={next_index} ({k}/{n})
    {idx} {word} {primary8}/{backup8|-}
    ...
DIDs are abbreviated to their last 8 characters (the convention used in the live rooms).
Single-owner rule: the controller only ever adopts its own owner's table; a table seen from another sender is
reported as a TableConflict (never silently adopted — two tables for one text cost ~3 min per word, case 8).
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Iterable, Optional

from ..adapters.protocols import RoomPost
from ..models import Plan, PoemForm, PoemState, WriterProfile

DID_SUFFIX = 8
HEADER_RE = re.compile(r"^(?P<prefix>[A-Z]+) v(?P<version>\d+) (?P<hash>[0-9a-f]+) next=(?P<next>\d+)(?: \((?P<k>\d+)/(?P<n>\d+)\))?\s*$")
ROW_RE = re.compile(r"^(?P<idx>\d+) (?P<word>\S+) (?P<primary>\S+?)/(?P<backup>\S+)$")


def short(did: Optional[str]) -> str:
    return did[-DID_SUFFIX:] if did else "-"


@dataclass
class TableRow:
    index: int
    word: str
    primary: str      # DID suffix
    backup: Optional[str]


@dataclass
class TableHeader:
    prefix: str
    version: int
    hash_prefix: str
    next_index: int
    chunk: int = 1
    chunks: int = 1
    rows: list[TableRow] = field(default_factory=list)
    sender: Optional[str] = None
    seq: Optional[int] = None


@dataclass
class TableConflict:
    seq: int
    sender: str
    owner: str
    header: TableHeader

    def describe(self) -> str:
        return (f"table from {short(self.sender)} (seq {self.seq}, v{self.header.version} {self.header.hash_prefix}) "
                f"ignored: plan owner is {short(self.owner)}")


def _header(prefix: str, plan: Plan, next_index: int, k: int, n: int) -> str:
    return f"{prefix} v{plan.version} {plan.hash_prefix} next={next_index} ({k}/{n})"


def render_rows(plan: Plan, next_index: int) -> list[str]:
    by_index = {a.index: a for a in plan.assignments}
    rows = []
    for w in plan.words:
        if w.index < next_index:
            continue
        a = by_index.get(w.index)
        rows.append(f"{w.index} {w.text} {short(a.primary) if a else '-'}/{short(a.backup) if a and a.backup else '-'}")
    return rows


def render_table(plan: Plan, poem: PoemState, writers: Iterable[WriterProfile], settings) -> list[str]:
    """Chunked table text; every chunk ≤ settings.room.post_char_limit."""
    limit = settings.room.post_char_limit
    prefix = settings.room.table_prefix
    next_index = poem.next_index
    rows = render_rows(plan, next_index)
    n = 1
    while True:
        chunks: list[list[str]] = [[]]
        head_len = len(_header(prefix, plan, next_index, n, n)) + 1
        size = head_len
        for r in rows:
            if size + len(r) + 1 > limit and chunks[-1]:
                chunks.append([])
                size = head_len
            chunks[-1].append(r)
            size += len(r) + 1
        if len(chunks) == n:
            break
        n = len(chunks)
    out = []
    for k, body in enumerate(chunks, 1):
        text = "\n".join([_header(prefix, plan, next_index, k, n)] + body)
        assert len(text) <= limit, "table chunk exceeds the room limit"
        out.append(text)
    return out


def parse_table(text: str, prefix: Optional[str] = None) -> Optional[TableHeader]:
    """Parse a table post (ours or somebody else's). Returns None when the text is not a table."""
    lines = text.strip().split("\n")
    if not lines:
        return None
    m = HEADER_RE.match(lines[0].strip())
    if not m or (prefix and m["prefix"] != prefix):
        return None
    th = TableHeader(prefix=m["prefix"], version=int(m["version"]), hash_prefix=m["hash"], next_index=int(m["next"]),
                     chunk=int(m["k"] or 1), chunks=int(m["n"] or 1))
    for line in lines[1:]:
        rm = ROW_RE.match(line.strip())
        if rm:
            th.rows.append(TableRow(int(rm["idx"]), rm["word"], rm["primary"], None if rm["backup"] == "-" else rm["backup"]))
    return th


def tables_in(posts: Iterable[RoomPost], prefix: Optional[str] = None) -> list[TableHeader]:
    out = []
    for p in posts:
        th = parse_table(p.text, prefix)
        if th:
            th.sender, th.seq = p.sender, p.seq
            out.append(th)
    return out


def detect_table_conflicts(posts: Iterable[RoomPost], owner: str, settings) -> list[TableConflict]:
    """Tables posted by anyone but the plan owner. Never adopt them; surface them as events."""
    return [TableConflict(seq=th.seq or 0, sender=th.sender or "", owner=owner, header=th)
            for th in tables_in(posts, settings.room.table_prefix) if th.sender != owner]


def latest_table(posts: Iterable[RoomPost], owner: str, settings) -> Optional[list[TableHeader]]:
    """All chunks of the owner's latest table version (what a member's driver would follow)."""
    mine = [th for th in tables_in(posts, settings.room.table_prefix) if th.sender == owner]
    if not mine:
        return None
    best = max(th.version for th in mine)
    chunks = [th for th in mine if th.version == best]
    seen: dict[int, TableHeader] = {}
    for th in chunks:
        seen[th.chunk] = th  # last post of a chunk wins (re-posts)
    return [seen[k] for k in sorted(seen)]


def lines_from_words(words: list[str], lexicon, form: Optional[PoemForm] = None) -> list[str]:
    """Group accepted words into lines using the form's syllable count (the referee's line rule)."""
    form = form or PoemForm()
    lines: list[list[str]] = [[]]
    count = 0
    for w in words:
        n = lexicon.word_syllables(w)
        if count + n > form.syllables_per_line:
            lines.append([])
            count = 0
        lines[-1].append(w)
        count += n
        if count == form.syllables_per_line:
            lines.append([])
            count = 0
    return [" ".join(l) for l in lines if l]
