# Gold Research Terminal and Trade Journal MVP

Version 2.2 proposal · 18 October 2026 · Product owner Dennis Eng

## 1 Product decision

Propose the next MVP as a gold-focused financial research terminal that also acts as a trade journal. The trader prepares with fundamental news and intermarket context, records a thesis, uploads broker statements and screenshots, reviews actual results, and chooses one measurable improvement for the next session. A separate Discord Gold Tutor provides questions, lessons, practice, and screenshot-review conversations through the shared evidence and knowledge services.

The requested Bloomberg-style direction means a compact, connected research workspace. The product name is **Gold Research Terminal**; it has no Bloomberg affiliation, data entitlement, or promise of feature parity.

This proposal replaces the course-first launch sequence in the previous PRD. The Discord Tutor is a companion MVP, while full course delivery, scoring research, and the Content Bible remain later work; the original PRD is preserved at [AI Gold Tutor reference](reference/AI-GOLD-TUTOR-PRD.md). Existing methodology stays in the [living Notion plan](https://app.notion.com/p/3e19e94cf0a4819bbabcd5b00f722bf7). This document versions the proposed implementation scope, not a new trading strategy. Dennis's current request takes precedence over the earlier launch order.

## 2 Current state and evidence

This repository contains planning documents, not an implemented production app. The separate [V5 visual wireframe](https://gold-fundamentals-desk-dennis.dennis-klicksmartai.chatgpt.site) demonstrates ten views, blank market references, regional and crypto coverage templates, local evidence selection, reviewed CSV net-result calculations, and daily review drafts.

The wireframe is not OpenBB Workspace and is not a deployed version of this repository. Local CSV metrics are a prototype, not broker reconciliation. Browser visual QA was unavailable during its creation. No market/news feed, historical-path service, secure cloud upload pipeline, automatic AI coaching, or Notion synchronization has been verified as connected. Build and test those capabilities before describing the app as production-ready.

## 3 First user and outcome

Launch privately for Dennis, a Vancouver-based discretionary gold trader. Gold is primary; BTC/crypto provides a focused additional news and reference desk. Support paper, replay, and live-account records as explicitly separate modes. Do not mix their performance.

The product should reduce fragmented research and make review repeatable. Success means reliable evidence, reconciled results, fewer repeated confirmed process breaches, and completion of a measurable review experiment. Increased profitability is an intended outcome to evaluate, not a guarantee or acceptance condition.

Core loop:

**Prepare → Plan → Trade externally → Upload → Reconcile → Review → Test one improvement**

## 4 MVP boundary

| Deliverable | MVP requirement | Later work |
|---|---|---|
| Research desk | Gold/DXY, oil, rates, macro events, regional news and reports | Professional squawk, X streaming, broad asset coverage |
| Gold references | Price, daily open, classic pivots, daily and weekly VWAP slots with availability states | Advanced chart tools and automated setup detection |
| BTC and Crypto | BTC reference, focused news, on-demand weekend digest | Altcoin trading, on-chain and liquidation platforms |
| Journal | Sessions, ideas, fills, planned risk, screenshots, immutable thesis snapshots | Broker execution and continuous account control |
| Imports | CSV plus PDF/PNG/JPEG evidence; reviewed extraction and reconciliation | Unbounded broker-format support and video capture |
| Analysis | Win rate, net P/L, profit factor, expectancy, known process adherence | Automatically inferred behavioural labels |
| Excursions | Eligibility and explicit missing-data states; validated path calculation when supported | Universal exact MAE/MFE across all feeds and scaled positions |
| Daily review | Evidence-linked findings and one measurable improvement experiment | Full courses and automatic entry-quality scoring |
| Discord Gold Tutor | Curated Q&A, lessons, practice, screenshot review, and private journal handoff in a separate deployable | Voice, ambient channel monitoring, automated broadcasts |
| Notion | Existing journal links, manual evidence export; optional confirmed write after validation | Automatic bidirectional synchronization |

Automatic trade calls, orders, risk increases to meet income goals, and promises of profitable outcomes are excluded. No streaming feed is required. Delayed, timestamped news is sufficient.

## 5 Two applications and shared services

| Application | Primary experience | Deployment boundary |
|---|---|---|
| Gold Research Terminal | Web research, market/news context, private uploads, journal, reconciliation, metrics, and daily review | apps/terminal-web |
| Gold Tutor on Discord | Command-driven questions, curated lessons, practice, screenshot explanations, and private journal discussion | apps/discord-tutor |

Start in this repository as a monorepo with two independently deployed apps, shared contracts, a curated knowledge service, private evidence service, and an authorized journal/metrics API. This is not a request to fork repositories or provision services. Identity linking is explicit; Discord roles or display names do not grant access to trading records. Tutor failures must not disable the web journal.

The companion [Discord Tutor PRD](DISCORD-GOLD-TUTOR-PRD.md) defines commands, delivery, private-data boundaries, and rollout. Web journal import/reconciliation remains authoritative for financial records; Discord explains approved metrics and cannot infer fills or approve statement extraction.

### Notion initiated tutor service

The Notion journal is an event source for explicit review requests. Ready for AI Review → verified adapter and durable queue → shared tutor service → validated review written to Notion → optional private Discord completion notification → follow-up coaching. The [trigger contract](NOTION-TUTOR-TRIGGER.md) defines schema additions, ownership, evidence gates, source versions, idempotency, loop prevention, and delivery failure states. Nothing is activated by the documentation change.

## 6 Screens and workflow

Preserve the wireframe's ten-view navigation: Overview, News and catalysts, BTC and Crypto, Intermarket monitor, Reports library, Price references, My briefing, Imports and analytics, Daily trade analysis, Data connections. Include a clear route to the journal from review screens; journal entities are part of the application, not another market-analysis tab.

### Prepare

Overview prioritizes the session handover, material news, next catalysts, DXY versus gold, oil, and rates. The ticker and reference strip remain compact. Every value has an instrument, source, unit, observation timestamp, retrieval timestamp, and freshness/delay state. A latest bar close is not labeled a live tick.

News filters combine Asia, London/Europe, US/New York, and Global with topics and assets. Geographic origin and affected session are separate. A significant China event can remain relevant through the US session. Official releases, source reports, and original links take priority over interpretation. Deduplicate stories and preserve corrections.

Initial desk cutoffs are configurable reporting times: Asia 09:00 Asia/Tokyo; Europe 08:00 Europe/London; US 08:00 America/New_York. They are not ICT kill-zone definitions or universal market-open times. Store UTC and show America/Vancouver with date-aware timezone conversion.

### Plan and journal

Create a Session and one Trade Idea per thesis. Store instrument/venue, mode, original thesis, planning time, source-backed briefing snapshot, relevant reference levels, planned entry/stop/targets, original approved cash risk, and management plan. Multiple entries and partial closes link to one idea. Preserve the original thesis; later events enter a timestamped management log.

Use the existing Notion structure as the integration target: Sessions, Trade Ideas, Executions, and Weekly Reviews. The application's normalized records are the calculation source; Notion is the review destination, and broker originals remain the financial evidence. Human edits and export identities must be preserved.

### Upload and reconcile

Accept CSV broker exports, PDF daily statements, and PNG/JPEG screenshots. CSV is the preferred financial source. Proposed bounds: 20 files, 20 MB each, 100 MB per batch. Validate actual content/MIME, use private storage, and retain original hashes and parser versions.

Flow: select → store privately → parse/extract → map → review confidence and conflicts → reconcile → confirm → calculate. Candidate extraction is never automatically a confirmed trade. Document the first supported broker format; unsupported statements stay as evidence with a reason, not fabricated rows.

Keep source account, currency, broker timezone, execution/deal IDs, row type, costs, and gross/net semantics. Separate cash flows, open positions, and canceled orders. Detect overlapping statements using execution identity and partial-close identity. Hash matching alone is insufficient. Review ambiguous duplicates and idea grouping. Preserve revisions and provenance.

Confirm that reported profit does not already include fees before adding commission/swap again. Reconcile statement totals and balances where evidence exists. Do not combine currencies without an explicit conversion method. See [metrics contract](METRICS-SPEC.md).

### Daily trade analysis

Select date, verified timezone, account/currency, instrument, mode, and grain. Use confirmed records. Review readiness, results, original plan versus actions, decision quality, evidence gaps, and one primary experiment.

A disciplined loss and an undisciplined win are different outcomes. Do not infer emotion or rule violations from P/L. Rubric items are Followed, Breach, Unknown, or Not applicable. Show known-check coverage beside adherence. Preserve existing loss-stop policy in the journal; do not count partial fills as separate losing ideas.

The daily review records up to three supported findings, the best disciplined decision, one issue to investigate, competing explanations, and one experiment with a measurable target, evidence requirement, and evaluation window. AI drafts explanations; code calculates all metrics. Dennis reviews conclusions before approval.

Example experiment: document a timestamped thesis and approved risk before every new idea over the next five reviewed sessions. Compare adherence and coverage; do not prescribe larger position sizes.

### BTC and weekend review

Show BTC with exact spot pair/venue and defined rolling 24-hour change. Keep BTC/USD separate from BTC/USDT, and spot separate from derivatives. Cover BTC/ETH, ETFs and institutional adoption, regulation, security/exchange events, and stablecoins. Deprioritize promotions and routine small-token stories.

An on-demand weekend digest begins at Friday 16:00 America/New_York and ends at its explicit cutoff; this is an editorial window. Closed traditional markets display last available observations. Do not manufacture weekend gold/DXY correlations by forward-filling prices. No external reminder or background message is created by this feature.

## 7 Data strategy and source gates

TradingView MCP is a candidate for quotes, bars, news, and calendar information after authorized capability tests. Follow [TradingView integration](TRADINGVIEW-INTEGRATION.md). An assistant's connection is not automatically a website credential, and a local Desktop bridge is not automatically reachable by a hosted app. No tokens/cookies in source control. Use the actual discovered tool schema; never guess symbol identifiers.

Use TradingView news where supported, official institutional releases for verification, and Marketaux's free tier for coverage gaps. Evaluate CoinDesk RSS as a supplemental crypto source with publisher terms checked. FRED and EIA are candidates for appropriately timed macro/energy series, not substitutes for trading quotes. Marketaux is news, not a price or volume feed.

Initial news polling is 30 minutes with cache reuse and quota-aware manual refresh. The documented Marketaux free plan checked during planning had 100 requests/day and three articles/request; recheck at implementation. Initial budget: 48 base, 24 shared regional/crypto requests, 28 for retries/pagination/reserve. Filters never create upstream calls. Limited responses mean incomplete coverage; do not advertise exhaustive breaking news.

Use bounded batched quote requests, proposed 60-second refresh when open and permitted. Track unavailable, disconnected, stale, delayed, partial, and closed-market states separately. Slower reports retain observation/reporting periods and publication dates. A no-new-stories response can be a successful feed check.

OpenBB remains an optional research surface over the same normalized API through widget/app definitions. It is not a mandatory frontend or an all-in-one free feed. Do not maintain a duplicate data pipeline.

## 8 Reference conventions

- Gold instrument: explicitly choose XAUUSD broker/feed; GC futures is a separate series. Never transfer prices or volume silently across them.
- Daily open: first valid bar open at/after midnight America/New_York within a configured five-minute tolerance; disclose the actual timestamp. This differs from the futures evening open.
- Pivots: classic variant using prior completed configured trading session H/L/C; store source and session bounds. P=(H+L+C)/3; R1=2P−L, S1=2P−H; R2=P+H−L, S2=P−H+L; R3=H+2(P−L), S3=L−2(H−P).
- Daily/weekly VWAP: instrument-calendar session/week anchors; show anchor, price/volume source, interval, history completeness, and estimate class. Completed-bar TP=(H+L+C)/3 weighted by V is an approximation. Zero total volume is unavailable. No fabricated spot volume or silently truncated week. Preserve futures contract/roll policy.
- DXY and BTC comparisons: matching time windows, aligned observations, and source identities. Historical correlation uses paired returns with sample size and method; no causal or deterministic trading labels.

Reference slots may be unavailable when evidence is insufficient. Releasing a useful journal does not authorize calling missing VWAP or MAE/MFE implemented. Full-reference acceptance requires validated sources and complete history.

## 9 Architecture and records

Use the existing Next.js/TypeScript direction, an authenticated API, PostgreSQL, private object storage, background parsing/ingestion jobs, deterministic analytics, and a structured AI review service. Begin with the existing deployment conventions after validating them. Python/FastAPI is optional for provider/analytics workers if justified; do not require a second stack for simple calculations.

Logical records: users/accounts; instruments/calendars; observations/bars/references; news/events/reports; sessions; ideas; executions and revisions; cash flows; uploads/extraction candidates/import reviews; evidence links; metric runs; price-path coverage; daily review versions/process assessments; experiments; connection credentials by secure reference; Notion export mappings.

All records and downloads enforce owner access. Source timestamps and corrected values retain version history. Object storage uses signed, short-lived URLs. Parse untrusted PDFs/images in bounded workers; defend against malicious files, embedded links, and prompt injection. Models cannot alter verified financial results or invoke broker tools.

Snapshots link input record IDs, calculation/rubric/model versions, cutoff, scope, and quality. New corrected imports invalidate freshness, not historical approvals. Recompute into a new version. Export one selected review to Notion only after user confirmation and use idempotency keys; no automatic overwrites or duplicate ledgers.

## 10 AI contract

A briefing separates facts, observed market response, interpretation, competing explanations, catalysts, and gaps. Every factual claim links to source evidence available by the cutoff. A publication time is not replaced by retrieval time.

A daily review uses deterministic metrics plus saved plans, screenshots, and user-confirmed assessments. It cannot infer hidden institutional intent, emotions, missed profits, exact excursions, or trade grouping without evidence. Missing evidence remains unknown. Entry Quality and Behaviour scoring in the existing tutor contracts are future modules, separate from current adherence; adherence is not a probability of winning.

## 11 Delivery slices and release gates

| Slice | Deliverable | Exit gate |
|---|---|---|
| A Foundation | Private auth, journal entities, original-file storage, CSV mapping/review | Owner isolation and durable state; original records remain auditable |
| B Daily improvement | Reconciled metrics, daily review/rubric, experiment tracking, Markdown export | Deterministic fixtures and complete import-to-review flow pass |
| C Research context | Gold/DXY core references, delayed regional news/calendar, oil/rates context, BTC desk | Actual authorized calls and quality states verified; source gaps disclosed |
| D Evidence enrichment | PDF/image extraction review, eligible price-path excursions, optional Notion export | Human review, matching-path evidence, idempotent writes verified |

A+B form the first usable journal increment. C completes the proposed terminal-plus-journal MVP. D is staged enrichment: accept all supported evidence formats in A but do not block a useful CSV journal on universal OCR or price-path support. VWAP and excursion status must remain honest until their gates pass. The [implementation plan](MVP-IMPLEMENTATION-PLAN.md) defines executable work packages. Build the Discord educational slice alongside these stages; private daily-review retrieval depends on the authorized journal API. Separate deployment gates prevent the bot from blocking the first usable web journal.

## 12 Acceptance and validation

- Persist a confirmed trade idea and uploaded evidence across authenticated reloads; another user cannot access them.
- Reimport identical and overlapping statements without double-counting; distinguish cash flows, open positions, executions, and completed ideas.
- Validate win-rate denominator, net-cost semantics, currency, timezone, zero-loss/no-trade states, and optional-risk coverage against [metric fixtures](METRICS-SPEC.md).
- Produce a daily review with reproducible metrics, supported findings, known/unknown adherence coverage, and one experiment. Include disciplined-loss and profitable-breach cases.
- No statement-only import can produce exact MAE/MFE. Missing path, boundary bars, venue mismatch, scaling, and partial closes downgrade/suppress excursions appropriately.
- Quotes/news carry actual source/observation/retrieval times and fail safely under partial provider outages; delayed news is accepted.
- BTC weekend context does not imply closed gold/DXY markets are live.
- Confirmed Notion exports return exact destination URLs, resist retries, preserve original theses, and leave unconfirmed data unexported.
- Complete browser QA for desktop/mobile, keyboard navigation, empty/loading/error states, uploads/review, and evidence/source drawers before release.
- Do not claim implementation from a static preview, provider documentation, or an untested connector setup.

## 13 Pilot and open decisions

Pilot with ten reviewed trading sessions plus a weekend scenario. Targets: useful preparation in five minutes; all factual claims traceable; all computed values reproducible; no duplicate confirmed fills; daily review completed for at least eight pilot sessions; one measurable experiment tracked through evaluation. Report sample counts and missing coverage with any performance trend.

Before coding provider-specific integrations, verify: target broker export and timestamp convention; account currency; XAUUSD/DXY/BTC sources; volume and full-week history; permitted TradingView deployment; news/report display rights; object storage/auth choices; cost budget; and Notion schema. None of these is established by this proposal. They do not block fixtures and provider-independent journal contracts.

## References

- [Notion journal tutor trigger](NOTION-TUTOR-TRIGGER.md)

- [Discord Gold Tutor MVP](DISCORD-GOLD-TUTOR-PRD.md)

- [Visual wireframe](https://gold-fundamentals-desk-dennis.dennis-klicksmartai.chatgpt.site)
- [Metrics and evidence contract](METRICS-SPEC.md)
- [Implementation plan](MVP-IMPLEMENTATION-PLAN.md)
- [Existing Notion journal](https://app.notion.com/p/3d99e94cf0a48114a318cd8bf84d6e49)
- [Trade journal companion](https://app.notion.com/p/3fd9e94cf0a481eba016d7abe32454fd)
- [Official TradingView MCP](https://www.tradingview.com/mcp/docs)
- [Marketaux documentation](https://www.marketaux.com/documentation)
- [OpenBB data integration](https://docs.openbb.co/workspace/developers/data-integration)

Private source links may require Dennis's access. Never copy real statements, account identifiers, screenshots, balances, OAuth responses, or private source text into this public repository. Use synthetic fixtures only.
