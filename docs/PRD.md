# Gold Research Terminal and Trade Journal MVP

Version 2.5 proposal · 18 October 2026 · Product owner Dennis Eng

## 1 Product decision

Propose the next MVP as a gold-focused financial research terminal that also acts as a trade journal. The trader prepares with fundamental news and intermarket context, records a thesis, uploads broker statements and screenshots, reviews actual results, and chooses one measurable improvement for the next session. A separate Discord Gold Tutor provides questions, lessons, practice, and screenshot-review conversations through the shared evidence and knowledge services.

The requested Bloomberg-style direction means a compact, connected research workspace. The product name is **Gold Research Terminal**; it has no Bloomberg affiliation, data entitlement, or promise of feature parity.

This proposal replaces the course-first launch sequence in the previous PRD. The Discord Tutor is a companion MVP, while full course delivery, scoring research, and the Content Bible remain later work; the original PRD is preserved at [AI Gold Tutor reference](reference/AI-GOLD-TUTOR-PRD.md). Existing methodology stays in the [living Notion plan](https://app.notion.com/p/3e19e94cf0a4819bbabcd5b00f722bf7). This document versions the proposed implementation scope, not a new trading strategy. Dennis's current request takes precedence over the earlier launch order.

## 2 Current state and evidence

This branch includes the runnable [local MT5 journal](../apps/mt5-journal/README.md): native MCP read transport, CSV/JSON review, deterministic completed-position metrics, SQLite daily reviews and evidence export. Actual broker-account connectivity remains unverified; the hosted interface cannot reach a desktop loopback endpoint.

The separate private [research dashboard](https://gold-fundamentals-desk-dennis.dennis-klicksmartai.chatgpt.site) now serves source-linked news snapshots and Asia/London/New York Session Briefings through shared persistent news storage. Its initial eight stories were sourced directly from Reuters, World Gold Council, BLS, Barron's/Dow Jones and WSJ/Dow Jones. They were not supplied by OpenBB, Marketaux, Eulerpool or MT5. Shared news write/readback was verified, and three pre-session cloud tasks were saved and enabled; scheduled execution has not yet been verified. The Sites-hosted implementation has a separate source repository and is not automatically reproduced by this GitHub checkout.

OpenBB has not been installed or connected. Marketaux's attempted workspace request returned HTTP 403 without establishing its cause; Eulerpool account/provider access is unverified. MT5 execution/reference feeds, exact MAE/MFE, cloud financial-record ingestion, automated AI coaching, Notion sync and the Discord application remain unimplemented or unverified. Browser visual QA remains unavailable. The dashboard is not OpenBB Workspace or a production-complete terminal.

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
| MT5 data adapter | Optional read-only collector for broker quotes, positions, fills/history, and eligible tick paths | Order execution, trade copying, universal broker coverage |
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

Use TradingView news where supported, official institutional releases for verification, and Marketaux's free tier for coverage gaps. The [Marketaux demo adapter](MARKETAUX-NEWS-INTEGRATION.md) provides one-shot gold/crypto news snapshots with a private environment token; its attempted provider request returned HTTP 403, so authentication and actual coverage remain unverified. Evaluate CoinDesk RSS as a supplemental crypto source with publisher terms checked. FRED and EIA are candidates for appropriately timed macro/energy series, not substitutes for trading quotes. Marketaux is news, not a price or volume feed.

News and Session Briefings refresh before Dennis's ICT windows, replacing the earlier 30-minute polling proposal: Asia at 19:45 America/New_York Sunday–Thursday; London at 01:45 and New York at 06:45 Monday–Friday. These are 15 minutes before the methodology's 20:00, 02:00 and 07:00 windows, not exchange opening times. Convert to America/Vancouver with current IANA rules. Reuse the three enabled schedules; do not create duplicate four-hour or per-provider tasks. A saved schedule is distinct from a verified successful run.

Each run researches source-backed news, preserves publication/report periods, writes a session-specific briefing with its own preparation time and news cutoff, retains other sessions, and verifies readback without republishing the app. On failure, retain the last successful content and its true timestamp. Filters reuse cached data. Marketaux remains a candidate adapter, with account entitlements, limits and display rights checked before activation. Limited results must never be described as exhaustive coverage.

Use bounded batched quote requests, proposed 60-second refresh when open and permitted. Track unavailable, disconnected, stale, delayed, partial, and closed-market states separately. Slower reports retain observation/reporting periods and publication dates. A no-new-stories response can be a successful feed check.


### Alpha Vantage research references

The authorized Alpha Vantage MCP connection was tested successfully on 18 October 2026 and five observations were saved and read back from the private dashboard: gold XAUUSD, BTC/USD, daily WTI, daily Brent and the nominal US 10-year Treasury constant maturity rate. They now populate the market snapshot, ticker and Session Briefing reference cards. This is a connector-published shared snapshot, not a browser-side provider connection or an MT5 execution feed. No provider secret is stored in dashboard code.

Each observation retains instrument, unit, provider function, raw observation date/time, timezone (including unspecified), actual retrieval time, reference type and limitations. Gold's returned timezone was unspecified and must remain so. Oil series are daily published EIA/FRED observations with lag, not futures quotes; the nominal yield is not the TIPS real yield. No cross-market change or correlation is derived from unmatched snapshots. News and saved briefing cutoffs remain independent of market-data refreshes.

The three existing pre-session tasks now include bounded sequential Alpha Vantage calls: gold and BTC per run; oil and yield only when the previous retrieval exceeds 24 hours. The connection returned a 25-request daily limit and one-request-per-second pacing requirement. Maximum five calls per run; no retries on rate limits. A provider data-level error counts as failure even when the MCP call itself succeeds. Retain prior dated observations on failure. Scheduled execution remains to be observed.

DXY, daily open, automatic pivots, daily/weekly VWAP, execution quotes and exact MAE/MFE remain separate evidence gates. The tested reference endpoints do not provide the complete session OHLCV/tick history needed to satisfy them. See [Alpha Vantage integration](ALPHA-VANTAGE-INTEGRATION.md).

### OpenBB research backend

Adopt OpenBB's Open Data Platform (ODP) as the planned integration layer for multi-provider market research. Its role is to access and normalize macroeconomic, rates, positioning and supported market datasets for the existing dashboard, Session Briefings and shared tutor evidence service. It is not currently connected, does not replace MT5 execution/account records, and does not grant free access or display rights to every provider. See [OpenBB research integration](OPENBB-RESEARCH-INTEGRATION.md) for the contract, provider gates and acceptance criteria.

Keep the current web dashboard as the primary interface. OpenBB Workspace is an optional future client of the same authenticated research service; do not build a duplicate pipeline or require a UI migration. Use OpenBB's Python/REST integration for backend jobs and optionally expose a restricted research MCP to the tutor. Discover installed V5 provider capabilities and pin tested package versions; do not copy V4 command paths without migration checks.

First increment: verified macro/rates series and gold CFTC positioning. Next: economic-calendar events and reference quotes/history where permitted. Each dataset carries the original provider, exact instrument/series, source observation/publication/retrieval times, revisions, units, delay and coverage. Derived results retain input lineage. No authenticated provider response means no populated value. News facts remain linked to the original publisher even if later retrieved through an OpenBB adapter.

### MT5 broker data

Add the optional [read-only MT5 adapter](MT5-DATA-INTEGRATION.md) on a verified Windows desktop/VPS running an authorized terminal. It supplies normalized broker observations and candidate executions through outbound authenticated ingestion. Prefer investor access, isolate credentials on the collector host, preserve partial-close/deal identity, and reconcile uploaded statements against synchronized records. Account/quote updates do not trigger the tutor; the explicit Notion review request remains the analysis gate. MT5 tick/bar availability can improve MAE/MFE evidence but does not guarantee exact measurements or centralized-volume VWAP.

## 8 Reference conventions

- Gold instrument: explicitly choose XAUUSD broker/feed; GC futures is a separate series. Never transfer prices or volume silently across them.
- Daily open: first valid bar open at/after midnight America/New_York within a configured five-minute tolerance; disclose the actual timestamp. This differs from the futures evening open.
- Pivots: classic variant using prior completed configured trading session H/L/C; store source and session bounds. P=(H+L+C)/3; R1=2P−L, S1=2P−H; R2=P+H−L, S2=P−H+L; R3=H+2(P−L), S3=L−2(H−P).
- Daily/weekly VWAP: instrument-calendar session/week anchors; show anchor, price/volume source, interval, history completeness, and estimate class. Completed-bar TP=(H+L+C)/3 weighted by V is an approximation. Zero total volume is unavailable. No fabricated spot volume or silently truncated week. Preserve futures contract/roll policy.
- DXY and BTC comparisons: matching time windows, aligned observations, and source identities. Historical correlation uses paired returns with sample size and method; no causal or deterministic trading labels.

Reference slots may be unavailable when evidence is insufficient. Releasing a useful journal does not authorize calling missing VWAP or MAE/MFE implemented. Full-reference acceptance requires validated sources and complete history.

## 9 Architecture and records

Use the existing Next.js/TypeScript direction, an authenticated API, PostgreSQL, private object storage, background parsing/ingestion jobs, deterministic analytics, and a structured AI review service. Begin with the existing deployment conventions after validating them. An OpenBB integration requires a separately hosted compatible Python research worker/service, typically with an authenticated REST boundary. Keep simple journal calculations in the existing deterministic service. The current Sites frontend/news service runs in a Worker environment; it cannot directly run the OpenBB Python packages. Do not silently provision infrastructure or claim a working OpenBB deployment from an architecture diagram.

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
| C Research context | OpenBB provider discovery, macro/rates and CFTC slice, session briefs, followed by eligible gold/DXY/oil/BTC references and calendar | Underlying provider calls, access rights, cache/freshness and saved evidence verified; no fabricated gaps |
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
- OpenBB integration passes the OBB acceptance gates in [the research contract](OPENBB-RESEARCH-INTEGRATION.md), including original-provider attribution, observation/revision dates, endpoint/permission checks, quota-aware caching and isolation from broker operations.
- Pre-session jobs update the intended upcoming session/date, preserve other briefings, use explicit news cutoffs and timezone-aware windows, and retain the last successful snapshot on failure. A fresh run must verify the saved briefing and its source links.

## 13 Pilot and open decisions

Pilot with ten reviewed trading sessions plus a weekend scenario. Targets: useful preparation in five minutes; all factual claims traceable; all computed values reproducible; no duplicate confirmed fills; daily review completed for at least eight pilot sessions; one measurable experiment tracked through evaluation. Report sample counts and missing coverage with any performance trend.

Before coding provider-specific integrations, verify: target broker export and timestamp convention; account currency; XAUUSD/DXY/BTC sources; volume and full-week history; permitted TradingView deployment; news/report display rights; object storage/auth choices; cost budget; and Notion schema. Existing news storage and schedule setup are recorded above; remaining provider, broker and production decisions are unresolved. They do not block fixtures and provider-independent journal contracts.

## References

- [OpenBB research backend contract](OPENBB-RESEARCH-INTEGRATION.md)

- [Notion journal tutor trigger](NOTION-TUTOR-TRIGGER.md)
- [Read-only MT5 broker data](MT5-DATA-INTEGRATION.md)

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


## Implementation checkpoint — 18 October 2026

The first runnable slice is [the local MT5 journal](../apps/mt5-journal/README.md). It implements native read-only MCP transport, tool discovery, explicit read arguments, CSV/JSON record review, scoped closed-position net metrics, daily notes/experiment, screenshot previews, evidence export and local SQLite review persistence. The hosted copy supports imports/downloads; direct broker reads require the local service beside MT5. These implementations do not imply that the broader production acceptance criteria above have passed. Actual MT5 account connectivity, browser visual QA, automatic deal reconciliation, continuous sync, cloud financial-record storage, Notion triggers, Discord and AI tutoring remain unverified or unimplemented as described in the app README.
