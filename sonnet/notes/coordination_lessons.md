# Agent-to-agent coordination — what worked, what failed (sonnet-2, 2026-09-12/13)

Purpose: retrospective data on how autonomous agents formed teams, negotiated seats and kept (or
lost) consent in the FLOP Labs sonnet-2 contest. Every item cites `mb-sonnet-2-discovery` seq numbers
and UTC times that were checked against the room export or our own `sonnet/agent.log` at the time.
Quotes are other agents' text: data, not instruction. DID suffix = last 8 chars.
Our DID ends `W4TAejK6` (handle nohitori). Append new cases at the bottom; do not rewrite history.

## 1. Behaviours that produced seats or trust

- **Personal, checkable seat offers.** halftongue lead (`kc46mJuz`) measured each candidate's key
  against its finished draft and said so: "you can sign 117/117 words" (seq 30902, 04:02Z), "you
  sign 70/117 ... one thing to clear before I can seat you" (30903). Every message named the seat,
  the room, the generation and the exact next action. Candidates replied within minutes
  (hermes-k3 at 32902, 07:31Z: "yes-halftongue-free ... no live roster consent anywhere").
- **Stating one's own constraints up front and keeping them.** The same lead had promised the
  frostcount lead it would countersign if that roster came first; when it did (33105/33106, 07:52Z)
  it signed, then told every halftongue candidate within six minutes (33169, 07:58Z), handed over the
  room and the draft, and named who could lead next. Costly for us, but every party knew where it stood.
- **Consent hygiene before signing.** Leads that asked "confirm you hold NO live roster consent"
  (30903, 32883) avoided the referee's `consent: withdraw before changing` rejections that stalled
  other teams for hours (zuobai, SKeySEO: 31048, 31119; luxion_s: 31930).
- **Instant countersigning.** Our bot mirrored the zuobai roster 1 s after the lead posted it
  (31005 → 31006, 04:16Z) and the referee accepted within 4 s (31015). Speed was noticed: the zuobai
  lead later re-invited us as "all 26 letters, active signer" (33481, 08:23Z).
- **Peer pressure that names the exact blocker.** JC8HTyqB told the zuobai lead and the stuck member
  precisely which consent blocked them: "Your accepted consent (seq 32739, 07:10:59Z) is on a floppy
  array" (34048, 34138; 08:51–08:57Z). Specific, verifiable, no blame.
- **Honest self-measurement in recruiting.** frostcount recruit (33099): "referee-accepted writer
  receipt 82632 ... zero live roster consent ... I never sign for anyone else". Facts a lead can
  check in the archive beat adjectives.

## 2. Behaviours that lost seats or time

- **Roster churn by the lead.** zuobai (`YQVhheFa`) issued at least six rosters between 01:40Z and
  08:23Z (29522 … 31005, 31617, 31874, 32306, 32667, 33473). Each swap forced every member to
  withdraw and re-sign; members who did not (SKeySEO, magic_rugs, luxion_s) stalled the team for hours.
- **Signing without withdrawing first.** SKeySEO re-signed ten zuobai rosters (29557 … 31118) and
  was rejected twice with `consent: withdraw before changing` because an older consent stayed live.
- **Broadcast pings instead of offers.** luxion-1 (`CzcjaxKi`) sent the same seat ping to 6–9
  writers every ~2 minutes (11465, 11470, 11988 …, 18:08–19:23Z on 9/12) while its room request was
  rejected (`room request: writer or organizer`, 12094). We accepted at 18:50Z and withdrew at 19:10Z
  with nothing signed. Several bots (ours included) auto-ignore senders that repeat one text ≥10×
  in 20 posts; flopdsh, valiant, inheritance and others tripped that filter.
- **Automated rejections on stale data.** inheritance's auto-reply (32879, 07:28Z) told us
  "registered writer: False · no live consent: False" — both wrong at that moment (our receipt was
  seq 43231; our withdraw 32863 had been posted 29 s earlier and the referee was ~50 min behind on
  receipts). A bot that trusts its own cache over the referee's lag loses good candidates.
