# Agent Requirements

This file is part of the split simulation requirements set. Requirement IDs and requirement text are preserved from the original monolithic requirements document.

## 4. Agent Types For First Pass

### Rationale

First-pass agents are intentionally simple enough to isolate Charter mechanics. Agent behavior exists to generate rule-relevant inputs, not to model high-fidelity political psychology.

### Common Agent Requirements

| ID | Requirement | Suggested Verification |
| --- | --- | --- |
| SIM-REQ-040 | Each agent shall have a stable identifier. | Agent initialization test. |
| SIM-REQ-041 | Each agent shall expose required state to the engine through typed data structures. | Serialization test. |
| SIM-REQ-042 | Each agent shall emit actions as simulation events. | Agent action test. |
| SIM-REQ-043 | Each agent shall accept deterministic configuration parameters. | Scenario loading test. |
| SIM-REQ-044 | Any stochastic agent choice shall use the scenario random seed. | Deterministic replay test. |
| SIM-REQ-045 | Each agent action event shall include `actor_id`, `event_type`, `submitted_tick`, and action-specific payload. | Agent event schema test. |
| SIM-REQ-046 | Each agent shall receive only the scenario inputs and public engine state declared for its agent type. | Agent boundary test. |
| SIM-REQ-047 | Each agent shall produce zero or more events per tick according to its configured behavior model. | Agent step test. |
| SIM-REQ-048 | Each agent shall expose a deterministic idle outcome when no configured action condition is met. | Idle behavior test. |

### Subscriber Agent

| Category | First-Pass Requirement |
| --- | --- |
| Required state | Subscriber ID, group labels, current delegation, pending delegation changes, petition support count, satisfaction value. |
| Required inputs | Scenario preferences, observed outcomes, satisfaction update parameters, delegation options. |
| Required actions | Create delegation, revoke delegation, transfer delegation, support petition, withdraw petition support, vote in configured decisions. |
| Required outputs | Delegation events, petition support events, vote events, satisfaction updates. |
| Configuration parameters | Initial group, baseline satisfaction, delegation propensity, churn tolerance, petition propensity, voting profile. |
| Minimum behavior model | Rule-based thresholds using configured satisfaction and event responses. |

Requirements:

| ID | Requirement | Suggested Verification |
| --- | --- | --- |
| SIM-REQ-050 | Subscriber agents shall hold exactly one representation token. | Initialization test. |
| SIM-REQ-051 | Subscriber agents shall emit fractional or whole-token delegation events when fractional delegation is enabled. | Delegation test. |
| SIM-REQ-052 | Subscriber agents shall emit vote events for Authority formation, reauthorization, National Decision, and scenario-defined legislative decisions when configured voting conditions are met. | Voting event tests. |
| SIM-REQ-053 | Subscriber agents shall emit delegation creation as a `delegation_create` event with `source_subscriber_id`, `target_representative_id`, `token_share`, and `submitted_tick`. | Delegation event schema test. |
| SIM-REQ-054 | Subscriber agents shall emit delegation revocation as a `delegation_revoke` event with `source_subscriber_id`, `delegation_id`, and `submitted_tick`. | Revocation event schema test. |
| SIM-REQ-055 | Subscriber agents shall emit delegation transfer as paired revocation and creation events or as a `delegation_transfer` event with equivalent source, old target, new target, token share, and submitted tick fields. | Transfer event schema test. |
| SIM-REQ-056 | Subscriber agents shall emit vote events with `voter_id`, `decision_id`, `vote_value`, `vote_weight_basis`, and `submitted_tick`. | Vote event schema test. |
| SIM-REQ-057 | Subscriber agents shall update satisfaction only through configured satisfaction inputs and shall emit the resulting value as a state update event. | Satisfaction update test. |

### Representative Agent

