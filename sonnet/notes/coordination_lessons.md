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
