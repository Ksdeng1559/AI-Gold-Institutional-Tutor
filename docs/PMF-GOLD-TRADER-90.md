# Gold Trader 90 + Gold Terminal — PMF Implementation Contract
Status: hypothesis / pilot-ready specification (2026-10-24). Business positioning and curriculum decisions live in [Notion](https://app.notion.com/p/3e19e94cf0a4819bbabcd5b00f722bf7?pvs=204). This document specifies testable application behavior, events, and rollout gates; it does **not** claim PMF.

## Segments and jobs-to-be-done
1. **Curious beginner (Gold Trader 90):** “Help me decide whether gold trading is appropriate, learn the fundamentals, and assess my abilities within 90 days without risking living expenses.” Users seeking immediate income must see a prominent message that trading is *not* reliable short-term income.
2. **Intermediate XAUUSD trader (Gold Terminal):** “Help me prepare for a session, classify context, apply a repeatable setup and learn from my decisions.”
3. **Advanced trader (Trading Lab):** “Help me compare setup performance by session, regime and execution behavior.”

## Single platform / two entry journeys
- **Gold Trader 90** beginner mode: 30 days foundations, 31–60 simulated practice, 61–90 performance and readiness assessment. Progress is **competency-gated, not time-gated**. 90 days is curriculum length, not a promise to earn or to begin live trading.
- **Gold Terminal** professional mode: pre-session intelligence, market map, setup review, AI Tutor, journal and analytics.
- Shared identity, knowledge base, chart evidence objects, journal, grading contracts and analytics. Switching modes preserves progress.
- Academy, Terminal and AI Trading Lab are product workspaces, not separate contradictory recommendation engines.

## MVP vertical slice (ordered)
P0: responsive beginner onboarding + risk expectations, free pre-NY briefing with source/time/data freshness and neutral/bull/bear branches; lesson player + quiz; screenshot upload with timeframe, symbol and timestamp; AI explanation with citation and unknown-evidence state; simulated trade planner (entry, invalidation, stop, target and R); structured journal; funnel analytics.
P1: manual/approved live data integration (MT5/market provider licensing gates), basic volume-profile / VWAP contextual overlays, tutor progress feedback and weekly review.
P2: MT5 historical trade import, advanced MAE/MFE/expectancy, multi-session classification, comprehensive 12-week academy and paid tiers.
Explicit non-goals: brokerage execution, copy-trading, guaranteed signals, automated financial advice, income projections shown as likely outcomes.

## Golden path acceptance tests
1. Beginner completes risk expectations onboarding before first simulation exercise; no live-money trading CTA.
2. User chooses Gold Trader 90; completes lesson and quiz; progress persisted; failures prescribe remediation instead of unlocking a live-trading milestone.
3. User opens briefing; every market field has as-of timestamp, source, feed type, freshness and stale/unavailable display; never fabricated values.
4. User uploads XAUUSD screenshot and timeframe metadata; tutor distinguishes observed values vs inferred context vs missing evidence and refuses unsupported entry-quality assertions.
5. User creates a simulated plan, records outcome and saves tutor review; analysis evaluates process independently of P&L.
6. User toggles to Terminal and sees same journal/progress with advanced panels; mobile layout remains usable.
7. Events exported with pseudonymous IDs; consent and data deletion enforced.
8. Access control, API cost ceilings and rate limiting protect paid resources. No user-generated personal financial data in model training by default.

## Activation, retention and PMF instrumentation
Event contract (server authoritative timestamps; user_id pseudonymous; acquisition_source, cohort, experience_segment, product_mode and experiment_id attached where consented):
- landing_view, signup_started, signup_completed
- risk_disclosure_viewed, risk_acknowledged
- lesson_started, lesson_completed, quiz_submitted, competency_gate_passed
- briefing_opened, briefing_scenario_saved
- screenshot_uploaded, tutor_review_requested, tutor_review_completed, insufficient_evidence_returned
- simulated_plan_created, simulated_trade_journaled, weekly_reflection_completed
- paywall_viewed, checkout_started, subscription_started, subscription_canceled
- support_ticket_submitted, dissatisfaction_reported
No PII, order credentials or sensitive broker secrets in events.

Metric definitions:
- Qualified signup: adult prospect who selects XAUUSD learning interest and completes risk/expectation questions; exclude bots and duplicates.
- Activation D7: qualified signup who completes >=1 lesson AND >=1 briefing/chart-review activity within seven calendar days.
- W4 retention: among activated pilot users, >=1 meaningful learning/review event during days 22–28 (not login alone).
- Paid conversion D30: qualified pilot signups initiating paid subscription within 30 days / all qualified pilot signups with full 30-day observation.
- Rule adherence: required checklist fields correctly completed on simulated plans / eligible simulated plans; separate from returns.
- Very disappointed: respondents choosing “very disappointed” on standard PMF survey / valid responses; show response rate and segment counts.
- Track time-to-first-value, provider data failures, hallucination/unsupported assertions, cancellation reasons, gross margin per active subscriber and support burden.

Provisional pilot decision thresholds (NOT benchmarks or forecasts): 25–30 interviews; 10–15 design partners; 100 qualified signups; >=40% D7 activation; >=50% W4 activated retention; >=10% D30 paid conversion; >=40% “very disappointed” of surveyed active users. Monitor confidence intervals; require full cohort windows; revise thresholds in Notion after interviews. Never infer PMF from sales alone.

## Experiment design
- Test A: free session briefing CTA vs free first chart-review CTA; compare qualified signup-to-D7 activation, separately by beginner/intermediate.
- Test B: guided Beginner Mode vs unstructured Terminal; measure completed exercises and unsupported-action rates.
- Test C: paid monthly Terminal vs bundled Trading Lab; measure willingness-to-pay and observed subscription behavior; proposed USD $39/$79 are **unvalidated hypotheses**.
- Primary success: repeat evidence-based learning/review behavior with acceptable unit economics and low user harm. Do not optimize for trading frequency or leverage.

## Compliance, claims and evidence
- Never promise income in 60–90 days; use “90-day learning and simulated practice pathway.”
- Avoid earnings screenshots/testimonials that mislead; do not claim strategy efficacy absent out-of-sample verification including slippage, transaction costs and sample size.
- Risk warnings for leveraged FX/CFD trading; educational content only, jurisdiction-specific legal review before commercialization.
- On contradictory DXY/yield/news signals display conflicting evidence and *no trade* as a valid output.
- Market-maker intent must be presented as hypotheses, not observable facts. Tick-volume is not centrally cleared COMEX volume.
- Market-data provider licenses and display entitlements must be approved before public real-time feeds.

## Delivery phases / exit gates
Phase 0 (Discovery): interviews, landing page, value-prop tests, source inventory. Exit: clear JTBD & meaningful signup intent.
Phase 1 (Learning vertical slice): beginner onboarding, lesson, practice, tutor, journal and telemetry. Exit: complete instrumented user journey.
Phase 2 (Terminal intelligence): licensed feed connector, freshness, session briefing, context map. Exit: reliable source-backed, correctly timed market displays.
Phase 3 (Pilot): 60-day mixed-segment cohort, interviews, onboarding improvements, pricing tests. Exit: cohort analysis and quantified go/no-go.
Phase 4 (Scale): advanced journal, paid subscriptions, full academy only after pilot supports investment.

## Dependencies
Retain existing [PRD](PRD.md), [AI Tutor contract](AI-TUTOR-SPEC.md), [Entry rubric](ENTRY-QUALITY-RUBRIC.md), [Architecture](ARCHITECTURE.md) and [TradingView integration](TRADINGVIEW-INTEGRATION.md). PMF does not change the 100-point entry-quality score: it measures process **not win probability**.
