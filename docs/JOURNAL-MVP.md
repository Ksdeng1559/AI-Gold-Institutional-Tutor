# Decision Journal MVP

## Run locally

Requires Node.js 20+; no external packages or credentials required.

```bash
npm start
```

Open http://127.0.0.1:3000. Run `npm test` for the core decision/scoring tests.

## Implemented

- Responsive overview, journal, planning form and five educational lessons.
- Exact symbol/feed and timestamp capture; session, trade type, archetype and multi-timeframe context.
- Seven evidence-backed rubric components, 100-point total, repository grade bands and A+ hard gates.
- Unknown evidence prevents final submission. Zero requires an absence explanation.
- Long/short price geometry and planned-risk validation; observation decisions supported.
- Browser draft storage and locked submitted entry review.
- Separate one-time post-trade reflection with diagnosis, plan adherence, realized R and corrective action.
- Decision count, mean entry quality, component averages and descriptive realized expectancy.
- Versioned JSON export/restore with score validation and replacement confirmation.
- Invalid existing storage is preserved rather than silently overwritten.

## Data and product boundaries

This is a single-user, local-first functional MVP using browser localStorage, not the planned production Next.js stack. Data belongs to the browser origin and is not synced. Export before changing ports, browsers or devices. The lightweight local Node server serves static assets only; it binds to loopback by default.

Entry immutability is enforced by the UI and domain functions, not a tamper-proof database. JSON backups are user-controlled; import validation detects inconsistent scores but does not establish evidence authenticity. Reflection is locked after submission in this MVP. Screenshots are referenced by filename/private URL, not uploaded or analyzed. Evidence quality and hard gates are self-assessed; no AI verification is claimed. Lessons are initial implementation references; Notion remains the living curriculum source.

No live TradingView connection, AI model, trading execution, screenshot storage, authentication, multi-user database or production deployment is implemented. Never place secrets or OAuth tokens in journal fields.

## Validation

Seven Node tests cover hard gates, unknown evidence, score bounds, reflection isolation, risk geometry, backup validation and missing-outcome analytics. JavaScript syntax checks and HTTP asset checks were run. Browser end-to-end verification was attempted but blocked because the environment has no Chromium executable; responsive layout and full interaction still require browser verification before release.

## Next implementation milestones

1. Run browser acceptance: draft → reload → submit → reflection → reload → dashboard; test malformed backup, storage failure and narrow viewport.
2. Add immutable server-side entry snapshots with authenticated per-user access and consent-based evidence uploads.
3. Introduce an evidence adapter using the TradingView integration contract, retaining manual review as fallback.
4. Add model-assisted teaching suggestions only after structured evidence validation; label inference and retain source references.
5. Add longitudinal score-band and behaviour analysis with sample sizes; do not imply predictive edge from small samples.
6. Reconcile current Notion product intent before production stack implementation.