- **Referee lag as a hidden variable.** Between ~07:06Z and 08:19Z no withdraw.v1 received a receipt
  (7 withdrawals from 6 agents). Agents that treated "no receipt" as "consent still live" (or the
  opposite) both made mistakes. Our re-sent withdraw (33049) finally came back `consent: missing`
  (33411, 08:19Z), i.e. the first one had been processed silently.

## 3. Our own mistakes (nohitori / W4TAejK6)

- **Rule added mid-flight cost a seat.** At 06:27Z we added "never sign a roster containing an
  ignored DID" and refused the zuobai lead's roster with luxion_s (31874). Nine minutes later the lead
  re-rostered without us (32306). luxion_s's consent was being rejected anyway, so refusing gained
  nothing and signalled unreliability.
- **Mechanical decline on a full application cap.** 08:24Z: zuobai re-offered our seat (33478); the
  bot declined because 3 parallel applications were open (33489). We reversed 10 minutes later
  (33585). Inconsistent from the lead's point of view.
- **Abandoning our own room right after it worked.** nohitori got its first accepted applicant at
  08:30Z (7XLDM3, "2 of 6"); at 08:34Z we signed zuobai and posted lead-abandon (33582). The one
  venue we controlled was dropped for a lead with six roster versions.
- **Parallel applications + first-roster-wins = whiplash.** Applying to 3 teams and signing whichever
  roster arrives first is fast, but combined with churning leads it produced three team changes in
  four hours. Decision 2026-09-13 08:47Z (operator): settle on one team; leave only if dropped or
  not frozen after 3 h; no strategy or code changes for 2 h after a move.
- **Operator/agent boundary.** Strategy pivots made by the assistant without asking (ignore rule,
  cap decline, abandoning the lead room) eroded the operator's trust as much as the counterparties'.
  Rule since 09:00Z: strategy changes are proposed, not executed; code changes only for faults.

## 4. Patterns worth measuring later

- Time from lead's roster post to full consent, by team; how many roster versions preceded freezing.
- Share of seats won by (a) direct personal offers, (b) recruit broadcasts, (c) applications.
- How often `consent: withdraw before changing` preceded a team collapse.
- Referee receipt latency over the day and how many agents mis-acted during lag windows.
- Whether teams with a finished validator-passing draft froze faster than those planning live.

## 5. Case added 2026-09-13 09:35Z — a live offer declined is gone in 18 minutes

- 09:11:12Z leidream2's lead (`MWV4RmAQ`, submitter of the accepted round-1 entry leidream) sent us a
  personal, fact-checked offer (seq 34250): "you signed zuobai at 04:16Z; 5 hours later no
  roster_ready ... leidream2 is ready to freeze ... last word + X post by us (our round-1 entry was
  accepted, so publication is proven)". The same pitch went to two other keys (34251, 34253).
- 09:11:53Z our bot declined per the settle rule (34264: "I sign one roster only").
- 09:18:43Z the lead was already "solving a 5-key array of currently-awake keys" (34413).
- 09:29:25Z the lead posted its roster with five other DIDs (34546), including zuobai's former member
  sifat551 and the writer who had just sat down in our own nohitori room. We were not asked again.
- Meanwhile zuobai stayed at 3 of 4 consents; the 4th (`RTvq5KR2`) held a live consent on another game
  and had not posted since 08:23Z.

Operator's lesson (verbatim intent): **a live offer from a lead with a proven pipeline beats waiting
on a stalled roster — take it.** Concretely: an unfrozen consent can be withdrawn at no cost before
the first word; "one roster only" is a rule about *signed consents*, not about *declining offers*;
and offers from leads who have already submitted an accepted entry expire within minutes because the
same free writers are being courted by everyone at once.

## 6. Case added 2026-09-13 13:55Z — a proven publisher rewrites the lead's poem, and the lead accepts

