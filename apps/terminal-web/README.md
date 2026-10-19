# Gold Intelligence Terminal

A working private research dashboard and trade journal. Source-linked news, independent provider references, timezone-aware session briefings, reviewed performance, immutable daily reviews and private evidence attachments.

The existing hosted application is at https://gold-fundamentals-desk-dennis.dennis-klicksmartai.chatgpt.site . Its R2 news snapshot and enabled pre-session tasks are preserved by code deployments. No provider key or user records are stored in this repository.

## Run the development preview

Requires Node.js 22 or later. No package installation is needed.

```sh
cd apps/terminal-web
mkdir -p .openai
cp .openai/hosting.example.json .openai/hosting.json
npm run build
npm test
npm run dev
```

Open http://localhost:4173 . The preview injects a **development-only identity** and uses an in-memory store. It must stay private/local and is not the production server. It starts with dated editorial seed context. An optional ignored `.sites-runtime/preview-snapshot.json` supplies a development snapshot; never commit user data there. The production Worker does not inject identities and requires Sites-authenticated visitor headers for journal data.

## Production

Use Sites setup/source workflow for the existing project. Configure `.openai/hosting.json` with its actual returned project ID and the existing R2 `BUCKET` binding. Build using `node scripts/build-news.mjs`; the Worker is `dist/server/index.js`. Publish the exact pushed state and preserve the current private audience. Never publish the development HTTP server. Reuse `news/latest.json`, GET/PUT `/api/news` and the two existing MCP news tools.

Journal APIs are owner-scoped through visitor identity: GET/POST `/api/journal`, GET/POST `/api/reviews`, POST `/api/evidence` and GET `/api/evidence/:id`. A shared news service token supplies no visitor identity, so it cannot read personal financial data. The Worker recomputes metrics, enforces bounded input, rejects duplicate positions and concurrent snapshot replacement, and checks attachment ownership. Reviews are append-only. Daily financial scope is the selected Vancouver closing date, regardless of the multi-day dashboard snapshot.

See [release behavior and verification](DASHBOARD-RELEASE.md). MT5 remains a separate [local collector](../mt5-journal/README.md); [Alpha Vantage collection](../alpha-vantage-feed/README.md) is also a separate process. No DXY, exact VWAP/MAE/MFE, automatic OCR, AI tutoring, Notion sync or broker order execution is claimed.
