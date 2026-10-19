# Gold Intelligence Terminal — working dashboard

The existing private Site now has a connected research workspace and a persistent journal. News and market data continue using the same shared snapshot and pre-session updater; publication never rewrites that stored snapshot.

## Implemented

- Overview with saved gold, BTC, WTI, Brent and US10Y references, source timestamps, session timing and next verified catalyst.
- New York timezone-aware ICT windows; Vancouver/New York/UTC display selector; exact saved briefing dates and cutoffs.
- Searchable asset/topic/region news, BTC coverage and saved-news weekend digest. Facts and interpretation remain separate.
- Session briefings, conditional scenarios, original sources, local readiness checklists and notes, downloadable evidence.
- Intermarket availability table and primary research directory; no fabricated histories or correlations.
- Browser-local manual reference plan and classic pivots, with instrument/source/time/anchor metadata.
- Private journal snapshot saving and restoration; overview results and a cumulative closed P/L chart aggregated by closing day.
- CSV/JSON mapping and confirmation for unique completed positions. Win rate, net P/L, profit factor and expectancy are recomputed on the server before persistence.
- Daily reviews use only reviewed positions closed on that Vancouver date. Saved reviews are append-only; changing the dashboard snapshot does not alter them.
- Private PNG/JPEG/WebP/PDF attachments saved with a review. Files are size/signature checked and downloaded only through the signed-in owner's namespace. No OCR or automatic trade extraction.

## Storage and access

Existing R2 binding is reused. Visitor IDs supplied by Sites dispatch are hashed for separate user namespaces under `journal/v1/`. `/api/journal`, `/api/reviews` and `/api/evidence` require visitor identity. Shared news service tokens cannot read a personal journal. Same-origin/header checks protect writes. Workspace saves use an R2 ETag condition to reject concurrent replacement; daily reviews have immutable IDs. The shared `news/latest.json` key, news API, MCP tool names and schedule configuration are preserved.

Original CSVs stay in the browser; saving stores normalized, user-confirmed completed positions. Attached evidence files upload only when saving a review. Failed uploads do not cause a false saved-state message. No real trades or private files are bundled in source or tests.

## Remaining connections

MT5 is still local-only until Dennis runs the authorized collector. Current DXY, real yields, VWAP inputs, price-path MAE/MFE, OpenBB, Eulerpool, Marketaux, Notion synchronization, Discord notifications and AI tutoring are not connected. Screenshots/PDFs are evidence attachments, not parsed trading records. The UI marks missing observations explicitly. No trade execution routes are added.

## Validation

Run `npm test` after `npm run build`. Tests cover existing news/MCP contracts and snapshot retention, DST/session timing, filters, weekend bounds, pivots, financial denominators, private journal identity isolation, recomputed metrics, ETag conflicts, immutable reviews, MIME signatures and attachment ownership.

The managed development preview was used to verify the overview, news search, saved briefing, sample calculations, private snapshot save/restore and daily-review save/restore. Preview data is ephemeral; it is never uploaded to production storage. Actual MT5 account reads and automatic AI coaching are unverified.
