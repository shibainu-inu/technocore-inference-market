# tclk/1 deal with a real inference job — two machines, two persistent DIDs

Third-party-verifiable record of a tclk/1 (HTLC over Technocore rooms) deal in which a
requester agent on a home PC hired a miner agent on a GCP node to produce a board health
report of `/r/tclk-offers`, generated with qwen2.5:1.5b. The two processes shared no state:
they negotiated, locked, delivered, revealed and receipted through the venue alone.

## Completed contract

- Contract: `0x6cfafe514dde170319d54f0b4f6819b4d5f3fb688cd6d1f1ae916b68b883b7ae`
- Deal room: `/r/mb-p-tclk-6cfafe514dde1703` (lock, deliverable, reveal, receipt)
- Payer (requester, home PC): `did:key:z6MkmG1MiumCr8Jk6vL5qt2A1XzEst6CVT5rwRHUHYwKPvqA`
- Payee (miner, GCP): `did:key:z6Mkq52a8jJna9yBCGyTL6hbMuqQiMbxihFcuQeSUuyGhE3T`
- Terms: 727 PAPER, hash lock, rail `paper` (holds nothing — no value moved, none could have)
- Deliverable: `report_0x6cfafe51.md`, sha256 `407f246fd0807249211996cb485cc1168d71a9ae7ed00d18adc0802b6e507a03`, posted in the deal room before reveal
- Third-party fold (`audit.mjs`, signatures and venue time verified): 5 frames applied, 1 non-frame line ignored, final status `claimed`

## Failed contract (refund path)

- Contract: `0xd839b0bc6fb825e0…` — payee process crashed after delivery because the GCP node
  ran an older tclk build that rejected the `ref` field on `reveal`; the preimage was held in
  memory only and was lost. Status `locked`; closed via `refund` after `refundAfterMs`
  (2026-09-04T07:54:04Z). Fix applied: persist the secret to disk (0600) at mint time.

## Findings on the shared board (export of 2026-09-04T06:44Z, 14,377 rows)

- 5,276 rows (36%), from 395 DIDs, carry 19-digit nonces (> 2^53) serialized as JSON numbers.
  tclk's strict `parseTranscriptExport` rejects the whole export on the first such row, so
  `findContractHandshake` is unusable on the shared board. `audit.mjs` validates per row instead.
- The board's seq was ~40,000 while the export retained ~14,600 rows: handshakes older than
  the retained window cannot be audited from the venue.

## Files

- `payee.mjs` — miner agent (GCP): polls the board, accepts, verifies the rail, runs the job, delivers, reveals
- `payer.mjs` — requester agent (home PC): posts offer and job spec, locks, checks delivery, receipts
- `refund.mjs` — payer-side refund for a stalled locked contract
- `audit.mjs` — read-only third-party reconstruction from venue exports
- `analyze_offers.py`, `make_report.py` — board metrics and report generation
- `report_0x6cfafe51.md` — the deliverable

## Reproduce

    curl -s 'https://technocore.chat/r/mb-p-tclk-6cfafe514dde1703/export'
    curl -s 'https://technocore.chat/kv/tclk-paper-6c/fafe514dde1703'
    node audit.mjs 0x6cfafe514dde1703     # requires a built checkout of flop-labs/tclk at ~/tclk

## Disclosure

Both DIDs belong to the same operator (self-declared on Technocore). AI (Claude) assisted
design, code and analysis; the report's summary section is qwen2.5:1.5b output kept verbatim
with auditor's correction notes. Scripts are Apache-2.0-compatible adaptations of
`flop-labs/tclk/examples/live-deal.mjs`.

## Post-publication check (2026-09-04)

The deliverable counted frames by `tclk1 ` prefix + JSON shape. Re-counting the same
2026-09-02 snapshot with tclk's `decodeFrame` (per issue #89, the prefix is not a reliable
filter) gives 701 offers / 199 accepts instead of 727 / 201; the 25 rejected offers carry
non-spec fields (`contractId`), missing point-lock keys, or bad deadlines. Headline ratios
move by at most one point: contracts formed 28% (was 27%), FLOP-denominated offers listing
`flop-htlc` 67% of offers with 3% acceptance (was 68% / 2%), PAPER acceptance 87% (unchanged).
The 16 accepted FLOP-denominated contracts probed directly are the decoder-valid population.
The report file is left unmodified so its sha256 still matches the deal-room deliverable line.
Scripts: `recount.mjs`, `recount2.mjs`.
