# Notion Journal to Gold Tutor Review Trigger

Proposal v1 · Part of the [two-app MVP](PRD.md) and [Discord Tutor](DISCORD-GOLD-TUTOR-PRD.md)

## 1 Event-driven learning loop

A trader prepares an entry in the existing Notion journal and explicitly requests an AI review. A service snapshots the evidence, queues a tutor job, validates any financial metrics, and writes a versioned review back to the journal. If the trader has linked Discord and enabled review notifications, the Discord app sends a private completion notification and offers follow-up questions.

The trigger is **Ready for AI Review**, not every edit or upload. Saving financial data and asking for coaching are separate actions. The request can cover a screenshot/idea review or a daily performance review. Missing statement or price-path evidence limits the result rather than becoming invented numbers.

This is an application workflow specification. No webhook, Notion schema change, hosted worker, Discord installation, or notification has been enabled by writing it.

## 2 Proposed Notion properties

Fetch the actual target data-source schema before implementing these additions. Add dedicated review properties instead of repurposing the journal's existing trade Status, Risk confirmed, Result reconciled, Session, or execution relations. Existing Template records must be excluded.

| Property | Purpose |
|---|---|
| AI review state | Draft, Ready for AI Review, Queued, Analysing, Complete, Needs evidence, Failed, Stale |
| Review type | Screenshot/idea or Daily performance |
| Review request ID | New stable request identity for each explicit request/re-request |
| Requested by | Verified internal owner mapping, not an arbitrary display name |
| Review source version | Canonical input snapshot/hash; exclude tutor output fields |
| Tutor review link | Durable review record or controlled Notion result section |
| Reviewed at | Actual completion time |
| Review issue | Missing evidence or safe failure explanation |

Keep notification preference and verified Discord linkage in protected application settings rather than a user-editable channel-ID property. Do not trust a Notion field to redirect another user's financial results. An explicitly configured button may set the request state/identity if supported, but the server must validate it; do not assume a native Notion automation exists.

## 3 Service flow

1. Trader selects a supported entry and marks it Ready for AI Review with a review type. For another analysis, explicitly request a new version.
2. A verified Notion event notifies the backend; fetch current page/properties/evidence using an authorized connection. Events are change hints, not a complete trusted financial record.
3. Check mapped workspace/data source/page ownership, non-template state, allowed review type, request identity, and accessible evidence. Ignore unrelated or previously handled changes.
4. Create a durable request/job and input snapshot, then mark Queued. Process subsequent steps asynchronously with a per-page/request lease.
5. Build the evidence bundle. Reuse confirmed metric runs for financial claims. A Notion number alone is not proof of a reconciled statement; link to a validated import or mark it user-reported.
6. Tutor generates structured observations, uncertainty, supported findings, and one improvement experiment. Validate source IDs and deterministic metrics before publication.
7. Recheck current source revision. If relevant inputs changed, label Stale and request a fresh review; do not silently replace a review of the old thesis with one of the new thesis.
8. Write a versioned Tutor Review section/link and Complete or Needs evidence state, preserving original thesis, screenshots, financial records, and human notes.
9. After writeback succeeds, create a completion-notification outbox item if the linked trader opted in. Discord privately notifies completion with an authenticated review link. The notification is not the storage source of truth.
10. Trader asks follow-up questions in Discord using the same review ID. Replies retain its input/metric versions and ownership checks.

## 4 Notion delivery adapter

Official Notion documentation describes webhook subscriptions, signed event delivery, and fetching current entity data after an event. Production validates signatures before queueing. Use subscribed page-property/content event types appropriate to the installed API version; do not equate a content update event with a requested review. Events may aggregate, retry, or arrive out of order. Source documentation checked on 18 October 2026:
- https://developers.notion.com/reference/webhooks
- https://developers.notion.com/reference/webhooks-events-delivery

Keep subscription verification tokens and integration credentials in secrets. Bind incoming events to the expected connection/workspace, retain a deduplicated event identity, and acknowledge only after durable handoff. Avoid long model work in the webhook request.

If webhooks are unavailable, an explicitly configured bounded polling adapter can inspect designated entries for Ready for AI Review. It must use the same ownership, request, and idempotency rules and show polling delay. Polling is an implementation alternative, not a scheduled task enabled in this chat.

## 5 Idempotency and loop prevention

Use a unique job key of workspace + page + verified owner + review request ID. Store source snapshot hash and relevant evidence version on the job. Event ID deduplication protects transport retries; job-key uniqueness protects against separate events describing the same request.

