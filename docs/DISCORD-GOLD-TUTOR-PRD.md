# Discord Gold Tutor MVP

Proposal v1 · 18 October 2026 · Companion application to the [Gold Research Terminal](PRD.md)

## 1 Purpose and application boundary

Run the Gold Tutor inside Discord as a separate deployable application. Help traders understand the Gold Institutional Trading framework, practice session classification, ask lesson questions, and review submitted chart evidence. Keep research tables, broker statements, reconciliation, performance calculations, and the durable trade journal in the web terminal.

Use two applications in one repository initially: apps/terminal-web and apps/discord-tutor. Shared contracts and services prevent contradictory definitions of evidence, trade identity, metrics, and methodology. This is a proposed architecture, not a registered or running Discord application.

The course/tutor roadmap is no longer entirely deferred: a small curated lesson/Q&A and screenshot-review slice becomes the Discord MVP. Full course delivery, video production, paid community billing, autonomous moderation, and live voice tutoring remain later work.

## 2 User journeys and commands

Proposed command names are product contracts to register during implementation, not existing commands.

| Command | User purpose | MVP response and boundary |
|---|---|---|
| /gold ask question | Explain a concept | Answer from approved methodology with source references and uncertainty |
| /gold lesson topic | Find a short lesson | Curated explanation, one practice question, source/version, and next resource |
| /gold review screenshot | Request chart review | Evidence-first observations, supported context, missing evidence, and one learning point |
| /gold practice topic | Practice recognition | A curated exercise; feedback explains reasoning rather than promising trade success |
| /gold journal | Open trade journal | Authenticated terminal link; no account P/L posted to a public channel |
| /gold daily-review date | Discuss an existing daily review | Owner-authorized summary of its immutable metrics snapshot and approved/draft status |
| /gold link | Link Discord and terminal identity | Short-lived, single-use authenticated linking flow; no password or broker login in chat |
| /gold privacy | Understand and manage stored evidence | Storage/deletion controls and account-unlink route |

Public educational questions may be answered in an explicitly configured education channel. Personal screenshots, journal results, and daily coaching use private interaction responses where supported or an authenticated web handoff. For sensitive statements and account-identifying images, direct upload to the private web terminal is the default. Do not ask users to put financial statements in public channels.

## 3 Tutor behaviour

Teach the existing framework without inventing a new mandatory indicator rule. Consult the living Notion methodology and the existing [AI Tutor contract](AI-TUTOR-SPEC.md). Preserve source/version information in a curated, permission-appropriate knowledge index. Private trading records are not part of the public course retrieval corpus.

Screenshot review separates visible facts, reproducible calculations if input exists, interpretation, and unknowns. Ask for the missing instrument, feed, timestamp, timeframe, or higher-timeframe evidence when it changes the interpretation. A single image need not support a full multi-timeframe conclusion. Do not claim access to unsubmitted charts or the user's TradingView account.

Session classification uses Pullback, Continuation, Reversal, or Sideways only when supported. It is descriptive, not a winning probability. Entry Quality and Behaviour numerical scoring are optional later features under their versioned contracts; the Discord MVP must not fabricate a full score from incomplete evidence.

In a daily-review conversation, retrieve the linked user's selected review and its calculation version through the authorized API. Quote existing metrics rather than recalculate them with the model. Distinguish followed process from profitable outcome. Provide one measurable learning experiment, ask for evidence when needed, and preserve the original thesis.

No live trade calls, orders, unsolicited DMs, bulk channel posting, automatic daily broadcasts, trading permissions, or risk escalation. Replies follow explicit commands; additionally, a user-requested Notion review may generate one private completion notification after verified linking and notification opt-in. This bounded event-driven flow is defined in [Notion tutor trigger](NOTION-TUTOR-TRIGGER.md). Scheduled community content remains a separate feature.

## Notion journal requests

A trader marks an entry Ready for AI Review. A verified change adapter fetches current evidence, queues an idempotent review, writes a versioned result back to Notion, and privately notifies the linked trader if enabled. Editing unrelated fields or the tutor's own result does not retrigger it. Background completion uses configured bot delivery, not an expired slash-command token. Review findings remain drafts for trader approval. See the [trigger contract](NOTION-TUTOR-TRIGGER.md).

## 4 Discord interaction implementation

Prefer slash commands and interaction components delivered to an HTTPS endpoint for MVP. This avoids requiring a persistent Gateway connection solely to handle commands. Do not subscribe to arbitrary server conversations or request Message Content access for the proposed command-only flow. Validate installed scopes and contexts against current platform requirements before registration.

Discord documents HTTP interaction delivery, deferred responses, private interaction flags, a three-second initial-response deadline, and a 15-minute interaction-token window. Verify these platform constraints again at implementation; acknowledge/defer before starting long retrieval/model jobs, and use a protected job/status link when work exceeds the reply window. Sources checked on 18 October 2026:
- https://docs.discord.com/developers/interactions/receiving-and-responding
- https://docs.discord.com/developers/interactions/application-commands

