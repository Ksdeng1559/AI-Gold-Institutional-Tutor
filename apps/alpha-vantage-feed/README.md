# Alpha Vantage MCP reference feed

A runnable collector and local dashboard using the official [alphavantage/alpha_vantage_mcp](https://github.com/alphavantage/alpha_vantage_mcp) server. Gold, BTC, WTI, Brent and nominal US10Y observations are cached in SQLite. The browser updates from that cache without issuing provider requests itself.

## Start

Requirements: Python 3.10+ for this collector, `uv`/`uvx` on PATH, and network access. `uvx --python 3.13 marketdata-mcp-server` starts the official server, whose current source requires Python 3.13. The upstream package is installed by uvx on first use; package installation and real local-provider access have not been exercised in this workspace. Review/pin the published package version in your deployment environment. Upstream source reviewed: `3ed9b05db06d16476d326a12441d68ad071b261a` (18 October 2026).

Set `ALPHA_VANTAGE_API_KEY` privately in the collector process environment. The official server accepts that variable, so no key is put in command arguments, URLs, source code or browser assets. An existing ChatGPT OAuth connection is not exported into this process. Use your own Alpha Vantage key; MT5 and Marketaux credentials are different.

From this directory:

```bash
python feed.py --serve
```

Open **http://127.0.0.1:8090**. The collector runs on startup, then every six hours; the browser reads the cache every 15 seconds. Keep the process running for automatic collection. A single collection pass is `python feed.py`. The database defaults to `~/.gold-journal/alpha-vantage.sqlite3`; `--cache` overrides it. No financial statements, accounts, broker credentials or trades are read.

A deployment with verified higher request entitlements may use `--refresh-seconds 300 --daily-budget <verified-limit>`. These flags do not purchase or grant data access. Default limit: 12 attempted provider calls per UTC day in this local database. All attempts, including errors, count before dispatch. The counter persists across restarts and serializes concurrent reservations. Other clients/ChatGPT tasks share your provider quota but are outside this local counter. Use one collector process per cache and verify the provider's reset policy before raising limits.

## Data and behavior

| Key | MCP tool | Freshness policy |
| --- | --- | --- |
| gold | GOLD_SILVER_SPOT, GOLD | Refresh at collector cadence; preserve unspecified timezone |
| btc | CURRENCY_EXCHANGE_RATE, BTC/USD | Refresh at collector cadence; preserve provider timezone |
| wti | WTI, daily | Reuse successful retrieval for 24 hours; daily EIA/FRED series |
| brent | BRENT, daily | Reuse successful retrieval for 24 hours; daily EIA/FRED series |
| us10y | TREASURY_YIELD, daily, 10year | Reuse successful retrieval for 24 hours; nominal constant maturity rate |

The client initializes MCP, sends initialized notification, discovers tool names (including pagination), and calls only the five allowed read tools. Calls are sequential, at least 1.1 seconds apart. It accepts structured content, text JSON and the provider's small JSON preview. It validates instrument, unit, positive finite value and dates. Preview truncation does not trigger a full-history download. Provider error payloads, Information/Note and isError are checked; refusal stops the pass without retries. Previous values and their timestamps remain unchanged on failure. Startup failures and per-series outcomes appear in the cache/dashboard; raw responses and exception bodies are not logged.

GET `/api/market` returns `{market_data, attempts, last_attempt_at?, collector_status?}`. Each normalized observation follows [the integration contract](../../docs/ALPHA-VANTAGE-INTEGRATION.md). The local server binds only to 127.0.0.1 and exposes no mutation or order route. Missing observations remain blank. DXY, automatic pivots, daily open, daily/weekly VWAP and exact MAE/MFE are not inferred.

## Hosted dashboard relationship

The current private Site already receives Alpha Vantage snapshots through the authorized ChatGPT plugin and its existing pre-session tasks. This local collector is a separate runtime and does not automatically publish to that Site. Its `market_data` shape is compatible with the Site contract. A future production worker must read the existing news/briefing snapshot, merge market data through authenticated ingestion, and verify readback without advancing news/briefing cutoffs. Do not expose the local server publicly or hard-code Site service credentials to bridge it. Reuse the established Site scheduling path until a separately authenticated hosted collector is provisioned.

A live dashboard means periodically updated observations at a permitted cadence. MCP does not turn daily macro series into live quotes or bypass provider delays/entitlements. The free connection previously returned 25 requests/day and one-per-second pacing; confirm your actual plan. This source's MIT software license does not grant redistribution rights to all underlying data.

## Validation

```bash
python -m unittest discover -s tests -v
```

Five offline tests cover initialization/discovery and read restrictions using a fake stdio server; provider errors/previews/missing observations; instrument/value/date semantics; persistent request budgets; cache reuse and failure retention; and the real local HTTP route reading the same cache. Dashboard JavaScript syntax passes. No real API key is included. Actual local provider execution, browser visual QA and remote-hosted collection remain unverified.
