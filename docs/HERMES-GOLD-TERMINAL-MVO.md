# Hermes Agent — Gold Terminal Minimum Viable Offer (MVO)
 
> **Status:** Implementation specification for paid pilot; not a declaration that integrations are live.
> **Living product authority:** [Gold Terminal MVO PRD in Notion](https://app.notion.com/p/4049e94cf0a4819ab4e0ff968446c8a8).
> **Related curriculum:** [Gold Institutional Trading — Course + AI Tutor](https://app.notion.com/p/3e19e94cf0a4819bbabcd5b00f722bf7).
> **Last scoped:** 2026-10-25.

## 1. Minimum viable offer

**Audience:** Self-directed XAUUSD traders using MT5 / TradingView.

**Offer hypothesis:** **$29/month** for *session intelligence + private screenshot review + trading journal*; validate currency, price acceptance and recurring usage during a paid pilot. Free lead magnet: public market overview, representative briefing/chart sample and opt-in Telegram channel. Premium moderator setups are **separate and later**, not part of the $29 entitlement.

**Primary acceptance journey:** Register → subscribe → receive Asia/London/NY briefing → privately upload chart to Discord → Hermes returns evidence-based interpretation → user explicitly saves chart/review against private trade idea → weekly review of verified records.

## 2. Hermes responsibilities and boundaries

Hermes is an orchestrator, **not** a trading execution engine or a substitute for human moderators.

| Workflow | Trigger | Inputs | Output | Human boundary |
| --- | --- | --- | --- | --- |
| Session briefing | Scheduled pre-Asia / pre-London / pre-NY | Timestamped XAUUSD market data, market news/calendar, manually verified completed VP screenshots/levels if supplied | Source-backed market context and conditional bull/bear/no-trade scenarios | Review ambiguous or significant commentary before public release |
| Vision chart analysis | Authenticated subscriber sends Discord DM/private upload | Image bytes, user/session, timeframe, source and capture time | Structured observation of visible VP, VWAP, liquidity, structure; unknown fields | Trader confirms any journal save |
| Journal assistant | User requests review/save | Existing trade idea, pre-entry thesis, authorized screenshots, confirmed executions | Draft observations, process review, weekly recap | No automatic writing or invented fill/financial figures |
| Telegram preview | Approved free content is available | Sanitized briefing excerpt | Free educational post / lead magnet CTA | No private journal data |
| Moderator distribution (later) | Moderator explicitly approves a setup | Public-approved entry zone, risk reference, targets, expiry | Telegram/Discord publication + status revisions | Proprietary setup method never ingested; regulatory clearance first |

No Jev, automatic Volume Profile extraction, automatic trade signals, copy trading, or live order execution in the MVO. No brokerage passwords should be requested.

## 3. Discord screenshot-analysis workflow

1. Confirm linked Discord identity and paid entitlement **server side**, not by prompt text.
2. Accept supported image attachment via **private DM** (or secured per-user interaction); check MIME, pixel dimensions, size and moderation/abuse controls.
3. Store image in a private bucket with owner ID, source (TradingView/MT5), instrument, timeframe, chart capture timestamp/timezone, server ingestion timestamp, retention policy, and optional session/idea IDs. Generate short-lived signed access.
4. Forward actual image content to a **tested vision-capable** model, via Hermes configured model/provider (OpenRouter where verified); reject text-only fallback that merely sees a Discord URL.
5. Ask for: observable price structure; visible POC/VAH/VAL/HVN/LVN; distinction completed vs developing profile; VWAP and session references where displayed; competing scenarios, invalidation, evidence gaps. Do **not** invent unreadable numeric levels or infer hidden moderator rules.
6. Return an educational chart review and a link/command to **Save to Journal**. Saving requires the user’s express action and an idempotency key; an uploaded chart is **not** a trade or a filled order.
7. Meter request and token/image spend per subscriber, and enforce quotas before invoking the model. Model failure or missing image should produce a transparent error, not fabricated analysis.

**Suggested initial pilot cap:** 20 screenshot reviews/month and 500 MB private attachments/user. These are cost-test **proposals**, not finalized entitlements. Provide deletion/export.

### Suggested structured review contract

```json
{
  "analysis_id": "uuid",
  "owner_user_id": "uuid",
  "source_image_id": "uuid",
  "symbol": "XAUUSD",
  "timeframe": "M30",
  "capture_time": null,
  "capture_timezone": null,
  "model_id": "configured-vision-model",
  "status": "draft",
  "observations": [
    {"type": "volume_profile", "claim": "POC visible", "price": null, "evidence": "chart visual", "certainty": "uncertain"}
  ],
  "market_scenarios": {
    "bullish": "conditional evidence",
    "bearish": "conditional evidence",
    "no_trade": "conflicts or missing context"
  },
  "missing_evidence": ["unreadable numeric scale"],
  "journal_idea_id": null,
  "saved_by_user": false
}
```

## 4. Session-briefing contract

- Run before three major sessions; store **America/New_York** session rules with DST conversion, while supporting subscriber display in **America/Vancouver**.
- Every report records generated_at, market evidence_cutoff, feed, quote type, news publication timestamps, source links and unavailable inputs.
- Context hierarchy: **H4/H1 → M30 location and validated VP → M15 permission → M5 structure → M1 refinement**.
- Use daily open, VWAP, pivots, PDH/PDL, session range, supply/demand, liquidity objectives and intermarket context **only if supplied**.
- NY archetypes: **Pullback, Continuation, Reversal, Sideways**. These are hypotheses, never probabilities or entry authorizations.
- Include *alternative scenarios* and a defensible **NO TRADE** outcome.
- Treat completed and developing Volume Profiles differently; only manually verified levels count as authoritative. Never use a final VP to explain a historical earlier decision.
- Generate one briefing per session for reuse by authorized audiences. Publish a selected sanitized preview to free Telegram and the full version to Gold Terminal/authorized Discord.
- Retry schedule errors idempotently; show stale-source warning and withhold unsupported numerical market claims.

## 5. Journal contract (adapt existing Pivot Precision design)

Preserve **Sessions → Trade Ideas → Executions → Weekly Reviews** as separate grains. One idea can have multiple broker fills/partial exits.

- Pre-entry immutable thesis, screenshot, evidence cutoff, intended entry/invalidation/risk, and session.
- Later actions are timestamped amendments, not revisions to what was known at entry.
- Broker statements/executions are authoritative for fills, commissions, swaps and actual P/L; chart images support *reasoning*, not financial reconciliation.
- Realized R only when original approved cash risk and reconciled net result exist; MAE/MFE requires matched price path, therefore deferred.
- No automatic journal writes from Discord analysis; **explicit Save** is required.
- Keep decision/process quality separate from winning/losing. Do not impose a platform-wide “two losses” or “three losses” rule; refer to method-version-specific policies.
- Private by default with Postgres RLS, signed media URLs and an audit trail.

References: [Journal Companion](https://app.notion.com/p/3fd9e94cf0a481eba016d7abe32454fd), [Pivot Precision](https://app.notion.com/p/3d99e94cf0a48114a318cd8bf84d6e49), [OODA](https://app.notion.com/p/3ff9e94cf0a481329899ee26ba2d9543), [Volume Profile module (proposed)](https://app.notion.com/p/4009e94cf0a4818d92c0de1aa06fe3bb), [AAA rules](https://app.notion.com/p/3fa9e94cf0a48140a64bdf3f0259ab2f).

## 6. Services, security and integration contracts

```text
Discord DM / private upload ──> Auth + entitlement + quotas ──> Media storage
                                       │                        │
                                       ▼                        ▼
                                  Hermes worker ──> Vision model provider
                                       │
                                       ▼
                              Analysis API / private journal
                                 (explicit save only)

Market data + news/calendar + verified VP ──> Hermes scheduled briefing
                                                 │
                                       ┌─────────┴─────────┐
                                       ▼                   ▼
                                  Gold Terminal       Telegram preview
```

**Web:** Existing Next.js/Vercel application where available. **State:** Supabase/Postgres with RLS. **Images:** private object storage with expiry/retention policy. **Worker:** persistent VPS/worker hosting Hermes/Discord gateway. **Model:** vision-capable model through OpenRouter if provider contract is verified. **Billing:** provider-agnostic recurring checkout, webhook verification, cancellation, entitlements and failed-payment grace policy.

Keep Discord and model tokens only in server secrets; rate-limit uploads, authenticate webhook signatures, prevent Discord prompt content from calling privileged tools, and log consent, data access and publishing. Users must be able to export/delete their records.

**Data validity:** Distinguish live vs delayed vs unavailable prices; confirm any commercial feed redistribution rights. Do not confuse spot XAUUSD broker tick-volume with consolidated COMEX exchange volume.

## 7. Minimum technical tasks, ordered

- [ ] Build sample landing page / demo briefing and $29 checkout test; verify currency displayed and cancellation.
- [ ] Confirm Vercel app, Supabase schema and Discord gateway baseline rather than assuming connections exist.
- [ ] Configure Hermes gateway and vision provider; test **actual screenshot ingestion**, not text-only image URLs.
- [ ] Connect server-verified Discord identity and per-user subscription entitlements.
- [ ] Implement scheduled pre-session briefings with timestamp and missing-data contracts.
- [ ] Implement private screenshot persistence + AI review + explicit Save-to-Journal.
- [ ] Implement Sessions/Ideas/Executions/Weekly Reviews minimal schema with RLS; validate a partial close.
- [ ] Add usage metering, spending caps, storage retention, backups and operational alerts.
- [ ] Pilot with five paying XAUUSD traders; track activation, review frequency, cost-to-serve and day-30 retention.

## 8. MVO acceptance and gating

**User path:** A paid subscriber can receive a valid briefing, upload a screenshot privately, receive an image-grounded report, explicitly save it to a journal idea, and review it later. Cancelling the subscription removes paid AI privileges without improperly deleting owned data.

**Truthfulness:** Under low-quality images, the model says “not visible” rather than hallucinating levels; under stale data it does not present a live quote.

**Isolation:** A user cannot see another subscriber’s images/trades; moderators cannot access private journals; no privileged tools available in public channels.

**Commercial pilot targets (hypotheses):** Five paid pilots, then ten; ≥70% journal activation; ≥50% weekly active pilot traders save at least one journal idea/review; ≥80% briefing delivery with timestamps; positive contribution margin after variable costs. Test pricing rather than assuming subscribers will renew.

**Regulatory launch gate:** Paid actionable XAUUSD setup publishing by moderators requires qualified jurisdiction-specific review before activation. Moderator private strategies are out of scope of the assistant knowledge base.

## 9. Defer until evidence supports investment

Jev setup classification, automated VP/POC extraction, chart scanning without screenshots, MT5 broker auto-sync, fully automated financial extraction, AI autonomous signals/orders, multi-moderator marketplace, and guaranteed live sessions.

**Change governance:** Update product/offering assumptions in linked Notion MVO. Update this file only when integration contracts, system safety, implementation acceptance tests or architecture need revision.