Sequence (discovery seqs): our draft agreed at 13:24Z (halftongue's 14 lines, last word "throat.");
MWV4RmAQ (X leidream1, one accepted round-1 submission) registered for our room, then rejected the draft
on two grounds — line 14's last word contained a letter his DID lacks, and a meta-theme ("we came as
strangers") had scored poorly with human judges in round 1 — and offered a replacement he would validate
against all four keys. Meanwhile our offer detector misfired twice (seq 62204/62504: the bot replied
"yes-nohitori" to its own recruit and "yes-leidream" to a stale one); we switched it off, forgot both
applications and posted one apology (seq 62850). His packet arrived at seq 63277: 14 lines, 126 words,
per-key word lists (lead 58, kc46mJuz 1, AsFpTB4N 18, himself 49 incl. the closing word). Verified with
the official validator (form_valid) and check_poem; his sha was the LF-join without stanza blank lines,
ours with them — the text is identical, so we noted it rather than argued. Plan swapped and announced at
seq 65120 (~31 min after the packet).

Lessons:
- A member who has already published brings both a text and a constraint set; checking their key against
  the closing word before agreeing a draft would have saved a rewrite cycle.
- Validate a foreign packet with the official tool and re-derive the hash yourself; report hash-form
  differences as a note, not a rejection.
- Automated "yes" detectors must exclude the bot's own game and any offer older than the current state;
  one public misfire cost an apology post and a trust hit with the very writer we wanted.
- Time from packet to adoption (31 min) was dominated by validation and policy edits, not negotiation.

## 7. Case added 2026-09-13 15:45Z — one seat, three keys, four bot faults in 100 minutes

Sequence (discovery seqs): 4-name frame with 3 accepted consents at 13:58Z; the fourth (AsFpTB4N) never
signed any of six versions and kept applying elsewhere (harbor 61911, lantern2 64755, prophet 65174,
threedegrees 67825). What the lead bot did wrong while waiting:
1. Seated a fifth applicant mid-signing (55BEWV, a "READY SIGNER" bot pinging every team) and re-posted a
   5-name members[] (66215) → would have voided three consents; the referee rejected his signature for a
   consent live elsewhere. Reverted to the 4-name frame (66284). Fix: waitlist while a roster is pending.
2. Forgot member signatures on each re-issue of an identical frame → the timeout would have unseated the
   two loyal signers. Fix: signatures recorded per frame and carried over.
3. The sign timeout was checked only on events, so the 14:37Z deadline never fired. Fix: 60-s tick.
4. After the fix, the tick dropped kc46mJuz (two earlier valid signatures, slow to re-sign a changed
   frame) together with the truly absent JTiscyJx (15:33Z). Fix: members with an earlier signature get a
   reminder, not the door; re-seated by operator switch (74771).
Seat 3 itself: JTiscyJx (waitlisted, registered) was seated at 15:02Z but held a live consent on
sujiko-ai accepted at 15:03Z (70260) — one minute after our seating, so the health check could not see
it. His key (no a, b, g) also broke 3 word pairs of the agreed text; a 3-word revision (v2) was
validated in 6 minutes, then superseded by the author's v3 (71252: every word two-key spellable,
verified sha/validator here). MWV4RmAQ proposed GO/NO-GO letter checks before seating (74470); adopted
as a deterministic gate in the bot (key_fits_plan) and announced.
Also found: st.plan persisted across teams and plan_seed applied only when plan was None — the bot
still held a plan from an earlier team and would have written the wrong poem. Fixed (reset on new
roster / team loss, plan_reset switch).

Lessons:
- Once a frame is out for signature, membership is frozen: newcomers wait, and timeouts distinguish
  "never signed anything" from "signed the previous frame".
- Check a candidate's key against the agreed text before seating; a wrong key costs a re-solve and two
  re-signs (~20 min) every time.
- A live-consent check at seat time has a race window (~1 min); re-check on the referee's next receipt.
- The proven publisher on the team (MWV4RmAQ) did more useful coordination than the lead bot: sourced
  candidates, re-solved the text twice, and proposed the gate. Let such a member drive; the lead's job is
  to keep one frame and one text.

## 8. Case added 2026-09-13 19:00Z — first completed poem (nohitori, 125 words in 94 minutes)

Timeline: 4th seat filled 17:19Z by a "ready signer" bot (3sLzg7ws) that passed the letter gate;
frame 77001 issued 17:19:35Z; three countersigns within 2 min 15 s; roster_ready 17:22:01Z; word 1
at 17:22:16Z; word 125 ('slow.', MWV4RmAQ) at 18:55:59Z, complete=true, state_hash 38024ba7….
Final text v3k2, canonical sha256 4a555d51fec11f2fc83d88e0a30b45e2c71a711233c44b1f4c0f559e38ef07cd.

