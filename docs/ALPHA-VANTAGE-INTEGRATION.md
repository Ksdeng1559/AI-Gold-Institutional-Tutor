# Alpha Vantage integration

Status: tested connector and deployed shared reference snapshots · 18 October 2026

## Scope

Use the user-authorized Alpha Vantage MCP plugin to retrieve reference data and publish normalized observations into the existing private Gold Fundamentals Desk R2 news/briefing snapshot. The website reads its own API. It contains no provider credentials. The connected assistant and saved pre-session tasks own retrieval; there is no direct streaming provider subscription in the browser. The Site has a separate source repository from this PR.

| Snapshot key | Provider function | Meaning | Critical limit |
| --- | --- | --- | --- |
| gold | GOLD_SILVER_SPOT, GOLD | XAUUSD gold reference, USD/troy oz | Returned timestamp timezone unspecified; not broker bid/ask |
| btc | CURRENCY_EXCHANGE_RATE, BTC/USD | USD/BTC reference | Returned UTC; individual venue unspecified |
| wti | WTI, daily | USD/barrel daily EIA/FRED observation | Published with lag; not futures execution quote |
| brent | BRENT, daily | USD/barrel daily EIA/FRED observation | Published with lag; not futures execution quote |
| us10y | TREASURY_YIELD, daily, 10year | Nominal constant maturity rate, percent | Not real yield or live bond quote |

## Persistence and display contract

Optional root market_data keys contain provider=Alpha Vantage, positive finite numeric value, instrument, unit, function, observed_at (raw timestamp/date), timezone, ISO retrieved_at, kind (reference quote or daily observation), and note. Source timestamps must not acquire an invented timezone. Server rejects malformed records and older retrieval writes, and merges omitted keys from previous storage. Keep news.updated_at and saved briefing preparation/cutoff timestamps unchanged when only market references refresh. Previous observations retain their own dates during failures. Do not embed fetched values as a perpetual fallback in static source.

Cards display units, observation date, timezone, retrieval and source limitations. They flag retrievals older than 12 hours while daily series retain their actual reporting dates. The saved briefing shows the latest references separately from its own evidence cutoff. No changes, correlations or session levels can be inferred merely because both instruments have a value.

## Refresh and quota

Existing Asia, London and New York pre-session tasks preserve their schedules. Fetch gold and BTC once per run. Fetch each daily macro series only if its retrieval is older than 24 hours. Execute provider calls sequentially, at least one second apart, at most five calls per run. The tested free connection returned 25 requests/day and a one-per-second pacing error. Other connector use shares that quota. No automatic retries on rate limits. Inspect structuredContent.error and provider Information/Note payloads even if isError=false. Parse the small latest-row sample_data preview; avoid downloading full historical responses.

## Verification and remaining work

Five source observations were published and read back without replacing the eight existing news stories or three briefings. Worker tests cover metadata/numeric validation, persistence, merge retention, stale-write rejection and asset routing. Build and script syntax checks pass. Deployment succeeded; browser visual QA remains unavailable. The updated tasks were saved and enabled, but no scheduled run has yet been observed.

DXY, broker MT5 quotes, automatic pivots, daily open and daily/weekly VWAP remain unavailable until separate eligible data and calculation conventions are verified. Historical gold close prices alone do not establish session OHLCV or exact MAE/MFE. Alpha Vantage news sentiment is an optional future evaluation and does not replace the current source-linked news.

## Official reference

[Alpha Vantage API documentation](https://www.alphavantage.co/documentation/). Entitlements and permitted display must be checked for each future endpoint. Endpoint availability does not imply every indicator or data feed is free.
