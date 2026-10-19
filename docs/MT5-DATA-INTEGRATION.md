# MetaTrader 5 Read Only Data Integration

Proposal v1.1 · 18 October 2026 · [Terminal MVP](PRD.md)

## 1 Purpose and scope

Add MT5 as a broker-connected data source for the web terminal and journal. Retrieve account state, open positions, orders, execution history, symbol metadata, prices, bars, and available historical ticks. This can reduce statement uploads and improve the price-path evidence used for MAE/MFE. CSV/PDF uploads remain fallback and reconciliation evidence.

This integration is read-only. It does not place, modify, cancel, close, or copy trades; change stops; enable trading agents; or give the Discord Tutor trading permissions. Live trading data means data about the broker account and markets, not automated live trading.

## 2 Recommended deployment

For the first journal demo, use MT5's native terminal MCP from a client running on the same PC as MT5. Follow [Native MCP journal demo](MT5-MCP-DEMO.md). This avoids requiring a Python collector for the first account/history snapshot. Native MCP does not by itself implement hosted ingestion, deduplication, Notion synchronization, or a continuous journal feed. Verify the actual exposed tools and restrict access to data reads; the server also exposes trade operations.

The terminal endpoint (normally `http://127.0.0.1:22346/mcp`) supplies broker account data. The separate `https://www.metatrader.com/mcp` endpoint supplies external market data/news and is not a substitute for terminal account history. A cloud chat cannot reach the user's loopback address. Keep the terminal local rather than exposing its port publicly.

For ongoing application ingestion, the Python collector below remains an implementation option; a native-MCP adapter can implement the same normalized ingestion contract after capability and permission validation.

Use a small collector on the user's Windows PC or a dedicated Windows VPS running an authorized MT5 terminal. The official MetaTrader5 Python package communicates with a terminal; it is not a general browser or independent public REST service. Choose a currently supported compatible Python/package combination and verify it on the actual host. Current package artifacts include Windows x86-64 wheels.

The collector sends normalized batches to the application's authenticated ingestion API over outbound HTTPS. Do not expose the terminal, debugging ports, login credentials, or a remote trading endpoint to the public internet. The web terminal and Discord bot consume the normalized backend, never the MT5 session directly.

Preferred flow:

Broker MT5 terminal → local read-only collector → private normalized ingestion → journal and analytics → explicit Notion review request → shared tutor → private Discord completion

The local host must remain running and connected for fresh data. A Windows VPS is an availability option, not a provisioned service or cost-free promise. A hosted web app cannot import the terminal package and assume it has access to the user's desktop. Mobile MT5 alone is not the collector host. An MQL5 data-export EA or managed connector is an alternative to evaluate separately, with the same read-only boundary and licensing checks.

## 3 Access and capability validation

Prefer a dedicated terminal authenticated with the broker's investor/read-only access where supported. Official MT5 help describes investor access as allowing account viewing and price analysis without trading. Confirm required history/quote functions actually work for the target broker/account. Store credentials only on the collector host using OS-protected secret facilities, not in GitHub, Notion, Discord, browser storage, or chat.

A package wrapper is not a broker permission boundary: the full library also exposes trading functions. The collector must allowlist only necessary data functions and omit all trade-request routes. Investor authorization and isolated deployment provide stronger protection than a UI toggle. Account switching must stop ingestion until the account/server mapping is reverified; never associate another account's data with a prior user's records.

Initial setup verifies terminal/package version, intended broker server/account, account currency and mode, supported symbols, permissions, quote age, history coverage, and disconnect/reconnect behaviour. The broker determines instrument coverage, retention, market-data rights, trading hours, and any fees. An MT5 account does not guarantee DXY, centralized GC volume, or external news coverage.

## 4 Data mapping

| Data need | Official Python interfaces to evaluate | Journal use |
|---|---|---|
| Health and identity | initialize, terminal_info, account_info, shutdown | Collector/account health and currency |
| Symbol definitions | symbols_get, symbol_info | Exact broker symbol, digits, tick/contract properties |
| Latest quote | symbol_info_tick | Broker bid/ask/last with observation time |
| Open state | positions_get, orders_get | Separate open exposure from closed results |
| Execution records | history_deals_get, history_orders_get | Fills, partial closes, costs, order/position relations |
| Bars | copy_rates_range and related bar functions | Completed candles and eligible reference calculations |
| Historical ticks | copy_ticks_range | Matched intratrade path where available |

Use the actual installed package's signatures and returned fields. A symbol suffix such as a broker-specific gold name must be resolved, not discarded. Preserve original account/server identity under private access, instrument/contract, position/deal/order identity, entry/exit classification, quantity, costs, currency, raw times, and normalized UTC instants.

An order, deal, position, and journal idea are different entities. Handle hedging and netting accounts, reversals, partial closes, standalone charges, cash flows, and corrections explicitly. Do not count opening deals, balance events, or every zero-profit row as a completed trade. Group thesis-level ideas only when confirmed by the trader or a separately validated rule.

## 5 Synchronization and quality