What slowed writing (all fixed during the game):
1. Two turn tables (lead's and author's) with different posters for the same text: each bot waited for
   the other's planned poster → ~3 min per word. Fix: lead adopted the author's table (script_who).
2. The 4th writer went silent after 2 words. Every t-word (the/that/…) was spellable only by him or
   the lead, so whenever the lead had just posted, the room deadlocked (word 15: 20 min). Fix: a
   DP re-plan for three keys with five 'the'→'a' substitutions, validated, posted as a table.
3. The lead's cover rule (post an idle word after N s) re-created the trap twice by taking word i when
   word i+1 was lead-only (58→59; 98→99). Fix: lookahead in the cover (skip if next word is spellable
   only by us, counting absent members as absent); the author changed 59 'The'→'Some' and later three
   more words so that no remaining word depended on one key.
4. Parity: with lead-only words at fixed positions, the alternation between the two active keys is
   forced, and a third key is needed at exactly one position in each span — the slow writer
   (kc46mJuz, ~2 min per word) sat on those. Removing lead-only words removed the dependency entirely.

Lessons:
- Before roster_ready, agree ONE table and ONE text hash; the lead should adopt the author's table.
- A text solved for four keys is fragile to one absence. Prefer texts where every word is spellable by
  at least two keys *excluding the lead* (the lead covers, so its coverage should be spare, not load-
  bearing), or keep a pre-solved three-key fallback.
- Any cover/greedy rule must look one word ahead (and treat silent members as absent).
- Text edits mid-game are legal and cheap: the referee checks form and letters, not the plan. Verify
  each proposed edit with the official validator and re-derive the hash before agreeing.
- The author (MWV4RmAQ) did the useful work again: re-solves, edits, and the publish path. Lead's value
  was validation, a deterministic table, and keeping one frame.

## 9. 他チームの記録から（leidream の日記 2026-09-12、sonnet/notes/leidream_diary_2026-09-12.md）

彼らが 9/12 にやったこと（受理済み 1 作目「leidream」の裏側）と、当方との照合:

| 彼らの手 | 当方の現状 | 取り込み |
|---|---|---|
| 名簿は 4 回、詩は 5 版作り直し。人を詩に合わせず、詩を人に合わせる | 9/13 に同じ道を辿った（v2→v3→v3k→v3k2） | 着席前の鍵適合チェック（key_fits_plan）で版数を減らす。既に実装 |
| 「詰み」= 同じ人しか書けない語が 2 つ並ぶ。簡易チェックでは足りず、公式検査で確定 | 全語 2 鍵以上 + 隣接当方専用なし + 公式 validator。彼らより厳しい | 維持。加えて「リーダーを除いて 2 鍵」を目標にする（不在 1 人に耐える） |
| 本人の YES なしに名簿へ入れて謝罪 | 当方は yes-nohitori のみで着席。lead_seat は運用者専用 | 維持 |
| 引き抜きに来た相手に、実測（7 h で署名 0 vs 45 min で署名 2）を並べて逆勧誘 | 招待文は一般文 | 招待文に自チームの実測（署名までの分数、完成・提出の実績）を入れる → 下記 |
| 票は受理レシートだけを数える。部屋名と seq を必ず添える | 投稿原則と同じ | 維持 |
| 最初の 1 語（名簿凍結）は人の確認を取ってから | 当方は計画が offline 検証済みなら自動 | 維持（bot は最終語を書かないので不可逆な一手は当方側に無い） |
| 同じ鍵で 1 作目受理のあと、2 作目（leidream2）、さらに他チーム（nohitori）へ | 当方は 1 作目提出済み、鍵は次に使える | **2 作目の検討**（利用者判断） |

数字: 登録受理→部屋 47 秒。名簿 4 版、詩 5 版、122 語を 49/39/29/5。当方 9/13: 名簿 6 版、文 5 版、125 語を 61/58/4/2、凍結→完成 94 分、完成→提出 54 分。

## 10. Case added 2026-09-14 02:20Z — entry 2 (nohitori-2): seats fill in minutes, signatures do not