Canonical input hashing includes thesis, relevant source fields, evidence IDs/versions, review type, and linked metric run. Exclude AI review state transitions, output sections, notification status, and completion timestamps. Otherwise the tutor's own writeback can appear as fresh evidence and create a loop.

Ready → Queued → Analysing → Complete is a single request lifecycle. Complete, Failed, or Needs evidence do not automatically requeue just because the page was edited. A new explicit request creates a new identity. Keep old reviews for comparison. Per-page serialization and a database lease prevent competing workers; fetch and compare inputs immediately before writeback, record version metadata, and mark late-detected changes Stale. Do not assume a Notion property write and application database transaction are atomic.

Retries reuse request identity and already completed steps. A writeback failure does not regenerate the model answer. Notification retries do not rerun analysis. Rate limits and model budgets apply by verified user/workspace. A dead-letter state exposes remediation without leaking secrets.

## 6 Evidence and metrics gates

Screenshot/idea review may proceed with visible chart evidence plus instrument/timeframe context and explicit missing-data statements. It does not need to invent account results to be useful.

Daily performance review requires a declared day/timezone, account/currency, mode, grain, and source coverage. Prefer reconciled executions and confirmed idea grouping. If missing, return Needs evidence with a checklist or a clearly limited qualitative review. Apply [METRICS-SPEC](METRICS-SPEC.md): statements alone cannot produce exact MAE/MFE; original approved risk is required for R; deposits and open trades are not wins/losses.

The tutor never changes broker P/L, net-cost semantics, original stops/thesis, execution grouping, or risk policy to match its narrative. A generated lesson is a hypothesis for Dennis to review, not a proven explanation of losses.

## 7 Discord completion delivery

The user explicitly enables notifications for requested tutor reviews and verifies the Discord account link. This grants a bounded completion notification for that user's requested review, not broadcast permission or access to all channel messages. No Discord server/channel IDs from arbitrary journal fields may route personal data.

A Notion-triggered background job has no fresh Discord interaction token. Use the authorized bot delivery mechanism and configured private destination after setup; do not reuse an expired slash-command token. Default notification includes completion state and a protected link, not account numbers, balances, statement images, or detailed P/L. Permission checks also apply when opening the link.

If DMs are blocked or the user unlinks/revokes notifications, retain the completed Notion/web review and show notification failure or suppression. Never fall back to a public channel. Deduplicate with request ID + destination + completion version. Account linking, notification delivery, and tutor jobs have independently observable states.

## 8 Output contract

Review result: request ID, source page ID, owner, review type, source snapshot/version, evidence cutoff, metric-run ID if any, observed facts, uncertainty, supported findings, best disciplined decision, one issue to investigate, one measurable experiment, model/prompt/methodology versions, approval state, completed time, and durable review URL.

State is Complete when an evidence-qualified review is persisted, not when a model merely returns text. Needs evidence is a useful outcome. Publication is draft coaching until Dennis reviews it. Corrected sources create a new request/version, not historical rewriting.

## 9 Implementation and acceptance

Add a Notion event adapter, durable request/job table, snapshot builder, tutor worker, validated writeback, notification outbox, and private Discord delivery. Reuse application ownership, metrics, and evidence services. This is a bounded event-driven integration, not unrestricted bidirectional synchronization of the entire journal.

| ID | Passing condition |
|---|---|
| TRIG01 | A real authorized Ready request creates one durable job; ordinary edits and Template pages do not |
| TRIG02 | Duplicate and out-of-order events cannot duplicate a job, review, or completion notification |
| TRIG03 | Tutor state/output writes cannot retrigger their own review |
| TRIG04 | Invalid signature, wrong workspace, inaccessible page, or unmapped owner cannot start personal analysis |
| TRIG05 | Missing statement/path/risk evidence yields qualified output or Needs evidence, not fabricated metrics |
| TRIG06 | Input changes during processing prevent an unlabeled stale result from overwriting the current review |
| TRIG07 | Writeback and notification failures retry independently without rerunning completed analysis |
| TRIG08 | A user with notifications enabled receives one private completion link; disabled/blocked delivery never falls back publicly |
| TRIG09 | A saved review preserves the original thesis, financial facts, and user notes |
| TRIG10 | Re-requesting a review creates a traceable new version while previous approved reviews remain available |

Rollout dependencies: hosted API/worker, authorized Notion integration and subscription, schema additions, verified user mapping, Discord app/private delivery setup, retention policy, and a synthetic end-to-end test. None is currently configured by this proposal.
