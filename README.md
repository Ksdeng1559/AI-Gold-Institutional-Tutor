# AI Gold Institutional Tutor

An educational XAUUSD application for the **Gold Institutional Trading** methodology.

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

See `docs/PRD.md` and `docs/ARCHITECTURE.md`.
