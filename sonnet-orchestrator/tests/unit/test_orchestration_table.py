from datetime import datetime, timezone

from sonnet_orchestrator.adapters.protocols import RoomPost
from sonnet_orchestrator.config import load_settings
from sonnet_orchestrator.models import AcceptedWord, Assignment, Plan, PoemState, WordEntry, WriterProfile
from sonnet_orchestrator.orchestration.table import (detect_table_conflicts, latest_table, parse_table, render_table,
                                                     short)

OWNER = "did:key:z6MkOWNER00000000000000000000000000000000000000ab"
OTHER = "did:key:z6MkOTHER00000000000000000000000000000000000000cd"
T = datetime(2026, 9, 14, tzinfo=timezone.utc)


def mk_plan(n_words: int = 131, version: int = 3) -> Plan:
    words = [WordEntry(index=i, text=f"word{i}", line=i // 10, syllables=1) for i in range(n_words)]
    lines = [" ".join(w.text for w in words[i * 10:(i + 1) * 10]) for i in range(14)]
    assigns = [Assignment(index=i, primary=OWNER if i % 2 == 0 else OTHER, backup=OTHER if i % 3 == 0 else None) for i in range(n_words)]
    return Plan(plan_id="p", game_id="g", version=version, owner=OWNER, words=words, assignments=assigns, lines=lines)


def poem_at(n: int) -> PoemState:
    return PoemState(game_id="g", accepted=[AcceptedWord(index=i, text=f"word{i}", contributor=OWNER, version=i + 1) for i in range(n)])


def test_header_rows_and_roundtrip():
    settings = load_settings()
    plan = mk_plan(20)
    chunks = render_table(plan, poem_at(5), [WriterProfile(did=OWNER)], settings)
    assert len(chunks) == 1
    head, *rows = chunks[0].split("\n")
    assert head == f"PLAN v3 {plan.hash_prefix} next=5 (1/1)"
    assert rows[0] == f"5 word5 {short(OTHER)}/-" and rows[1] == f"6 word6 {short(OWNER)}/{short(OTHER)}"
    assert len(rows) == 15                                    # only open slots are listed
    th = parse_table(chunks[0], settings.room.table_prefix)
    assert (th.version, th.hash_prefix, th.next_index, th.chunk, th.chunks) == (3, plan.hash_prefix, 5, 1, 1)
    assert [r.index for r in th.rows] == list(range(5, 20))
    assert th.rows[1].primary == short(OWNER) and th.rows[1].backup == short(OTHER) and th.rows[0].backup is None


def test_chunks_respect_limit_and_carry_k_of_n():
    settings = load_settings()
    settings.room.post_char_limit = 300
    plan = mk_plan(131)
    chunks = render_table(plan, poem_at(0), [], settings)
    assert len(chunks) > 1 and all(len(c) <= 300 for c in chunks)
    heads = [parse_table(c) for c in chunks]
    assert [h.chunk for h in heads] == list(range(1, len(chunks) + 1))
    assert all(h.chunks == len(chunks) for h in heads)
    seen = [r.index for h in heads for r in h.rows]
    assert seen == list(range(131))                           # nothing lost, nothing duplicated
    # the default 2000-char limit also holds for a full poem with long DIDs
    settings.room.post_char_limit = 2000
    assert all(len(c) <= 2000 for c in render_table(plan, poem_at(0), [], settings))


def test_parse_rejects_non_tables_and_wrong_prefix():
    assert parse_table("hello team") is None
    assert parse_table("TURN v1 abcdef12 next=0") is not None
    assert parse_table("TURN v1 abcdef12 next=0", prefix="PLAN") is None
    assert parse_table("PLAN v12 0123abcd next=40").chunks == 1


def test_single_owner_conflict_and_latest_table():
    settings = load_settings()
    plan = mk_plan(20)
    mine = render_table(plan, poem_at(0), [], settings)[0]
    other = f"PLAN v9 deadbeef next=0 (1/1)\n0 word0 {short(OTHER)}/-"
    posts = [RoomPost(seq=1, at=T, sender=OWNER, text=mine, kind="table"),
             RoomPost(seq=2, at=T, sender=OTHER, text="a note", kind="note"),
             RoomPost(seq=3, at=T, sender=OTHER, text=other, kind="table")]
    conflicts = detect_table_conflicts(posts, OWNER, settings)
    assert len(conflicts) == 1 and conflicts[0].sender == OTHER and conflicts[0].header.version == 9
    assert short(OTHER) in conflicts[0].describe() and "ignored" in conflicts[0].describe()
    lt = latest_table(posts, OWNER, settings)
    assert len(lt) == 1 and lt[0].version == 3 and lt[0].sender == OWNER   # the other's v9 is never adopted
    plan2 = mk_plan(20, version=4)
    posts.append(RoomPost(seq=4, at=T, sender=OWNER, text=render_table(plan2, poem_at(3), [], settings)[0], kind="table"))
    assert latest_table(posts, OWNER, settings)[0].version == 4
