# Gold Journal application · MVP 0.1

A runnable local web application for MT5 account/history reads, reviewed statement imports, completed-position performance and daily journaling. Python 3.10+ and a current browser are required; no third-party Python packages are needed. Run it on the PC where MT5 is running. The hosted copy supports file imports and evidence downloads; it cannot access the desktop terminal.

## Start on Windows

1. Download this proposal branch (or switch to `docs/gold-terminal-journal-mvp-20261018`). Keep MT5 running, enable its internal MCP server at `http://127.0.0.1:22346/mcp`, and verify the intended account. Prefer broker investor/read-only access. Regenerate the key that was shared in chat.
2. Open PowerShell in the repository folder. The following prompts privately for the replacement key instead of saving it in shell history. The process environment is cleared when the service exits:

```powershell
$mt5JournalSecret = Read-Host 'MT5 internal MCP key' -AsSecureString
$mt5JournalPointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($mt5JournalSecret)
try {
    $env:MT5_MCP_TOKEN = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($mt5JournalPointer)
    python apps/mt5-journal/server.py
} finally {
    Remove-Item Env:MT5_MCP_TOKEN -ErrorAction SilentlyContinue
    [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($mt5JournalPointer)
}
```

3. Open **http://127.0.0.1:8088** and select **Connect local MT5**. Only the terminal endpoint is used. There is no need to connect MetaEditor or the separate remote Marketaux/MetaTrader marketdata services.
4. Select `get_trading_account_info`, inspect its schema, supply the required arguments, and read it. Verify currency, demo/real type and the intended broker account privately.
5. Select a history tool and supply a bounded range using its actual discovered schema. Inspect pagination and coverage; repeat bounded reads as necessary. The current app does not auto-page tool results or merge/reconcile fragmented deal records.
6. Select **Review this result in ledger**. Choose the correct returned record array and map ID, closing time and **net after all costs**. Confirm only if all records are fully closed, unique positions for one account and currency. Raw orders/deals and partial closes must be reconciled first. MT5 reconstructed positions are still subject to broker-history verification.
7. Set the date scope, account mode and currency, calculate results, write your daily review, and save locally or download the evidence bundle.

If native MCP history output is not machine-readable JSON, export a reviewed CSV from broker history. The app does not guess financial meanings from unstructured text or silently infer undocumented MT5 fields.

## Included features

- Native Streamable HTTP MCP initialize/list/call with JSON and SSE response handling and session headers.
- Fixed loopback terminal endpoint and exact allowlist for account, open positions, history, marketwatch and time reads. No generic MCP method route, order/stop operations, arbitrary URL, shell execution or chart modification.
- Actual discovered schemas and explicit argument objects; safe connection/errors and last-read timestamps.
- CSV/JSON import and native JSON result-array review; duplicate-ID, date and numeric validation. Imports remain in memory until deliberately exported or included in a saved review.
- Reviewed net P/L, win rate (wins / all completed positions including flat), net profit factor and per-position expectancy, scoped by Vancouver dates. Open exposure does not automatically enter metrics. No inferred MAE/MFE or risk multiples.
- Fictional sample data behind an explicit button, visibly labeled. It is never loaded as an MT5 feed.
- Daily notes, process assessment, one experiment, screenshot previews and JSON evidence export. No screenshot OCR or automated coaching.
- Local SQLite review persistence at `~/.gold-journal/journal.sqlite3`; set `GOLD_JOURNAL_DB` privately to override. Saved reviews include reviewed positions and notes. Screenshots and raw source results are not stored. Recent saved reviews are listed; editing/deleting stored reviews is not implemented. Back up the database and downloaded evidence privately.

## Security and deployment boundary

The service binds only `127.0.0.1:8088`. Host/origin checks and a required custom header block cross-origin writes; no CORS or public bridge is enabled. The MT5 bearer key is used only in server-to-terminal requests, never sent to the browser. Known credential fields and the current token value are redacted from JSON responses/storage. Provider error bodies and request URLs are not logged. Local account data and the SQLite database are private financial records; the database is not encrypted by this application. Other software running under the same OS account is within the local trust boundary.

An application allowlist is not a substitute for broker read-only permissions. Keep MT5's full trading server and the local journal port off the public internet. A local MCP key must not be committed or configured in the static hosted interface. No key is included in these files.

The UI includes a link to the existing Notion journal. Saving a review does not call Notion, Discord, an LLM, or an execution service. Marketaux's separate news script remains a one-shot source adapter. No background polling, hosted account ingestion, multi-user authentication or production cloud persistence is implemented here.

## Verification

Run from this directory:

```sh
python -m unittest discover -s tests -p 'test_*.py'
node tests/metrics.test.cjs
```

Tests exercise mocked native MCP protocol responses, exact read-only restrictions, origin protections, journal persistence, CSV parsing, duplicate IDs, date scope, financial denominators and exceptional cases. Actual terminal/broker reads require the local setup above and remain unverified from the cloud workspace. No actual trades or account records were retrieved during development. Browser QA was unavailable in this workspace; a Windows native-MCP smoke test remains required.
