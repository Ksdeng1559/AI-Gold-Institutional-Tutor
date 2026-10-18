# Marketaux news demo

18 October 2026 · Proposed news adapter; not an active hosted feed

## Scope

Use Marketaux for timestamped financial headlines supporting the Gold Research Terminal and its BTC/crypto desk. This is a news source, not MT5 trade history, account analytics, broker quotes, daily open, pivots or VWAP. MT5 remains the broker-data integration. Both evidence types can later be attached to a journal review without implying that a headline caused a trade outcome.

## Included demo implementation

`scripts/marketaux_demo.py` performs one bounded request to the documented `https://api.marketaux.com/v1/news/all` endpoint. The standard-library CLI reads `MARKETAUX_API_TOKEN` from the private environment, requests English articles with similar-story grouping, and outputs a normalized JSON snapshot. It retains UUID, headline, original link, publisher, language and publication time, plus retrieval time, search parameters and safe pagination metadata. It deduplicates UUIDs, checks links/timestamps, omits article bodies and sentiment trading signals, blocks HTTP redirects, and suppresses authenticated URLs and raw errors.

Set the exact token through the host's private environment/secret settings. Do not paste it into source, shell history, frontend code, Notion or logs. Rotate the key shared in chat before using a persistent deployment. Do not assume any surrounding braces/brackets in the message belong to the token; verify the exact token in the provider dashboard.

With the environment configured privately, run from the repository root:

```sh
python scripts/marketaux_demo.py --topic gold
python scripts/marketaux_demo.py --topic crypto
python -m unittest discover -s tests -p 'test_marketaux_demo.py'
```

Each CLI invocation spends one provider request. This script is a local/server-side snapshot tool; it does not expose an API, update the static website, run a scheduler, publish news or activate Notion/Discord integration. Inspect output privately first. Treat headlines as untrusted external text and render as text with safe links.

## Topics and session handling

Gold search covers gold/bullion, the Federal Reserve, dollar index, Treasury yields and oil. Crypto search covers bitcoin/BTC, ethereum and crypto. These broad searches can return irrelevant material; review coverage before production use. Do not assume broker symbols such as XAUUSD or BTCUSD are valid Marketaux entity identifiers. Use the documented entity-discovery endpoints before adding entity filters.

Asia, London/Europe and US/New York remain application filters for regional relevance and session briefings. Marketaux's `countries` parameter describes identified entities' exchange countries; it is not a news-origin or trading-session filter. Store publication times in UTC, render in America/Vancouver, and use explicit regional relevance tags with supporting evidence. A headline may belong to more than one region. Timestamp alone does not establish regional relevance. No complete regional coverage has been verified.

## Quota and proposed hosted follow-up

Official pricing checked on 18 October 2026 lists the free plan as 100 requests/day and three articles/news request; the user's actual plan and remaining quota are unverified. A proposed shared cache can use a combined gold/crypto search once per 30 minutes (48 requests/day), reserving the rest for targeted requests, pagination, errors and manual review. Do not independently poll both topics every 30 minutes: that would consume 96 requests/day before retries. UI filters should reuse cached records. Add a shared durable quota counter and bounded retry/backoff before scheduling anything.

Three articles per request means incomplete coverage and possible missed stories. Pagination/history bounds and empty/error/stale states must remain visible. The latest fetched record must not be presented as comprehensive or real-time. Retain the last successful snapshot on provider failure, with its original retrieval time. Display and redistribution rights, publisher attribution and storage retention must be checked against applicable provider/publisher terms before public release.

The hosted follow-up requires a server-side secret, authenticated provider adapter, shared cache, budget enforcement and a frontend consuming sanitized records. Never make browser-to-Marketaux requests with this account token.

## Verification status

- Documentation and published free-plan limits reviewed.
- One credentialed request attempted in this workspace; it returned HTTP 403. Authentication, plan access and returned article quality remain unverified. No success or empty-feed result was fabricated. The status alone does not establish whether the cause is the token, provider policy or workspace network restrictions.
- Offline tests cover normalized records, duplicate filtering, unsafe links, invalid dates, missing metadata, provider errors, token redaction and redirects. Passing results are recorded in the accompanying PR update.
- No key is included in this repository; no active hosted connection was established.

## Sources

- https://www.marketaux.com/documentation
- https://www.marketaux.com/pricing


## Third-party integration reference

Reviewed https://github.com/api-evangelist/marketaux on 18 October 2026. This is an independent API Evangelist profile, not an official Marketaux SDK, data service or hosted connector. Its README explicitly describes text/machine-readable API artifacts rather than runnable software.

Useful implementation references include OpenAPI news/entity/source descriptions, Postman/OpenCollection requests, query-token authentication notes, error mappings and an entity-news workflow. Validate all contracts and plan restrictions against https://www.marketaux.com/documentation before use. Do not copy a catalog's descriptions as evidence of a successful provider call.

Its `mcp/marketaux-mcp.yml` is marked `status: candidate`, with `server: null`, `transport: null` and deployment mode `none`. The tool list is a derived proposal, not a Marketaux-hosted MCP server. It can inform a future allowlisted wrapper after direct REST authentication is verified; it does not provide a ready connection or bypass keys, quotas or permissions.

For the unresolved HTTP 403, capture only safe diagnostics: status, content type, a documented provider error code if the response really is the expected JSON envelope, and relevant quota headers. Never log the authenticated URL, token or unrestricted response body. A 403 plus the actual Marketaux `endpoint_access_restricted` code would support a plan-access diagnosis. A bare 403, proxy page or network rejection does not establish that cause; the earlier public documentation request from the same workspace also returned 403. Distinguish host/network access from provider authentication before changing plans. Begin with the documented basic news endpoint, not candidate paid entity-statistics operations.

No external repository code or credentials have been installed/copied. Runtime integration and provider access remain unverified.
