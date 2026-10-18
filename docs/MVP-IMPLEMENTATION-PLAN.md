# Terminal and Trade Journal MVP Implementation Plan

Status: proposed work packages, not completed features. Read [PRD](PRD.md), [metrics contract](METRICS-SPEC.md), and [TradingView evidence contract](TRADINGVIEW-INTEGRATION.md) first. Existing course and entry-quality contracts apply only to their later modules. Do not promote a local-only preview into a production claim.

## 1 Start with repository and capability validation

This repository currently has documentation only. Choose and record the initial framework/auth/database/storage implementations before scaffolding. Follow existing Next.js/TypeScript direction unless a material blocker justifies a documented alternative. Use PostgreSQL and private object storage behind explicit owner authorization. No credentials or real trading records belong in Git.

Resolve one representative broker CSV shape and timezone/cost semantics. Maintain a provider matrix with verified/unverified state for gold, DXY, BTC, oil/rates, news/calendar, volume history, and Notion. Authenticate and make actual read-only calls before describing any integration as connected. An unavailable data provider must not block journal development.

## 2 Work packages

| Package | Build | Dependency | Definition of done |
|---|---|---|---|
| WP01 Private foundation | Auth, owner-scoped account/session/idea entities, database migrations, private evidence objects | Stack decision | Persistent private records; negative cross-user access tests |
| WP02 Import and review | CSV adapter, PDF/image evidence upload, extraction-candidate lifecycle, mapping and confirmation UI | WP01 | Unsupported data fails clearly; originals retained; no auto-confirmed trades |
| WP03 Reconciliation | Execution identity/revisions, costs, cash flows, duplicates, idea links | WP02 | Overlapping exports cannot duplicate totals; financial semantics auditable |
| WP04 Metrics engine | Deterministic scorecards, eligibility/exclusions, grain/date/currency controls | WP03 | All METRICS-SPEC fixtures pass |
| WP05 Daily improvement | Frozen daily snapshot, process rubric, evidence/lesson review, one experiment, approval versions | WP04 | Complete import-to-reviewed-lesson flow; independent outcome/process labels |
| WP06 Research desk | Normalized source adapters, quality states, regional delayed news/calendar, gold/DXY and oil/rate context | Provider validation | Actual authorized data or explicit unavailability, accurate timestamps |
| WP07 Gold references and BTC | Daily open/pivots, validated VWAP slots, BTC desk and weekend review | WP06 | No silent feed substitutions; full-week coverage or honest gaps |
| WP08 Structured extraction | Text-PDF/OCR adapters, per-field confidence review, evidence linkage | WP02/03 | Human-reviewed extraction; unreadable/ambiguous inputs remain unresolved |
| WP09 Evidence-backed analysis | Structured AI brief/review with deterministic validation and source IDs | WP05/06 | Unsupported claims rejected; model cannot overwrite broker facts |
| WP10 Optional enrichments | Matched-path excursions, confirmed Notion export, OpenBB surface | Separate access gates | Method/coverage verified; writes idempotent; same normalized contracts |

WP01–05 deliver the first usable journal. WP06–07 add the terminal experience. WP08–10 can be staged, with limitations explicit. Do not delay reconciled CSV analysis for universal OCR, streaming news, full course content, or exact excursions for every broker.

## 3 Suggested application boundaries

- Web: ten reference screens, journal views, upload/review states, daily improvement loop, accessibility.
- Domain: sessions/ideas/executions/cash flows, immutable plans and approved review versions.
- Import workers: bounded parsing/OCR, normalized candidates, original-source references, no financial overwrites.
- Analytics: pure functions for metrics/references, coverage and provenance, reproducible input IDs.
- Research adapters: quote/bar/news/calendar/report interfaces; no provider-specific fields leaking into core journal logic.
- AI: structured explanations with source validation; no broker write tools.
- Notion: one-way confirmed export initially; retain destination mapping and idempotency; no bidirectional sync.

Prefer the simplest deployable architecture with one source of truth for normalized calculations. Add Python workers only for justified library/provider needs. OpenBB is optional and uses the same API. Keep credentials in server-managed secrets and tokens revocable; never expose a local Desktop debugging endpoint.

## 4 Suggested contracts

Domain services should support bounded authenticated endpoints for:

- Upload preparation/finalization and batch status.
- Extraction candidates, column mapping, duplicate resolution, review, and confirmation.
- Session/idea CRUD and execution associations, with plan history preserved.
- Analytics summary by account/currency/mode/day/grain with eligibility and exclusions.
- Daily review draft, edit, approve, regenerate-as-new-version, and experiment evaluation.
- Market/reference snapshots, news/calendar/report queries, freshness and connection health.
- Explicit Notion export, returning a verified URL and stable export identity.

Each implementation PR defines request/response types and migrations. Untrusted source text is evidence, not an instruction to fetch arbitrary URLs, change configuration, or call tools.

## 5 Test and release strategy

Test pure financial calculations with the listed fixtures, then adapters with synthetic broker exports and missing-field/duplicate/correction cases. Validate authorization on both records and original-file downloads. Use a fake provider for outage/rate-limit/expiry tests and an actual authorized call for capability validation.

End-to-end acceptance path: create a Session/Idea → upload a synthetic statement and screenshot → map/reconcile/confirm → calculate metrics → record evidence-backed daily review → choose one experiment → reload durable state → export explicitly to Notion if configured. Verify revoked credentials stop future provider jobs. No automated orders or messages.

Browser QA is required for the built app: desktop/mobile, keyboard operation, readable tables, error and loading states, original-file preview, duplicate resolution, and draft approval. Check that unknown data never becomes zero or assumed adherence.

The V5 standalone wireframe is a visual reference only. It does not satisfy durable storage, authentication, extraction, live provider, AI review, or reconciliation gates. The first pilot covers ten trading sessions and a weekend; report process coverage alongside any financial trends.

## 6 Handoff requirements for Codex or Claude Code

Deliver small reviewable implementation changes. Keep completed work, unverified integrations, and deferred work distinct in each PR. Include migration and rollback notes where relevant, synthetic fixtures, meaningful tests, setup instructions without secrets, and observed checks. Do not copy real statements or private Notion page contents into this public repository. Do not change the trader's methodology, risk rules, or scoring rubrics merely to make a test pass.
