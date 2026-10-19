# Native MT5 MCP: journal demo

18 October 2026 · Proposed setup, not a connected feed

## Goal

Produce one private, read-only snapshot from the trader's demo account: account currency, open exposure, closed gold positions, net results, and a daily journal review. Confirm the actual account type before describing it as a demo account. No orders, stop changes, scripts, chart changes, or automated Discord/Notion publishing are included.

## Local connection

1. Regenerate the internal API key visible in the shared screenshot. Rotate the separately exposed marketdata key too. Never commit either key or paste the replacement into chat.
2. Keep MT5 running on the same computer as the local MCP client. Prefer an investor/read-only login where supported. Verify broker and account locally.
3. In MT5, Tools → Options → MCP, enable the internal server. The screenshot's address is `http://127.0.0.1:22346/mcp`. Click Copy for the official client configuration.
4. Configure only the terminal server for this demo in the local client's private settings. For local Codex, MetaQuotes documents the following project configuration. Replace the placeholder locally; keep the real `.codex/config.toml` untracked and outside shared artifacts. Merge with existing configuration rather than overwriting it.

```toml
[mcp_servers.terminal]
url = "http://127.0.0.1:22346/mcp"
enabled = true
http_headers = { "Authorization" = "Bearer <REGENERATED_LOCAL_KEY>" }
```

5. Restart the local client and inspect its available MCP tools. An instruction to read only is not a permission boundary: restrict enabled tools where the client supports it, and use broker read-only authorization where available.

This cloud workspace cannot reach the user's `127.0.0.1`. Configuring a local client does not automatically connect this chat or the hosted dashboard. Do not expose the terminal port to the internet. The remote marketdata endpoint is for market information/news, not this broker journal.

## Read-only discovery and capture

Officially documented candidates are listed below. Inspect installed tool schemas first: availability and arguments can differ by terminal version. Do not guess arguments or substitute a mutating tool when a read is unavailable.

| Candidate tool | Demo evidence |
|---|---|
| get_trading_account_info | Account type, currency, balance/equity; redact identifying details from shared output |
| get_time_information | Source time conventions and UTC conversion |
| get_marketwatch_symbols | Exact broker gold symbol, including suffix |
| get_trading_open_positions | Current positions and pending orders, kept outside closed-trade statistics |
| get_trading_history_orders | Bounded order/deal history, entry/exit classification, costs and fills |
| get_trading_history_positions | Position reconstruction, reconciled against underlying deals |
| get_chart_ticks_history | Optional matched bid/ask path, only when needed and available |

Use a user-visible seven-day date range rendered in America/Vancouver and translated to UTC after confirming source conventions. Capture returned source timestamps, retrieval time, coverage, pagination and errors. Do not declare the snapshot complete until all pages and relevant deal types are covered. Export only to private local files; do not commit financial records to this public repository.

## Prompt for the connected local client

> Prepare a read-only Gold Trading Journal demo using the connected terminal MCP. First list the available account, open-position, history and time tools with their schemas. Do not place, modify, cancel or close orders; run scripts, shell commands or EAs; change charts; or send anything to Discord or Notion. Verify account type, currency, exact gold symbol and source time conventions. Retrieve the last seven calendar days of available gold deals and reconstructed positions, with pagination and coverage recorded. Keep open exposure separate. Reconcile partial closes, reversals, commissions, swaps and fees before counting completed positions. Present net P/L, win rate, profit factor, expectancy and the included sample count, using docs/METRICS-SPEC.md. Mark ambiguous records for review. Leave MAE/MFE unavailable unless a sufficient matched holding-period price path exists. Show a daily review with evidence-linked observations and one proposed process experiment. Redact account identifiers and never reveal keys. Stop and report missing read capabilities rather than substituting other tools.

## Demo output and acceptance

The local result should show connection state, verified demo/real/unknown account type, source currency, exact instrument, source timestamps, included date range, completed/open/unresolved counts, and reconciliation status. The journal table should preserve broker record identity privately and show direction, quantity, entry/exit time, gross/net basis, costs, net P/L and review state. Follow the existing metrics contract for denominators and exceptional cases.

Success means one genuine account snapshot reconciles to the same-period broker history, repeated capture does not duplicate completed trades, and unsupported metrics remain explicitly unavailable. No real account has been accessed by this document. No persistent sync, ingestion service or tutor trigger has been activated. For a cloud-only demonstration, a redacted broker CSV export is the immediate alternative; label it as an uploaded snapshot rather than a live connection.

## Official references

- https://www.metatrader5.com/en/terminal/help/mcp_and_ai/configuration
- https://www.metatrader5.com/en/terminal/help/mcp_and_ai/capabilities
- https://www.metatrader5.com/en/terminal/help/startworking/authorization
