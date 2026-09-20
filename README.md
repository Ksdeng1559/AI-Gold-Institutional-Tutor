# AI Gold Institutional Tutor

An educational XAUUSD application for the **Gold Institutional Trading** methodology.

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

**Maintenance rule:** Do not manually mirror routine Notion edits into this README. Update GitHub when a change affects code, schemas, tests, deployment, security, or another versioned implementation contract.

## Product goal
Teach traders to classify session context, evaluate **entry quality**, review screenshots, improve execution behaviour, and journal decisions independently of P&L.

## Core workflow
Course → AI Tutor → Visual Trade Review → Entry Quality Score → Behaviour Review → Journal → Setup Library → Continuous Improvement

## Core methodology
- Asia → London imprint → New York classification
- New York archetypes: Pullback, Continuation, Reversal, Sideways
- Intermarket compass → H1/M30 location → M15 permission → M5 confirmation → M1 execution
- Daily Open, VWAP, VAH, VAL, POC, pivots, volume profile
- Liquidity sweeps, FVGs, order blocks, MSS/CHoCH/BOS, displacement, retest
- TDI/MACD/EMA as execution confirmation layers

## MVP
1. AI Tutor chat
2. Course and lesson library
3. Multi-timeframe screenshot upload
4. Structured visual trade review
5. Entry Quality scoring
6. Behaviour scoring
7. Trade journal
8. Setup library
9. Progress analytics
10. Content/resource library

## Entry Quality model
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