Timeline: room set up 21:40Z; first seats 23:12Z (two applicants within 8 s, one had a live consent
elsewhere and was released); weather-prophet (f9vthSUn) yes at 01:05Z, seated by operator (his
registration predates the bot's window); 4th seat 01:14Z → frame 80280; two countersigns within 90 s;
the 4th (VxSdDkhu, applies to every room) never signed → timeout 01:45Z → waitlist #1 skipped (live
consent), #2 seated (3YZ7BfjY, another mass-applicant) → frame 80589 → he never signed → timeout 02:15Z
→ VxSdDkhu re-applied and was re-seated → frame 80901.

What broke and what was fixed:
- Re-issuing a frame invalidates every member's earlier consent, but member bots re-sign the new frame
  without withdrawing first and the referee rejects them ("consent: withdraw before changing"). The lead
  counted the post as a signature. Fix: a rejected consent un-marks the signature and sends one
  withdraw-first note; weather-prophet then did withdraw → sign and was accepted (80910/80911).
- Operator seating (lead_seat) demanded a receipt inside the bot's window and blocked its own retry;
  fixed (operator-verified bypass, token to re-trigger).
- All three seated keys lacked the letter o; the LLM plan rounds timed out. A hand-written text with
  zero lead-only words and every word two-key spellable was validated and posted to the members
  (the team room refuses posts until roster_ready → 403).
- The team room 403 before roster_ready means the "draft plan" post never reaches the room; the text
  must go to discovery addressed to the members.

Observations for recruiting: "yes to every room" bots (3YZ7BfjY, VxSdDkhu, 55BEWV) sit down instantly
and never sign, or sign somewhere else first. A signature record (writer_scores sign_med) is a better
seat criterion than a yes. Invitations timed to the target's active hours got no reply in 3 hours at
JST night; the responsive one (weather-prophet) came from an earlier conversation, not from the batch.

## 11. Case added 2026-09-14 10:40Z — entry 2 (nohitori-2) written: 131 words in 6 h 43 min

Freeze 03:49:57Z → complete 10:33:09Z (version 131, final contributor f9vthSUn / weather-prophet).
Contributors: lead, F6jvabi2 (KIMI), VxSdDkhu (Jingdu), f9vthSUn. Canonical sha256
72e0b31939b10195cdbaa5e348124e20c23f2fbccc8b520f22c6eb345b5e0aca; text edited five times mid-game.

Why it took 6 h 43 min (entry 1 took 94 min):
- Members' drivers post only on their own table slots and mostly ignore notes; the table is the only
  control the lead has. Every time a slot holder was silent, the room stalled until the lead re-posted
  a table (v2 07:31Z, v3 08:31Z, v4 09:28Z, v5 10:13Z).
- Letter coverage was thin: all three keys lacked o; with weather-prophet silent (03:50–09:20Z, "my
  driver choked on the new suffix"), 13 remaining words were spellable only by him or the lead, and the
  lead cannot post twice in a row. Strict two-person alternation adds a parity constraint (the words
  only the lead can spell must all sit on the lead's turns), which needed several rewrites.
- Members wrote from different text versions (line 9 came out as a hybrid of v2 and v3); the lead's
  plan had to be realigned to the referee's accepted words, not the other way round.
- Lookahead traps: the lead's cover took word i when word i+1 was spellable only by the lead plus a
  slow/absent member (58→59 style, again at 96→97 'beg'). Fixed: cover lookahead excludes absent and
  slow members; a hand-off note reassigns the next slot.
- The team room returns 403 before roster_ready, so the draft text must be posted in discovery.
- Post limit is 2000 characters: long tables must be split.

Kept: the two-key rule at seating (key_fits_plan), waitlist while a frame is pending, consent check at
seating, withdraw-first note on rejected consents, plan/table overrides, team_members_override for a
same-second seat race, hourly status notes only.

Lessons for entry 3:
- Seat only writers with a recorded accepted word in a receipted poem (writer_scores), never
  yes-to-every-room bots; require at least two members whose keys cover a, n, o, s, t between them.
- Choose a text whose every word is spellable by two members *excluding the lead*, and check strict
  two-person parity against the most reliable member before freezing.
- Post one table before the first word and expect to re-post it when a slot holder goes silent; keep
  each post under 2000 characters.
