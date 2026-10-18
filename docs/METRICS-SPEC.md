# Trade Journal Metrics and Evidence Contract

Proposal v1 · Applies to the [terminal MVP](PRD.md). Calculations are deterministic and versioned; models explain results, not compute or overwrite them.

## Eligibility and provenance

Confirmed rows only enter the final scorecard. Every run identifies input records/revisions, account/currency, instrument, mode, date bounds/timezone, grouping grain, cost semantics, formula version, and exclusions. Preserve raw broker times until their timezone is verified. Do not aggregate account currencies without a declared conversion method.

Grains: a broker execution/partial-close record is not a completed idea. User-confirmed idea grouping includes all related fills and partial exits, with completion at final closure. Count realised execution closes in the day; count completed ideas at final close. Show open/carried positions separately.

Net result is gross profit plus signed commission, swap, and other costs **only if** those costs are not already included. Unknown cost semantics block final financial confirmation. Cash deposits/withdrawals/credits/transfers are not trades. Duplicate detection uses account and execution identity plus partial-close identity; ambiguous composite matches require review.

## Core metrics

Let N=W+L+B for confirmed closed records, with net P/L classified at account-currency precision. W positive, L negative, B zero.

| Metric | Definition | Missing or edge state |
|---|---|---|
| Primary win rate | W/N | N=0 unavailable; breakevens included |
| Decisive win rate | W/(W+L) | Separately labeled; no decisive results unavailable |
| Net P/L | Sum of eligible net results | Currency and cost semantics required |
| Profit factor | Sum positive net / absolute sum negative net | Positive gain with no losses: no-loss sample; all zero: unavailable; no wins with losses: 0 |
| Average win | Sum positive net/W | No winners: unavailable |
| Average loss | Absolute sum negative net/L | No losers: unavailable |
| Expectancy | Net P/L/N | Per selected grain; N=0 unavailable |
| Payoff ratio | Average win/average loss | Both averages required |
| Idea R | Completed idea net / original approved idea cash risk | Positive known original risk required; never margin or guessed historical stop |
| R expectancy | Mean eligible idea R | Report eligible subset and excluded count |
| Rule adherence | Followed/(Followed+Breach) | Unknown/Not applicable excluded and counted visibly; empty eligible set unavailable |

Consecutive losses use fully closed ideas in final-close order when grouping is confirmed. Partial wins do not reset a completed-idea counter. If close order is ambiguous, show an uncertainty state rather than imposing an arbitrary behavioural story. Preserve the journal's configured policy.

Closed-balance drawdown needs a verified opening balance, chronological results, and explicit treatment of external flows. Without balances, label currency drawdown of cumulative trading P/L instead. Floating-equity drawdown requires equity observations. Return percentages need a declared cash-flow-aware methodology; otherwise unavailable.

## MAE and MFE

Statements with only entry, exit, and final P/L cannot establish intratrade extrema. Require verified entry/exit timestamps and price path for the same instrument/venue/contract, with stated coverage and valuation side.

For fixed-size entry E and eligible in-position prices P, report nonnegative price distances:

- Long MAE=max(0,E−min(P)); long MFE=max(0,max(P)−E).
- Short MAE=max(0,max(P)−E); short MFE=max(0,E−min(P)).

Cash conversion requires quantity, multiplier, currency conversion, and explicit costs/spread convention. Use bid for long liquidation and ask for short liquidation where available; midpoint, last, or OHLC measurements are separately labeled approximations. GC futures cannot silently supply exact XAUUSD excursions.

One-minute OHLC is a bar-based approximation. Entry/exit boundary bars can contain pre-entry/post-exit extrema. Exclude uncertain portions or label a bound/estimate; do not claim tick precision. Missing bars, incomplete coverage, or unknown timezone downgrade/suppress output. Zero observed excursion with complete evidence differs from unavailable evidence.

Scaled positions and partial closes require a time-varying inventory/P&L path for idea-level cash excursions. Per-fill extrema need not coincide, so summing MAEs/MFEs is invalid. Excursion R needs original approved idea risk. Report method and eligible/total counts for all excursion aggregates.

A screenshot supports a manually reviewed estimate only if scale and the full relevant interval are visible; it cannot independently establish exact cash excursions. Never invent invisible stops or intrabar order.

## Daily reviews and evidence

Production day bounds are [local midnight, next local midnight) in the verified IANA timezone, converted to UTC. Date-only source data without timezone supports explicitly labeled broker-date reviews, not inferred Vancouver sessions.

Default rubric: pre-entry thesis; predefined risk/stop; applicable session/setup discipline; management-change documentation; post-trade review. Values: Followed, Breach, Unknown, Not applicable. Store rubric version, evidence, and user confirmation. Good P/L cannot establish adherence. Behavioural claims need more than result signs.

Freeze input/metric/evidence IDs at review creation. Corrections mark it out of date and generate a new version. Separate deterministic metrics, user-entered assessments, model hypotheses, and approved conclusions. One experiment includes change, target, evidence, and evaluation window. Do not infer causal improvement from small before/after samples.

## Required synthetic fixtures

| Fixture | Expected result |
|---|---|
| Closed net +100, −50, 0 | N=3; primary win rate 33.33%; decisive rate 50%; PF=2; expectancy=16.67 |
| Two wins, no losses | PF labeled no-loss sample, not an invented large number |
| No trades | Metrics unavailable; no-trade review still allowed |
| Deposit plus closed loss | Deposit excluded from counts and trade P/L |
| Duplicate and overlapping statements | One confirmed execution per identity; corrected rows versioned |
| Partial closes belonging to one idea | Distinct execution totals and one completed idea; no invented grouping |
| Unknown original risk | R unavailable; currency metrics retained when valid |
| Long E=100, low=97, high=108 | Price MAE=3, MFE=8 on valid in-position path |
| Short E=100, low=92, high=103 | Price MAE=3, MFE=8 |
| No path, wrong venue, missing interval | MAE/MFE unavailable or explicitly partial/proxy estimate |
| Boundary candle extends before entry | No unqualified exact excursion claim |
| Scaling with asynchronous extrema | Do not sum per-fill MAEs/MFEs |
| Followed=3, Breach=1, Unknown=2 | 75% known-check adherence; 4 known, 2 unknown |
| Profitable breach versus disciplined loss | Outcome and process labels remain separate |
| Weekend BTC with closed gold/DXY | No fabricated contemporaneous correlation |
| Mixed currencies or unknown fees | No misleading combined confirmed scorecard |