| Category | First-Pass Requirement |
| --- | --- |
| Required state | Representative ID, subscriber ID if applicable, raw delegated tokens, weighted delegation, coalition identifier if configured. |
| Required inputs | Delegations received, cap rules, coalition rules, voting profile. |
| Required actions | Cast aggregated votes, join or leave configured coalition, receive or lose delegation. |
| Required outputs | Aggregated vote events, cap violation events, coalition status events. |
| Configuration parameters | Ideological or policy label, coalition membership, voting strategy, cap compliance behavior. |
| Minimum behavior model | Deterministic voting according to configured profile and current delegated weight. |

Requirements:

| ID | Requirement | Suggested Verification |
| --- | --- | --- |
| SIM-REQ-060 | Representative agents shall report raw delegated token totals. | Delegation aggregation test. |
| SIM-REQ-061 | Representative agents shall report weighted delegation totals. | Weighting test. |
| SIM-REQ-062 | Representative agents shall be subject to raw and weighted delegation caps. | Cap enforcement test. |
| SIM-REQ-063 | Representative agents shall emit aggregated vote events with `representative_id`, `decision_id`, `raw_token_total`, `weighted_token_total`, and `vote_value`. | Aggregated vote schema test. |
| SIM-REQ-064 | Representative agents shall not include pending delegations in aggregated vote events. | Pending delegation exclusion test. |
| SIM-REQ-065 | Representative agents shall expose coalition membership as input to cap evaluation when `coalition_id` is configured. | Coalition cap input test. |

### Authority Agent

| Category | First-Pass Requirement |
| --- | --- |
| Required state | Authority ID, Authority Charter, scope model, active status, renewal date, satisfaction history, resource balance if configured. |
| Required inputs | Charter scope, funding configuration, event requests, review decisions, emergency triggers. |
| Required actions | Propose action, claim scope, declare emergency if configured, submit to review, dissolve, merge, separate. |
| Required outputs | Authority action events, scope claims, emergency declarations, review records, lifecycle events. |
| Configuration parameters | Coercive status, permitted powers, territory, population affected, review interval, satisfaction response parameters. |
| Minimum behavior model | Deterministic scope-limited action selection from scenario event requests. |

Requirements:

| ID | Requirement | Suggested Verification |
| --- | --- | --- |
| SIM-REQ-070 | Authority agents shall not execute actions until the engine marks the Authority active. | Authority lifecycle test. |
| SIM-REQ-071 | Authority agents shall submit proposed actions to scope validation before execution. | Scope validation test. |
| SIM-REQ-072 | Authority agents shall expose lifecycle state for creation, activation, review, reauthorization, dissolution, merger, and separation. | Lifecycle state test. |
| SIM-REQ-073 | Authority agents shall emit proposed action events with `authority_id`, `scope_id`, `requested_power`, `affected_territory`, `affected_population`, `resource_request`, and `submitted_tick`. | Authority action event schema test. |
| SIM-REQ-074 | Authority agents shall receive an engine decision before changing lifecycle state. | Lifecycle transition test. |
| SIM-REQ-075 | Authority agents shall emit emergency declaration events with `authority_id`, `qualifying_condition`, `affected_scope`, `declared_tick`, and requested emergency powers. | Emergency declaration schema test. |
| SIM-REQ-076 | Authority agents shall emit review submission events with `authority_id`, `review_type`, `review_period`, and evidence payload. | Review event schema test. |

### Adversarial Faction Agent

This is a simulation abstraction.

| Category | First-Pass Requirement |
| --- | --- |
| Required state | Faction ID, target rules, controlled agents if configured, budget or action capacity if configured, capture strategy. |
| Required inputs | Scenario objectives, observed power concentration, delegation landscape, Authority targets. |
| Required actions | Coordinate delegation shifts, create petition pressure, attempt coalition concentration, attempt scope pressure. |
| Required outputs | Capture attempt events, coordinated action events, success or failure records. |
| Configuration parameters | Aggressiveness, target Authority, target Representative, coordination window, resource limit, detection exposure. |
| Minimum behavior model | Deterministic or seeded strategy attempting to maximize configured concentration or scope expansion objective. |

