# TradingView integration and operational learnings

Recorded: 2026-10-17 (America/Vancouver). Status: documentation only; no application adapter implemented.

## Scope and source of truth

This file versions the connection procedure, evidence requirements and acceptance checks for developers using Claude Code or Codex. Evolving trading methodology remains in Notion. Apply the existing [AI Tutor contract](AI-TUTOR-SPEC.md) and [architecture](ARCHITECTURE.md); this integration does not replace their timeframe hierarchy or scoring rules.

## What happened in this session

- The user attempted the official TradingView MCP connection through ChatGPT using a different TradingView account.
- The user reported "Something went wrong setting up the connection."
- A screenshot showed TradingView's authorization page requesting mcp:read and mcp:tools permissions with an Allow button.
- The user reported that authorization would not complete and confirmed a paid account. The exact plan, failed redirect, token exchange and server-side cause were not verified.
- No successful authenticated market-data read occurred in this chat.
- The user chose Claude and then reported starting installation of tradesdontlie/tradingview-mcp. Installation completion and a successful health check remain unverified.

Do not describe the account email difference as the proven cause. A visible consent page is not proof of a completed connection. A paid account alone does not establish a qualifying plan or exchange real-time entitlement.

## Option A: official hosted MCP

Reference: https://www.tradingview.com/mcp/docs
Server: https://mcp.tradingview.com/mcp
Transport: Streamable HTTP; authentication: OAuth 2.1.

TradingView's documentation checked on 2026-10-17 states Essential and higher paid plans qualify; trials do not. Recheck current documentation before setup.

Claude web/desktop:
1. Settings → Connectors → Add custom connector.
2. Add the server URL.
3. Sign into the intended TradingView account and authorize access.
4. Verify through a harmless symbol search and then an explicitly requested data read.

Claude Code:
```bash
claude mcp add --transport http mcp-tradingview https://mcp.tradingview.com/mcp
```
Run /mcp to complete authentication, then inspect discovered tools.

If authentication fails, record the stage (before consent, Allow click, redirect or final connection setup), sanitized error and timestamp. Start a fresh authorization flow rather than reusing an old consent tab. Trying the entire flow in one browser is a diagnostic experiment, not a proven fix. Never store OAuth callback query strings, authorization codes, cookies, passwords or tokens in GitHub.

## Option B: community local Desktop bridge

Repository reviewed: https://github.com/tradesdontlie/tradingview-mcp
README checked on 2026-10-17. Community project, not an official TradingView integration.

This bridge connects Claude Code to a locally running TradingView Desktop instance over Chrome DevTools Protocol (CDP). It uses the Desktop session rather than the hosted MCP OAuth flow. It still requires an installed, signed-in TradingView application and applicable subscriptions/data access.

Documented prerequisites: Node.js 18+, TradingView Desktop, Claude Code with MCP support; Windows/macOS/Linux support.

Installation outline:
1. Review the current repository README, security notes, license and dependencies.
2. Clone the repository and run npm install.
3. Launch TradingView Desktop with its documented local debugging configuration.
4. Register the absolute path to src/server.js as a local stdio MCP server using the client's supported configuration.
5. Restart/reload MCP discovery as needed and run the health check before analysis.

Example local MCP configuration (replace the path):
```json
{
  "mcpServers": {
    "tradingview-local": {
      "command": "node",
      "args": ["C:/absolute/path/tradingview-mcp/src/server.js"]
    }
  }
}
```

The README documents debugging port 9222. Keep the debugging endpoint local; do not expose it to the internet. Its undocumented internal interfaces can break after TradingView updates. The repository flags potential TradingView terms and market-data licensing conflicts; review suitability before automated data collection or commercial integration. Its code license does not grant market-data redistribution rights.

## Read-only acceptance checklist

Installation is accepted only after observing all relevant results:
- [ ] tv_health_check succeeds (community bridge).
- [ ] Exact chart symbol, venue/feed and timeframe are returned.
- [ ] Latest bar timestamp and retrieval time are recorded.
- [ ] Visible indicator names and accessible values are returned.
- [ ] Raw bars or a screenshot match the same chart/feed and timestamp context.
- [ ] Missing indicators, unavailable fields and unknown freshness are explicitly reported.

Tool names above come from the community README; use the installed server's actual discovered schemas. For the official MCP, use search_symbols as the initial read check. Do not use get_active_watchlist as a harmless test: its documented behavior may activate or create a watchlist.

Connection validation does not authorize changes to charts, scripts, alerts, watchlists or orders.

### First verification prompt

> Verify the installed TradingView MCP connection using its available health/read tools. Keep this check read-only. Report the exact symbol/feed, timeframe, latest bar timestamp, retrieval time, visible indicators and unavailable fields. Do not claim real-time entitlement from historical bars alone.

## Analysis evidence contract

- Preserve symbol and venue throughout a review. Never silently substitute GC futures for XAUUSD spot/CFD or transfer levels across feeds.
- Use UTC internally and America/Vancouver for display, with date-aware daylight saving conversion.
- Preserve the existing tutor hierarchy: H4 regime, H1 location, M30 POI/auction context, M15 permission, M5/M2 confirmation and M1 precision execution. Fetch only supported, needed intervals; unavailable M2 is unknown, not a fabricated interval.
- Use closed bars for confirmed setups; label forming candles separately.
- Separate source observations, reproducible calculations and interpretation.
- Read TDI, VWAP bands and volume-profile values only when actually exposed or visible. Record indicator settings and session boundaries where available.
- Do not invent HVN/LVN, POC, VAH/VAL, anchored VWAP, standard-deviation bands or order-flow delta. OHLCV price-change proxies are not trade delta/CVD; OHLCV profile estimates are not tick-level order flow.
- Unknown evidence remains unknown. Do not award confluence points for missing evidence.
- Treat the existing 4304/4277 case study in the tutor spec as a historical teaching example, never current market levels.
- Present bullish, bearish and neutral conditions with evidence-supported invalidation. Entry-quality scores are not win probabilities.
- No trade execution is authorized by installing or testing this integration.

## Proposed application boundary (not implemented)

A future adapter should return an evidence envelope containing source type (official MCP/local bridge/screenshot), exact symbol, venue, timeframe, retrieval timestamp, latest-bar timestamp, closed/forming status, freshness/delay status, indicator settings, session definition, source reference and missing fields.

Keep credentials outside source control. Gate account/chart mutations separately from analysis. Retain evidence only under appropriate user consent and data rights. A local stdio bridge is not automatically accessible to the deployed web application.

## Next engineering steps

1. Complete and record the user's local read-only acceptance checks.
2. Choose an adapter based on verified capabilities and permitted usage; keep screenshot upload available.
3. Define and validate the evidence envelope before connecting it to tutor scoring.
4. Add meaningful adapter tests for stale data, missing fields, forming bars, venue mismatch and unsupported intervals when implementation begins.
5. Reconcile any evolving methodology decisions with Notion rather than duplicating them here.
