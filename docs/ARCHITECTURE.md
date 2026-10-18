# Architecture — AI Gold Institutional Tutor

## Two independently deployed applications

- apps/terminal-web: research terminal, uploads, journal, reconciliation, and daily analytics.
- apps/discord-tutor: signature-verified command handler, deferred responses, curated lesson/Q&A and screenshot-review flows.
- packages/contracts: shared identity, evidence, review, and metric envelopes.
- packages/tutor-core: reusable grounded tutoring and knowledge retrieval.
- packages/analytics: deterministic calculations; journal API exposes owner-scoped results.

Use shared knowledge/evidence services and an authorized journal API. Discord handlers do not bypass owner checks with broad database credentials. Verify explicit account linking; public course retrieval cannot include private trading records. No Discord Gateway or privileged message monitoring is required for the proposed HTTP command-only design; validate platform setup at implementation. The [Discord PRD](DISCORD-GOLD-TUTOR-PRD.md) is the companion interface contract. No bot or infrastructure has been deployed.

## Notion event adapter and tutor jobs

The [Notion trigger contract](NOTION-TUTOR-TRIGGER.md) adds verified webhook/polling ingress, a durable request queue, source snapshot builder, tutor worker, versioned Notion writeback, and a private-notification outbox. Only explicit Ready requests trigger jobs. Job identity, canonical-input hashing, per-page leases, and source rechecks prevent duplicates, self-trigger loops, and unlabeled stale results. Bot notifications require verified linking and opt-in; delivery failure cannot expose personal data publicly. Journal metrics remain deterministic and owner scoped.

## Proposed terminal and journal MVP extension

The next-release scope is proposed in [PRD](PRD.md), with [work packages](MVP-IMPLEMENTATION-PLAN.md) and a [metrics contract](METRICS-SPEC.md). The architecture below originally supported the course/tutor plan; it is a reusable baseline rather than an instruction to build every course service for the terminal MVP.

Add these logical modules to the existing authenticated web/API and private-data architecture:
- Research adapters → normalized observations/news/calendar/references → source-backed session briefs.
- Private uploads → parsing/extraction candidates → user review and reconciliation → confirmed executions and cash flows.
- Journal sessions/ideas and immutable plan snapshots → deterministic metrics → daily evidence review → one improvement experiment.
- Optional matched historical path → eligibility-qualified MAE/MFE, with method/coverage preserved.
- Optional confirmed Notion export → existing journal destination with idempotent mapping.

Code computes financial metrics. Models draft explanations and cannot replace broker evidence. Preserve owner isolation, raw source provenance, cost/timezone semantics, partial-close identity, and review versions. Delayed news is sufficient; no streaming provider or broker execution is required. OpenBB is an optional UI over the same normalized backend. Validate production stack choices before provisioning; no infrastructure is created by these documents.

## High-level architecture
User → Next.js Web App → Auth → Application API → AI Orchestrator → Multimodal LLM / Retrieval → Structured Review → Supabase

Supporting systems:
- Supabase Postgres: users, sessions, lessons, reviews, scores, outcomes
- Supabase Storage: chart screenshots and media metadata
- Notion: curriculum and editorial planning
- GitHub: source and technical docs

## Suggested monorepo
```
AI-Gold-Institutional-Tutor/
├─ apps/
│  ├─ terminal-web/
│  └─ discord-tutor/
├─ packages/
│  ├─ tutor-core/
│  ├─ scoring-engine/
│  ├─ chart-review/
│  ├─ course-content/
│  └─ shared-types/
├─ docs/
├─ supabase/
└─ tests/
```

## Core services
### Tutor Core
- system rules
- course retrieval
- response formatting
- lesson recommendations
- uncertainty handling

### Chart Review
Inputs:
- screenshots
- timeframe
- session
- optional trade metadata

Outputs:
- observations
- evidence references
- missing evidence
- classification
- thesis
- scoring inputs

### Scoring Engine
Deterministic validator for:
- component range checks
- total score = 100 max
- grade band
- hard gates
- missing-data flags

The LLM proposes evidence and component values; deterministic code enforces score rules.

### Journal Service
Stores:
- session
- trade idea
- planned/actual entry
- stop
- target
- Entry Quality
- Behaviour Score
- P&L
- R
- MFE/MAE
- diagnosis
- corrective action

### Course Service
- modules
- lessons
- quizzes
- progress
- mastery
- related setup examples

### Content Service
- Content Bible items
- Value Bombs
- CTA keywords
- diagnostic DM routing
- engagement metrics

## Data principles
- P&L must not rewrite historical Entry Quality scores.
- Screenshots are immutable source evidence after review submission.
- AI output must be versioned with model/prompt/rubric version.
- Every score component stores rationale.
- Unknown evidence is explicit.
- Outcome analytics are computed separately from setup scoring.

## Security/privacy
- Signed URLs for private screenshots.
- Row-level security for user journal data.
- Avoid public exposure of broker/account identifiers.
- Explicit consent before using user screenshots as course examples.
- Remove identifying/account information from public educational assets.

## Deployment
Recommended first deployment:
- Vercel for Next.js
- Supabase for Postgres/Auth-adjacent data/storage if Clerk is used for identity
- environment variables for model/API keys
- CI tests for schema and score validation