Requirements:

| ID | Requirement | Suggested Verification |
| --- | --- | --- |
| SIM-REQ-080 | Adversarial faction agents shall be labeled as simulation abstractions. | Manifest review. |
| SIM-REQ-081 | Adversarial faction agents shall not receive Charter powers unavailable to ordinary Subscribers, Representatives, or Authorities. | Scenario validation test. |
| SIM-REQ-082 | Adversarial faction agents shall generate capture-attempt events for metrics. | Event log test. |
| SIM-REQ-083 | Adversarial faction agents shall declare `target_metric`, `target_actor_id`, `strategy`, and `success_condition` in scenario configuration. | Scenario validation test. |
| SIM-REQ-084 | Adversarial faction agents shall emit coordinated action events that identify every controlled or influenced actor used by the event. | Capture event schema test. |
| SIM-REQ-085 | Adversarial faction agents shall report failed attempts as events rather than omitting them. | Capture metrics test. |

### Court Or Review Agent

| Category | First-Pass Requirement |
| --- | --- |
| Required state | Review body ID, jurisdiction type, pending review queue, decision rule, load count. |
| Required inputs | Scope conflicts, rights or scope violation claims, emergency reviews, consolidation appeals. |
| Required actions | Accept review event, issue deterministic decision, invalidate action if configured criteria are met. |
| Required outputs | Review decisions, invalidation events, load metrics. |
| Configuration parameters | Decision mode, review latency, invalidation criteria, capacity per tick. |
| Minimum behavior model | Deterministic rule-based review using configured criteria. |

Requirements:

| ID | Requirement | Suggested Verification |
| --- | --- | --- |
| SIM-REQ-090 | Court or review agents shall apply deterministic decision rules. | Deterministic review test. |
| SIM-REQ-091 | Court or review agents shall record review queue length by tick. | Metrics test. |
| SIM-REQ-092 | Court or review agents shall not create new Authority powers. | Review output validation test. |
| SIM-REQ-093 | Court or review agents shall accept review requests with `review_id`, `review_type`, `claimant_id`, `target_event_id`, `authority_id`, and `submitted_tick`. | Review request schema test. |
| SIM-REQ-094 | Court or review agents shall emit review decisions with `review_id`, `decision`, `reason`, `affected_event_id`, and `decision_tick`. | Review decision schema test. |
| SIM-REQ-095 | Court or review agents shall mark decisions that rely on simulation-only review criteria as simulation abstractions. | Manifest and decision log test. |

### Event Generator Or Environment Agent

This is a simulation abstraction.

| Category | First-Pass Requirement |
| --- | --- |
| Required state | Event schedule, random event parameters if enabled, active crisis state. |
| Required inputs | Scenario event configuration, random seed, current tick. |
| Required actions | Emit scheduled events, emit seeded random events, end events when configured. |
| Required outputs | Crisis events, demand events, resource events, satisfaction shock events. |
| Configuration parameters | Event schedule, event frequency, affected territory, affected population, severity, duration. |
| Minimum behavior model | Scheduled deterministic events with optional seeded random variation. |

Requirements:

| ID | Requirement | Suggested Verification |
| --- | --- | --- |
| SIM-REQ-100 | Event generator agents shall be labeled as simulation abstractions. | Manifest review. |
| SIM-REQ-101 | Event generator agents shall emit events only from scenario configuration or seeded random generation. | Replay test. |
| SIM-REQ-102 | Event generator agents shall identify affected function, territory, population, and severity where applicable. | Event schema test. |
| SIM-REQ-103 | Event generator agents shall emit scheduled events at the configured tick. | Schedule test. |
| SIM-REQ-104 | Event generator agents shall emit event termination records when configured event duration ends. | Event lifecycle test. |
| SIM-REQ-105 | Event generator agents shall not directly modify Subscriber, Representative, or Authority state. | State transition audit test. |