Proposed starting cadence, subject to broker/host tests: quote sampling every 1–5 seconds, open-state sampling every 5–10 seconds, history reconciliation every 30–60 seconds, and bounded historical backfill on initial connection/recovery. These are targets, not verified latency guarantees or a promise of a streaming tick service.

Use durable cursors with overlapping history windows, broker execution identity, and idempotent upserts. Commit cursors only after the server acknowledges durable ingestion. Retry with backoff; reconcile after disconnection before declaring history current. Pause on account/server mismatch. Record terminal health, last successful sync, latest source timestamp, gaps, and measured ingestion latency.

Do not treat a current poll time as the quote time. No new ticks while a market is closed is different from a failed collector. Open P/L is unrealized and does not enter closed-trade win rate. Equity snapshots can support sampled equity drawdown but cannot establish an unobserved intratick maximum drawdown. Record sampling interval and gaps.

MT5 Python documentation specifies UTC-aware requests and UTC tick/bar times. Preserve broker statement display-time conventions separately and test reconciliation; do not add a server offset twice. Retain millisecond time where returned, and render local times with date-aware America/Vancouver conversion.

## 6 MAE MFE and reference eligibility

Use broker-matched historical bid/ask data covering the verified holding interval. Preserve side, contract multiplier, quantity, currency conversion, and spread/cost convention. The [metrics contract](METRICS-SPEC.md) still governs. Missing tick history, partial coverage, bar-boundary uncertainty, and scaled positions can prevent exact excursion measurement even when the account is connected.

Store eligible per-position price paths and time-varying inventory where needed. Do not sum execution MAEs/MFEs into an idea total. Broker final net profit remains authoritative; modeled path P/L is separate and must not replace it. Historical stop changes and planned risk may still require journal entries or captured event evidence; current position state is not a complete past-management timeline.

Gold daily/weekly VWAP requires classified volume. Broker tick volume may support a labeled tick-volume-weighted estimate; it is not centralized futures traded volume. Real-volume availability must be tested. Keep GC and XAUUSD references separate, and preserve full-week coverage and anchor conventions. An MT5 connection does not automatically validate every VWAP or order-flow measure.

## 7 Application and tutor boundaries

The Data connections screen gains MT5 account/collector health, exact broker feed, sync times, coverage, and revoke controls. Imports and analytics shows source MT5 versus uploaded statement and detects overlaps across both. The private journal automatically receives candidate execution updates, with confirmation/reconciliation state shown; AI cannot auto-confirm ambiguous financial rows.

A newly closed trade or refreshed quote does not automatically call the tutor. The Notion Ready for AI Review workflow remains the explicit analysis trigger. Its evidence bundle can reference verified MT5-derived metric runs and price paths. This avoids repeated reviews on every tick and preserves consent and source-version control. Optional automatic end-of-day requests would require a later explicit product setting.

## 8 Security and failure handling

Use an enrollment flow bound to the authenticated owner and a revocable collector credential restricted to ingestion. Authorize every server-side account mapping; do not trust an arbitrary account ID supplied by the collector. Batch replay resistance and execution uniqueness are mandatory. Encrypt transport and private records, redact sensitive logs, and keep tokens off public dashboards.

No arbitrary command execution or MT5 function names are accepted over the collector API. Revocation blocks new ingestion without affecting broker protective orders or account trading. Collector failure must show stale/unavailable data while existing journal records remain usable. Never close or modify trades as a connection-recovery action.

## 9 Acceptance criteria

| ID | Passing condition |
|---|---|
| MT501 | Intended investor/read-only account and required data reads verified on actual supported host |
| MT502 | No order-send/modify/cancel/close interface exists in collector or application routes |
| MT503 | Exact broker symbols, account currency, source times, and connection health appear correctly |
| MT504 | Identical, overlapping, corrected, and replayed deal batches do not duplicate financial results |
| MT505 | Partial closes, reversals, account mode, fees, and cash flows reconcile to a broker statement |
| MT506 | Disconnect/restart recovers history gaps before declaring sync current |
| MT507 | Account switch or revoked collector token prevents incorrectly mapped ingestion |
| MT508 | Matched bid/ask path yields method-qualified excursions; missing history stays unavailable |
| MT509 | Sampled equity drawdown and tick-volume VWAP estimates are clearly distinguished from exact measures |
| MT510 | New MT5 observations do not trigger repeated tutor jobs; explicit Notion request uses a frozen evidence snapshot |

## Sources and implementation gates

Official references checked on 18 October 2026:
- https://www.metatrader5.com/en/terminal/help/mcp_and_ai/configuration
- https://www.metatrader5.com/en/terminal/help/mcp_and_ai/capabilities
- https://www.mql5.com/en/docs/python_metatrader5
- https://www.mql5.com/en/docs/python_metatrader5/mt5historydealsget_py
- https://www.mql5.com/en/docs/python_metatrader5/mt5copyticksrange_py
- https://www.metatrader5.com/en/terminal/help/startworking/authorization
- https://pypi.org/project/metatrader5/

Exact host, broker, account mode, investor access, history retention, symbol coverage, and data rights remain unverified. No terminal was accessed, no credentials collected, and no live connection or order capability was deployed by this proposal.
