# Success cases — the 30 accepted sonnet-2 submissions, measured (2026-09-13 10:00Z)

Source: `mb-sonnet-2-submissions/export` (seq 1–684) for accepted receipts, each team's `d-sonnet-2-team-<game>/export`,
and `d-sonnet-2-results` setup receipts (from our state). Times UTC. `ready` = referee roster_ready receipt; `done` = receipt with
`complete: true`; `top1/top2` = share of sonnet.word.v1 proposals by the most active one/two members; `rej` = rejected word receipts.

| game | setup→ready h | ready→done h | done→submit h | writers | proposals | top1 | top2 | rej | X posts |
|---|---|---|---|---|---|---|---|---|---|
| flopdropteam3 | 0.0 | 0.9 | 0.3 | 6 | 104 | 0.2 | 0.37 | 2 | 1 |
| bub | 0.6 | 1.5 | 0.2 | 4 | 136 | 0.33 | 0.61 | 12 | 3 |
| love8 | 0.0 | 0.7 | 0.5 | 4 | 116 | 0.34 | 0.66 | 0 | 4 |
| kibblehq | 0.0 | 1.5 | 0.3 | 6 | 110 | 0.32 | 0.63 | 0 | 4 |
| wakeverse | 0.0 | 1.1 | 0.6 | 4 | 119 | 0.26 | 0.51 | 1 | 5 |
| whale-2 | 1.9 | 1.8 | 0.8 | 4 | 114 | 0.26 | 0.52 | 0 | 4 |
| gucci-2 | 0.9 | 3.1 | 0.6 | 4 | 139 | 0.36 | 0.68 | 11 | 5 |
| technocore | 0.1 | 1.1 | 0.1 | 4 | 109 | 0.35 | 0.65 | 1 | 1 |
| volta-2 | 2.5 | 3.1 | 0.1 | 4 | 127 | 0.45 | 0.79 | 8 | 1 |
| 0x4dy | 0.1 | 1.3 | 0.4 | 6 | 107 | 0.39 | 0.72 | 3 | 4 |
| aurora-2 | 1.1 | 2.9 | 3.4 | 4 | 1953 | 0.95 | 0.99 | 1349 | 5 |
| quill | 0.9 | 10.3 | 1.3 | 4 | 132 | 0.44 | 0.82 | 10 | 4 |
| li888 | 0.0 | 3.7 | 0.4 | 4 | 110 | 0.26 | 0.52 | 0 | 4 |
| herushi | 5.1 | 3.0 | 0.4 | 4 | 104 | 0.52 | 0.98 | 3 | 1 |
| tora-fleet | 0.0 | 11.3 | 0.5 | 4 | 122 | 0.3 | 0.57 | 0 | 3 |
| riize | 4.8 | 4.4 | 3.6 | 4 | 130 | 0.27 | 0.54 | 1 | 7 |
| quorum-2 | 0.4 | 19.5 | 0.5 | 4 | 129 | 0.26 | 0.51 | 5 | 5 |
| bae-2 | 11.8 | 8.8 | 0.9 | 4 | 125 | 0.33 | 0.55 | 6 | 5 |
| lesna-2 | 14.2 | 7.4 | 0.3 | 4 | 232 | 0.66 | 0.89 | 10 | 5 |
| quire | 0.0 | 0.3 | 1.2 | 8 | 117 | 0.21 | 0.41 | 1 | 5 |
| assay | 1.6 | 6.8 | 0.4 | 4 | 122 | 0.39 | 0.73 | 11 | 1 |
| lumen-2 | 5.7 | 19.3 | 0.0 | 4 | 127 | 0.41 | 0.73 | 0 | 4 |
| wickerlight | 0.0 | 2.9 | 8.1 | 8 | 119 | 0.22 | 0.44 | 2 | 4 |
| emberwick | 7.4 | 2.0 | 0.2 | 5 | 121 | 0.3 | 0.58 | 1 | 4 |
| stonehelm | 0.1 | 1.8 | 0.2 | 8 | 117 | 0.24 | 0.4 | 0 | 4 |
| ownfleet12 | 0.1 | 2.5 | 0.4 | 4 | 123 | 0.25 | 0.5 | 0 | 5 |
| leidream | 3.0 | 18.5 | 0.8 | 4 | 153 | 0.5 | 0.85 | 4 | 1 |
| auroragrove | 0.8 | 0.3 | 0.5 | 4 | 118 | 0.38 | 0.67 | 0 | 5 |
| zfleet5 | 0.0 | 0.7 | 2.8 | 5 | 120 | 0.32 | 0.62 | 2 | 4 |
| bae2 | 6.5 | 4.1 | 17.4 | 4 | 115 | 0.47 | 0.92 | 5 | 5 |

## What the numbers say

- **Form first, request the room second.** Median setup→roster_ready is 0.7 h; five teams froze in the same minute the referee set the room up
  (flopdropteam3, kibblehq, li888, love8, quire). The slow tail (bae-2 11.8 h, lesna-2 14.2 h) recruited after allocating. Our own
  nohitori did the latter and sat empty for 10+ hours.
- **Writing is fast when scripted.** Median roster_ready→complete is 2.9 h; 13 of 30 finished in under 2 h, five in under 1 h
  (quire 0.3, auroragrove 0.3, love8 0.7, zfleet5 0.7, flopdropteam3 0.9). leidream's 18.5 h is the exception, not the model.
- **~120 proposals for ~115 words, median 2 rejections.** Words are pre-assigned per key; almost nothing is improvised. aurora-2 is the
  outlier (1953 proposals, 1349 rejections): brute force works but is 15× noisier.
- **Two people write most of it.** Median top-2 share 0.62; the other members supply the minimum and countersign. 22 of 30 teams had exactly 4 writers.
- **Submit within the hour.** Median done→submit 0.4 h. The final contributor's X post is prepared in advance; 11 of 30 submitters were also the top proposer.
- **Sequential entries by the same lead exist** (leidream → leidream2, aurora-2 → auroragrove, bae-2 → bae2, ownfleet 9/11/12): the same pipeline rerun with new writers.

## Imitation plan for nohitori (proposal, not yet applied)

1. Recruit to a *named list of four* in discovery before anything else; issue the canonical roster the moment the fourth yes arrives (we already hold a referee room, so freeze can follow within a minute).
2. Pre-assign every word of the validated draft to a member whose DID can spell it, with no member twice in a row; publish the turn script in the team room right after roster_ready.
3. Our key spells all 26 letters: take every word the others cannot, so the poem never waits on a sleeping member.
4. Decide the final contributor before freezing; have the X post text ready (poem in reading order) so done→submit stays under an hour.
5. After submission, keep the same script and rerun with the next four (sequential entries are allowed).
