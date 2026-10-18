# AI Gold Institutional Tutor

A proposed gold research terminal and trade journal for the **Gold Institutional Trading** project, with the education and AI Tutor roadmap retained for later releases.

> [!IMPORTANT]
> ## Living Source of Truth — Notion
> The current product plan, curriculum, AI Tutor rules, visual/video asset plan, Content Bible, engagement strategy, roadmap, and methodology decisions are maintained in the **[Gold Institutional Trading — Course + AI Tutor + Content Bible Plan](https://app.notion.com/p/3e19e94cf0a4819bbabcd5b00f722bf7?pvs=204)**.
>
> **Notion is the living knowledge source.** Routine business, curriculum, methodology, content, and product-planning changes should be made in Notion rather than copied into this repository. GitHub remains the system of record for source code, schemas, tests, deployment configuration, and versioned technical contracts needed to reproduce the application.
>
> Before implementing a feature, check the Notion plan for current product intent. If a non-code product decision conflicts with stale GitHub prose, use the Notion plan as the current source and reconcile any affected versioned technical contract through an issue/PR.

## Knowledge governance

| Information | System of record |
| --- | --- |
| Product vision, roadmap and business decisions | **Notion** |
| Course curriculum and lesson planning | **Notion** |
| Visual/video asset planning | **Notion** |
| Content Bible and engagement strategy | **Notion** |
| Evolving methodology notes and research | **Notion** |
| Application source code | **GitHub** |
| Database migrations/schemas used by the app | **GitHub** |
| Versioned scoring implementation and AI release contracts | **GitHub** |
| Tests, CI/CD and deployment | **GitHub** |

**Proposal note:** The terminal/journal PRD versions Dennis’s proposed next-release technical scope. The Notion course plan has not been overwritten. If the proposal is adopted, reconcile the release roadmap in Notion; keep implementation contracts reproducible in GitHub.

**Maintenance rule:** Do not manually mirror routine Notion edits into this README. Update GitHub when a change affects code, schemas, tests, deployment, security, or another versioned implementation contract.

## Proposed next MVP

Build a **Gold Research Terminal and Trade Journal**: fundamental news and market context alongside reviewed statements, screenshots, daily performance analysis, and one measurable improvement for the next session. Bloomberg-style describes the information-dense interface; this project has no Bloomberg affiliation or data rights.

- **Start here:** [Proposed MVP PRD](docs/PRD.md)
- **Build sequence:** [Implementation plan](docs/MVP-IMPLEMENTATION-PLAN.md)
- **Calculation and evidence rules:** [Metrics contract](docs/METRICS-SPEC.md)
- **Visual reference:** [Terminal wireframe](https://gold-fundamentals-desk-dennis.dennis-klicksmartai.chatgpt.site)

The repository remains documentation-only. The separate wireframe is a local-interaction preview with unconnected providers; it is not a production app built from this repository.

## Core workflow
Prepare → Plan → Trade externally → Upload statements and screenshots → Reconcile → Daily analysis → Test one improvement

## Core methodology
- Asia → London imprint → New York classification
- New York archetypes: Pullback, Continuation, Reversal, Sideways
- Intermarket compass → H1/M30 location → M15 permission → M5 confirmation → M1 execution
- Daily Open, VWAP, VAH, VAL, POC, pivots, volume profile
- Liquidity sweeps, FVGs, order blocks, MSS/CHoCH/BOS, displacement, retest
- TDI/MACD/EMA as execution confirmation layers

## MVP scope
1. Gold fundamentals and delayed regional news across Asia, London/Europe, and US/New York.
2. DXY, oil, yields, BTC context, and a focused crypto-news desk.
3. Gold price, daily open, pivots, daily and weekly VWAP with explicit source/availability states.
4. Sessions, trade ideas, private screenshots, reviewed statement imports, and execution reconciliation.
5. Win rate, profit factor, expectancy, and evidence-qualified MAE/MFE.
6. Daily decision-quality review, rule-adherence coverage, and one measurable experiment.
7. Existing Notion journal access and optional confirmed export.

Start with a durable CSV journal and daily review, then add verified research adapters. No streaming news or automated execution is required. Course delivery, tutor chat, entry-quality scoring, and the Content Bible remain a later roadmap; see the [previous tutor PRD](docs/reference/AI-GOLD-TUTOR-PRD.md).

## Future Entry Quality model
- Location Quality — 20
- Liquidity Event — 20
- M5 Structure/Displacement — 20
- Retest Quality — 15
- VWAP/Volume Profile/Pivot Confluence — 10
- Momentum/TDI Confirmation — 10
- Entry Efficiency/Structural SL — 5

The score measures **entry quality, not probability of winning**.

## Product guardrails
- Educational and analytical; no guaranteed outcomes.
- A winning trade is not automatically a high-quality trade.
- Classification and entry scoring remain separate.
- Every score requires visible or user-supplied evidence.
- Unknown evidence remains unknown.
- Avoid unsupported claims about hidden institutional intent.
- Regulatory/compliance review is required before commercializing personalized actionable outputs.

## Planned stack
- Next.js + TypeScript
- Tailwind CSS
- Clerk or equivalent auth
- Supabase/Postgres
- Supabase Storage
- Multimodal LLM with structured outputs
- Retrieval over curated course/system documents
- Notion for curriculum/editorial planning
- GitHub for source, issues, releases and technical docs

## Project documentation
- **Living product/course/content plan:** [Notion — Gold Institutional Trading Course + AI Tutor + Content Bible](https://app.notion.com/p/3e19e94cf0a4819bbabcd5b00f722bf7?pvs=204)
- **Versioned product requirements:** `docs/PRD.md`
- **Technical architecture:** `docs/ARCHITECTURE.md`
- **AI Tutor implementation contract:** `docs/AI-TUTOR-SPEC.md`
- **Entry Quality implementation rubric:** `docs/ENTRY-QUALITY-RUBRIC.md`
- **Initial content implementation reference:** `docs/CONTENT-BIBLE.md`

- **TradingView connection setup and evidence contract:** [TradingView integration](docs/TRADINGVIEW-INTEGRATION.md)

