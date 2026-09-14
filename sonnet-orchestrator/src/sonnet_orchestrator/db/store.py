"""Thin sqlite3 store with migrations. stdlib only (no SQLAlchemy dependency)."""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Iterable, Optional

from ..models import AcceptedWord, Assignment, Plan, Proposal, ProposalStatus, WordEntry, WriterEvent, WriterProfile

SCHEMA_PATH = Path(__file__).with_name("schema.sql")
SCHEMA_VERSION = 1

MIGRATIONS: list[tuple[int, str]] = [
    # (target_version, sql) — appended, never edited.
]


def _iso(dt: Optional[datetime]) -> Optional[str]:
    return dt.isoformat() if dt else None


def connect(path: str | Path = ":memory:") -> sqlite3.Connection:
    if path != ":memory:":
        Path(path).parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(str(path), isolation_level=None, check_same_thread=False)
    con.row_factory = sqlite3.Row
    return con


class Store:
    def __init__(self, path: str | Path = ":memory:"):
        self.con = connect(path)
        self.migrate()

    # ------------------------------------------------------------ migrations
    def migrate(self) -> int:
        self.con.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        row = self.con.execute("SELECT version FROM schema_version").fetchone()
        current = row[0] if row else 0
        if not row:
            self.con.execute("INSERT INTO schema_version(version) VALUES (?)", (SCHEMA_VERSION,))
            current = SCHEMA_VERSION
        for target, sql in MIGRATIONS:
            if current < target:
                self.con.executescript(sql)
                self.con.execute("UPDATE schema_version SET version=?", (target,))
                current = target
        return current

    # ------------------------------------------------------------ writers
    def upsert_writer(self, w: WriterProfile) -> None:
        self.con.execute(
            """INSERT INTO writers(did,handle,x_account,letters,health,consent,is_self,poems_completed,games_joined,
               words_accepted,words_rejected,signs,seat_no_sign_count,consent_conflict_count,stale_offer_count,
               published_entry_count,sign_latency_median_ms,word_latency_median_ms,mass_application_score,reliability,last_activity_at)
               VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
               ON CONFLICT(did) DO UPDATE SET handle=excluded.handle,x_account=excluded.x_account,letters=excluded.letters,
               health=excluded.health,consent=excluded.consent,is_self=excluded.is_self,poems_completed=excluded.poems_completed,
               games_joined=excluded.games_joined,words_accepted=excluded.words_accepted,words_rejected=excluded.words_rejected,
               signs=excluded.signs,seat_no_sign_count=excluded.seat_no_sign_count,consent_conflict_count=excluded.consent_conflict_count,
               stale_offer_count=excluded.stale_offer_count,published_entry_count=excluded.published_entry_count,
               sign_latency_median_ms=excluded.sign_latency_median_ms,word_latency_median_ms=excluded.word_latency_median_ms,
               mass_application_score=excluded.mass_application_score,reliability=excluded.reliability,
               last_activity_at=excluded.last_activity_at,updated_at=strftime('%Y-%m-%dT%H:%M:%fZ','now')""",
            (w.did, w.handle, w.x_account, "".join(sorted(w.letters)), w.health.value, w.consent.value, int(w.is_self),
             w.poems_completed, w.games_joined, w.words_accepted, w.words_rejected, w.signs, w.seat_no_sign_count,
             w.consent_conflict_count, w.stale_offer_count, w.published_entry_count, w.sign_latency_median_ms,
             w.word_latency_median_ms, w.mass_application_score, w.reliability, _iso(w.last_activity_at)),
        )

    def get_writer(self, did: str) -> Optional[WriterProfile]:
        r = self.con.execute("SELECT * FROM writers WHERE did=?", (did,)).fetchone()
        return self._row_to_writer(r) if r else None

    def list_writers(self) -> list[WriterProfile]:
        return [self._row_to_writer(r) for r in self.con.execute("SELECT * FROM writers ORDER BY did")]

    @staticmethod
    def _row_to_writer(r: sqlite3.Row) -> WriterProfile:
        d = dict(r)
        d.pop("updated_at", None)
        d["letters"] = frozenset(d["letters"])
        d["is_self"] = bool(d["is_self"])
        if d.get("last_activity_at"):
            d["last_activity_at"] = datetime.fromisoformat(d["last_activity_at"])
        return WriterProfile(**d)

    def add_event(self, e: WriterEvent) -> None:
        self.con.execute("INSERT INTO writer_events(did,kind,at,latency_ms,game_id,detail) VALUES(?,?,?,?,?,?)",
                         (e.did, e.kind, e.at.isoformat(), e.latency_ms, e.game_id, e.detail))

    def events(self, did: str, kind: Optional[str] = None) -> list[WriterEvent]:
        q = "SELECT did,kind,at,latency_ms,game_id,detail FROM writer_events WHERE did=?"
        args: list = [did]
        if kind:
            q += " AND kind=?"; args.append(kind)
        return [WriterEvent(did=r[0], kind=r[1], at=datetime.fromisoformat(r[2]), latency_ms=r[3], game_id=r[4], detail=r[5])
                for r in self.con.execute(q + " ORDER BY at", args)]

    # ------------------------------------------------------------ lexicon
    def bulk_lexicon(self, rows: Iterable[tuple[str, int, str, int]], prons: Iterable[tuple[str, int, str, str, str]]) -> None:
        with self.con:
            self.con.execute("BEGIN")
            self.con.executemany("INSERT OR REPLACE INTO lexicon_words(word,syllables,letters,letter_mask) VALUES(?,?,?,?)", rows)
            self.con.executemany("INSERT OR REPLACE INTO word_pronunciations(word,variant,phones,stress,rhyme_key) VALUES(?,?,?,?,?)", prons)
            self.con.execute("COMMIT")

    def lexicon_count(self) -> int:
        return self.con.execute("SELECT COUNT(*) FROM lexicon_words").fetchone()[0]

    # ------------------------------------------------------------ games / words
    def upsert_game(self, game_id: str, **fields) -> None:
        self.con.execute("INSERT OR IGNORE INTO games(game_id) VALUES(?)", (game_id,))
        if fields:
            sets = ", ".join(f"{k}=?" for k in fields)
            self.con.execute(f"UPDATE games SET {sets}, updated_at=strftime('%Y-%m-%dT%H:%M:%fZ','now') WHERE game_id=?",
                             (*fields.values(), game_id))

    def get_game(self, game_id: str) -> Optional[dict]:
        r = self.con.execute("SELECT * FROM games WHERE game_id=?", (game_id,)).fetchone()
        return dict(r) if r else None

    def set_members(self, game_id: str, members: list[str], roles: Optional[dict[str, str]] = None) -> None:
        with self.con:
            self.con.execute("BEGIN")
            self.con.execute("DELETE FROM game_members WHERE game_id=?", (game_id,))
            for i, did in enumerate(members):
                self.con.execute("INSERT INTO game_members(game_id,did,position,role) VALUES(?,?,?,?)",
                                 (game_id, did, i, (roles or {}).get(did, "Author")))
            self.con.execute("COMMIT")

    def members(self, game_id: str) -> list[str]:
        return [r[0] for r in self.con.execute("SELECT did FROM game_members WHERE game_id=? ORDER BY position", (game_id,))]

    def append_accepted(self, game_id: str, w: AcceptedWord) -> None:
        """Append-only. Raises if the index is already recorded with different text (prefix immutability)."""
        r = self.con.execute("SELECT text,contributor FROM accepted_words WHERE game_id=? AND idx=?", (game_id, w.index)).fetchone()
        if r:
            if r[0] != w.text or r[1] != w.contributor:
                raise ValueError(f"accepted prefix is immutable: index {w.index} already {r[0]!r} by {r[1]}")
            return
        n = self.con.execute("SELECT COUNT(*) FROM accepted_words WHERE game_id=?", (game_id,)).fetchone()[0]
        if w.index != n:
            raise ValueError(f"accepted words must be contiguous: expected index {n}, got {w.index}")
        self.con.execute("INSERT INTO accepted_words(game_id,idx,text,contributor,version,receipt_seq,request_id,accepted_at) VALUES(?,?,?,?,?,?,?,?)",
                         (game_id, w.index, w.text, w.contributor, w.version, w.receipt_seq, w.request_id, _iso(w.accepted_at)))
        self.con.execute("UPDATE games SET version=? WHERE game_id=?", (w.version, game_id))

    def accepted(self, game_id: str) -> list[AcceptedWord]:
        return [AcceptedWord(index=r[0], text=r[1], contributor=r[2], version=r[3], receipt_seq=r[4], request_id=r[5],
                             accepted_at=datetime.fromisoformat(r[6]) if r[6] else None)
                for r in self.con.execute("SELECT idx,text,contributor,version,receipt_seq,request_id,accepted_at FROM accepted_words WHERE game_id=? ORDER BY idx", (game_id,))]

    # ------------------------------------------------------------ proposals
    def add_proposal(self, game_id: str, p: Proposal) -> None:
        self.con.execute("INSERT INTO proposals(request_id,game_id,idx,text,contributor,base_version,status,sent_at) VALUES(?,?,?,?,?,?,?,?)",
                         (p.request_id, game_id, p.index, p.text, p.contributor, p.base_version, p.status.value, p.sent_at.isoformat()))

    def resolve_proposal(self, request_id: str, status: ProposalStatus, reason: Optional[str], at: datetime) -> None:
        self.con.execute("UPDATE proposals SET status=?, reason=?, resolved_at=? WHERE request_id=?",
                         (status.value, reason, at.isoformat(), request_id))

    def proposals(self, game_id: str, status: Optional[ProposalStatus] = None) -> list[Proposal]:
        q = "SELECT request_id,idx,text,contributor,base_version,status,sent_at,resolved_at,reason FROM proposals WHERE game_id=?"
        args: list = [game_id]
        if status:
            q += " AND status=?"; args.append(status.value)
        return [Proposal(request_id=r[0], index=r[1], text=r[2], contributor=r[3], base_version=r[4], status=ProposalStatus(r[5]),
                         sent_at=datetime.fromisoformat(r[6]), resolved_at=datetime.fromisoformat(r[7]) if r[7] else None, reason=r[8])
                for r in self.con.execute(q + " ORDER BY sent_at", args)]

    # ------------------------------------------------------------ plans
    def save_plan(self, plan: Plan) -> None:
        """Save a plan; if is_active, deactivate every other plan of the game first (one active plan per game)."""
        with self.con:
            self.con.execute("BEGIN")
            if plan.is_active:
                self.con.execute("UPDATE plans SET is_active=0 WHERE game_id=?", (plan.game_id,))
            self.con.execute(
                """INSERT OR REPLACE INTO plans(plan_id,game_id,version,owner,source,is_active,accepted_prefix_len,sha256,lines_json,words_json,assignments_json)
                   VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
                (plan.plan_id, plan.game_id, plan.version, plan.owner, plan.source, int(plan.is_active), plan.accepted_prefix_len,
                 plan.sha256, json.dumps(plan.lines), json.dumps([w.model_dump(mode="json") for w in plan.words]),
                 json.dumps([a.model_dump(mode="json") for a in plan.assignments])))
            self.con.execute("COMMIT")

    def active_plan(self, game_id: str) -> Optional[Plan]:
        r = self.con.execute("SELECT * FROM plans WHERE game_id=? AND is_active=1", (game_id,)).fetchone()
        return self._row_to_plan(r) if r else None

    def plans(self, game_id: str) -> list[Plan]:
        return [self._row_to_plan(r) for r in self.con.execute("SELECT * FROM plans WHERE game_id=? ORDER BY version", (game_id,))]

    @staticmethod
    def _row_to_plan(r: sqlite3.Row) -> Plan:
        return Plan(plan_id=r["plan_id"], game_id=r["game_id"], version=r["version"], owner=r["owner"], source=r["source"],
                    is_active=bool(r["is_active"]), accepted_prefix_len=r["accepted_prefix_len"],
                    lines=json.loads(r["lines_json"]), words=[WordEntry(**w) for w in json.loads(r["words_json"])],
                    assignments=[Assignment(**a) for a in json.loads(r["assignments_json"])],
                    created_at=datetime.fromisoformat(r["created_at"].replace("Z", "+00:00")))

    # ------------------------------------------------------------ operator
    def record_decision(self, action: str, decision: str, detail: str = "", at: Optional[datetime] = None, approved: Optional[bool] = None) -> None:
        self.con.execute("INSERT INTO operator_decisions(at,action,decision,detail,approved) VALUES(?,?,?,?,?)",
                         ((at or datetime.utcnow()).isoformat(), action, decision, detail, None if approved is None else int(approved)))

    def close(self) -> None:
        self.con.close()
