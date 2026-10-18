# OpenBB research integration

Proposal v1 · 18 October 2026 · [Terminal PRD v2.4](PRD.md)

## Product role

OpenBB's Open Data Platform (ODP) is the planned research integration layer for the Gold Research Terminal. Keep the existing web dashboard and journal. Use OpenBB to access, organize and normalize supported research providers; do not treat it as a universal data entitlement, a substitute for account history, or a requirement to adopt OpenBB Workspace.

| Component | Responsibility | Current state |
|---|---|---|
| Existing dashboard | Research presentation, original-source links and Session Briefings | Private hosted implementation; browser QA unverified |
| OpenBB ODP | Provider integration for macro, rates, positioning and eligible market datasets | Planned; not installed or connected |
| MT5 | Broker-specific account state, positions and execution/history reads | Local application implemented; actual broker connection unverified |
| Journal analytics | Reviewed trade grain, net metrics, evidence and daily reviews | Local runnable slice; automatic reconciliation remains future work |
| News sources | Publisher reporting and official releases, with original attribution | Initial editorial snapshot saved; not supplied by OpenBB |
| Marketaux | Optional financial-news adapter | Request returned HTTP 403; cause and account access unverified |
| Eulerpool | Optional broader financial-data provider | No authenticated connection; free-tier access and instruments unverified |
| Discord / Notion tutor | Authorized educational review of frozen journal/research evidence | Proposed integration; not active |

## First datasets and access gates

Prioritize official macroeconomic/rates series and gold CFTC positioning. Discover the actual OpenBB V5 providers and commands before selecting interfaces. FRED, Federal Reserve, BLS and CFTC are candidates, not guaranteed keyless adapters. Verify original-source access, required keys and usage rights independently.

Later candidates are economic-calendar events, exact gold/DXY/oil/BTC references and historical bars. Confirm instrument identity, venue, units, delay, retention and entitlement before populating the dashboard. Do not substitute a gold ETF for spot gold, a dollar proxy for DXY, or front-month futures for the trader's broker symbol without explicit labels and a separately approved use case.

OpenBB does not resolve Eulerpool registration or grant access to a paid dataset. A connected assistant's MCP does not automatically authorize a website or unattended job. Provider API keys are not interchangeable. Optional Eulerpool evaluation must use its actual published authentication method and verified account access; no connector should be described as working based solely on documentation.

## Service boundary and deployment

Run a minimal, version-pinned OpenBB Python environment on a compatible backend host. Inspect V5 documentation and installed schemas; validate migrations before using older V4 examples. The current dashboard's Sites Worker cannot execute OpenBB's Python packages directly. Do not add OpenBB to the browser bundle.

Expose an authenticated, bounded research API to the dashboard and scheduled workers. Optionally expose an allowlisted research MCP to the tutor. Keep trading/account credentials, broker write operations and raw personal journal records outside the research service. OpenBB Workspace may be another client of this same service later; it is not the MVP frontend.

Install only the selected provider packages. Validate costs and hosting before provisioning. Keep secrets in the host's secret settings, never source code, browser storage, Notion or logs. Separate commercial redistribution rights from API authentication.

## Normalized evidence

Every observation stores original provider, dataset/series ID, exact instrument/contract and venue where applicable, value/unit/currency, source observation time or measured period, publication time when supplied, retrieval time, delay/freshness state, revision/vintage and transformation version. Preserve null/unavailable values. Corrections create new versions rather than rewriting evidence attached to a completed review.

Cache by provider, dataset, parameters and entitlement. Use bounded requests, timeouts, quota counters and backoff. Browser filters reuse cached records. Partial failures preserve last-success timestamps and disclose stale/missing coverage. Never switch providers silently: differing definitions, revisions or broker prices may change the meaning of a value.

VWAP requires eligible volume and complete anchor coverage. Daily open/pivots require exact session conventions. MAE/MFE needs a matched holding-period price path and inventory. An OpenBB installation alone validates none of these calculations.

## Session Briefing and tutor use

Reuse the three existing pre-session jobs. Timing follows Dennis's ICT framework: 19:45 Sunday–Thursday before Asia's 20:00 window, 01:45 Monday–Friday before London's 02:00 window, and 06:45 Monday–Friday before New York's 07:00 window, all America/New_York. Display Vancouver times through IANA conversion. These are methodology windows, not exchange opening times.

Each briefing freezes source observations, news/report links, verified upcoming catalysts, source cutoff, preparation time, intended session/date and coverage gaps. Present facts, observed market response, interpretation and conditional questions separately. Prior-session direction and NY archetype remain unknown without actual chart/intermarket evidence. Source research may continue while OpenBB is unavailable; label the source method accurately.

Research updates do not initiate broker actions or automatically request a tutor review. The explicit Notion Ready for AI Review contract remains separate. A tutor receives only an owner-authorized, frozen evidence bundle and cannot alter deterministic financial results.

## Acceptance criteria

| ID | Passing evidence |
|---|---|
| OBB01 | Tested version-pinned environment; installed commands/providers discovered; source access and keys validated without exposure |
| OBB02 | At least one macro/rates series and one gold-positioning dataset reconcile to original source periods, units and revisions |
| OBB03 | Original provider and exact series/instrument, publication/observation/retrieval times, delays and missingness survive API and UI presentation |
| OBB04 | Cache/quota tests prevent per-filter upstream calls; outages retain last successful data without false freshness |
| OBB05 | Quotes, proxies, futures contracts and broker observations remain distinct; insufficient volume/path coverage suppresses VWAP/excursions |
| OBB06 | Unauthorized reads/jobs fail; keys and journal records are not exposed; research endpoints cannot invoke broker writes |
| OBB07 | One actual pre-session run writes/readbacks the correct session/date and frozen evidence, preserves other sessions and handles source failure |
| OBB08 | Optional Workspace/MCP reuses the research service; frontend usability and end-to-end owner isolation pass before release |

Documentation updates do not satisfy these gates. Keep unresolved checks visible in the implementation plan.

## Official references

Checked 18 October 2026:

- https://docs.openbb.co/odp
- https://docs.openbb.co/odp/python
- https://docs.openbb.co/odp/python/quickstart
- https://docs.openbb.co/odp/python/reference
- https://docs.openbb.co/odp/python/quickstart/workspace
- https://eulerpool.com/developers/mcp-server
- https://eulerpool.com/developers/authentication