Verify incoming Discord requests using the current documented signature procedure and raw body. Invalid signatures fail before work is queued. Validate application/user/context identity, permissions, allowed guild/channel, and component ownership. Use interaction ID as an idempotency key and enforce bounded retries, timeouts, output length, per-user quotas, and provider budgets. Disable automatic mentions in model-generated text.

Treat attachment metadata/URLs and user text as untrusted. Allow only supported attachment sources, validate content and size, copy permitted evidence to private storage with ownership/provenance, and do not rely on temporary Discord URLs as durable storage. If a screenshot was posted publicly, a private bot reply does not make the original image private; warn and offer the private upload path. Do not log interaction tokens, signed attachment URLs, or raw personal account details.

## 5 Shared identity and private data

Use a stable internal user ID plus a verified Discord user-ID mapping. Discord display names, roles, email guesses, guild membership, and caller-supplied trade IDs are not sufficient proof of journal ownership. The logged-in terminal session must confirm the intended Discord account before linking. Link tickets expire, are one use, and bind the initiating identity and purpose.

Enforce ownership again at every journal/review read and save. A bot process credential cannot authorize arbitrary access to all users. A forged interaction parameter or another user's review ID must be rejected. Public tutoring uses only approved nonpersonal knowledge; personal retrieval is isolated by user and record permissions. Unlinking blocks future cross-application reads; data deletion follows a documented policy without claiming to remove copies already visible on Discord.

Use short-lived authenticated deep links and private interaction responses; never embed journal access tokens or broker data into public URLs. Keep model, database, and Discord credentials in each deployable's server-side secrets. Separate deployment permissions and rate budgets for each app.

## 6 Shared service contracts

- Knowledge service: curated lesson ID/content/version and source permissions; refreshes do not overwrite historical reviews.
- Evidence service: owner, original source, capture/retrieval times, instrument/venue, timeframe, content hash, review status, and retention.
- Tutor service: structured observations, missing evidence, interpretation, sources, learning point, and prompt/model version.
- Journal/metrics API: authorized read of immutable calculation snapshots; metrics remain deterministic under [METRICS-SPEC](METRICS-SPEC.md).
- Review persistence: direct Discord saves require confirmation; an explicit Notion Ready request authorizes versioned review writeback under the trigger contract. Retries map to one durable result. Neither path automatically confirms extracted broker rows.

Prefer shared packages for contracts, knowledge retrieval, evidence validation, analytics types, and structured tutor logic. Use a service/API boundary for data access rather than duplicating database logic inside Discord handlers. A Discord service outage must not disable the terminal journal; a news-provider outage must not disable lessons.

## 7 Deliverables and rollout

1. Curated knowledge set, source/version contract, command schema, and privacy/access design.
2. Developer test application in a chosen test server/context, using synthetic nonpersonal charts and journal records.
3. Signature-verified command handler with deferred replies, safe errors, quotas, and no ambient message monitoring.
4. Ask/lesson/practice and evidence-qualified screenshot-review flows.
5. Verified user linking and private journal/deep-link flow; daily-review retrieval after the web journal API is ready.
6. End-to-end permission and failure tests, documented registration/install steps, operational metrics, and a small invited pilot.

Discord application ID, public key, installation target, server/channel IDs, bot credentials where needed, and real deployment environment are setup dependencies. This proposal does not create an app, install a bot, join a server, send a message, or enable background activity.

## 8 Acceptance criteria

| ID | Passing condition |
|---|---|
| DISC01 | Valid interactions are acknowledged/deferred within the platform deadline; invalid signatures never queue work |
| DISC02 | Duplicate delivery produces one job and no duplicate saved review |
| DISC03 | A curated concept answer links to approved source material and states unknowns |
| DISC04 | Incomplete screenshot evidence cannot yield fabricated levels, exact MAE/MFE, or a full entry score |
| DISC05 | Educational channel replies never include another user's journal or personal retrieval context |
| DISC06 | Journal reads require verified linking and record ownership; forged user/review IDs fail |
| DISC07 | Expired reply token, failed model call, attachment expiry, and rate limits produce clear recoverable states |
| DISC08 | Unlink/revoke stops future cross-app access without affecting the user's terminal login |
| DISC09 | Save requires explicit confirmation and returns the persisted terminal URL |
| DISC10 | The terminal remains usable while Discord is unavailable, and the tutor can teach while market feeds are down |

Pilot measures: grounded-answer coverage, human agreement on screenshot observations, unknown-evidence handling, successful private handoffs, latency, and repeated confirmed learning/process errors. Do not promise trading returns from tutor usage.
