# Simulation Requirements

## 1. Purpose And Scope

This document defines first-pass requirements for a Jefferson Mark III Charter simulation engine. The engine exists to test Charter mechanics under agent-based scenarios, including failure modes, institutional load, delegation dynamics, authority lifecycle behavior, emergency expiration, scope conflict, consolidation pressure, and adversarial capture attempts.

The first pass is not a full political simulator. It is a deterministic Charter mechanics engine with simple configurable agents and institutions sufficient for stress testing. It shall not predict real-world political outcomes.

### Rationale

The Charter contains threshold, timing, scope, review, emergency, representation, and consolidation rules that can be tested mechanically before richer behavioral modeling exists. A narrow first pass reduces the risk of confusing Charter mechanics with speculative sociology.

### Requirements

| ID | Requirement | Suggested Verification |
| --- | --- | --- |
| SIM-REQ-001 | The simulation engine shall evaluate Charter mechanics under configurable agent-based scenarios. | Review scenario runner interface and scenario fixtures. |
| SIM-REQ-002 | The simulation engine shall keep Charter rule evaluation separate from Mesa runtime integration. | Unit test rules engine without importing Mesa. |
| SIM-REQ-003 | The first-pass simulation shall not claim to predict real-world election, institutional, or population behavior. | Documentation review. |
| SIM-REQ-004 | The first-pass simulation shall support stress testing of delegation, authority formation, authority lifecycle, emergency action, scope conflict, consolidation, and review load. | Scenario suite coverage review. |
| SIM-REQ-005 | The simulation engine shall label any behavior not defined by the Charter as a simulation abstraction. | Requirements and scenario configuration review. |

## 2. Source Of Authority And Source Documents

### Rationale

The simulation is traceable to the Charter and is not an alternate constitutional source. Machine-readable derivatives and requirements documents assist implementation but do not supersede the canonical Charter.

### Requirements

| ID | Requirement | Suggested Verification |
| --- | --- | --- |
| SIM-REQ-010 | The canonical source of Charter authority shall be `charter/charter.md`. | Documentation review. |
| SIM-REQ-011 | The machine-readable derivative shall be `derivatives/simulation/charter_sim.yaml`. | Configuration loading test. |
| SIM-REQ-012 | If this document conflicts with `charter/charter.md`, `charter/charter.md` shall control. | Documentation review. |
| SIM-REQ-013 | If `charter_sim.yaml` conflicts with `charter/charter.md`, the YAML shall be treated as defective. | Validation test using injected mismatch metadata. |
| SIM-REQ-014 | Simulation-only abstractions shall be explicitly marked as simulation abstractions in requirements, configuration, or output metadata. | Static review of scenario schema and generated manifest. |
| SIM-REQ-015 | Charter ambiguities shall be represented as open questions, configurable assumptions, or implementation-blocking validation errors. | Gap-handling unit tests. |

### Charter Source Traceability

Each implemented rule is traceable to a Charter source location or explicitly labeled as a simulation abstraction. Traceability is a first-pass compliance requirement, not a legal interpretation layer.

| ID | Requirement | Suggested Verification |
| --- | --- | --- |
| SIM-REQ-016 | Each engine rule shall have a stable `rule_id`. | Rule registry test. |
| SIM-REQ-017 | Each engine rule shall include `source_document`, `source_article`, `source_section`, and `source_clause` fields when derived from the Charter. | Rule traceability schema test. |
| SIM-REQ-018 | Each engine rule derived from `charter_sim.yaml` shall include the YAML path used as `derivative_path`. | Rule traceability schema test. |
| SIM-REQ-019 | Each simulation abstraction rule shall include `abstraction_label` and `abstraction_rationale`. | Rule traceability schema test. |
| SIM-REQ-020A | The engine shall reject a rule definition that lacks both Charter source traceability and simulation abstraction metadata. | Invalid rule registry test. |
| SIM-REQ-020B | Each rule decision log entry shall include the `rule_id` used to make the decision. | Decision log test. |
| SIM-REQ-020C | Each scenario manifest shall list the Charter-derived rules and simulation abstraction rules enabled for the run. | Manifest test. |
| SIM-REQ-020D | The validation report shall identify any enabled simulation abstraction rule before the run executes. | Validation report test. |

## 3. Core Simulation Concepts

### Rationale

The engine needs stable concepts before Mesa agents are implemented. These concepts are implementation-independent and define the minimum state and events required to test Charter mechanics.

### Requirements

| ID | Requirement | Suggested Verification |
| --- | --- | --- |
| SIM-REQ-020 | The engine shall represent a Subscriber as a political member holding one representation token. | State model unit test. |
| SIM-REQ-021 | The engine shall represent a Representative as a Subscriber receiving delegated representation tokens from other Subscribers. | Delegation fixture test. |
| SIM-REQ-022 | The engine shall represent a Delegation as a revocable assignment of all or part of a Subscriber representation token to a Representative. | Delegation lifecycle test. |
| SIM-REQ-023 | The engine shall represent a Representation Token as the unit of delegable representation held by each Subscriber. | State initialization test. |
| SIM-REQ-024 | The engine shall represent an Authority as a governance body with an Authority Charter and sealed functional scope. | Authority creation test. |
| SIM-REQ-025 | The engine shall represent an Authority Charter as structured data containing scope, funding sources, renewal process, and oversight structures. | Authority charter validation test. |
| SIM-REQ-026 | The engine shall represent a Legislative Authority as an Authority whose configured scope includes legislative act creation. | Scenario schema validation test. |
| SIM-REQ-027 | The engine shall represent an Executive or administrative Authority as an Authority whose configured scope includes administrative execution or coordination. | Scenario schema validation test. |
| SIM-REQ-028 | The engine shall represent a Coercive Authority as an Authority possessing adjudication, enforcement, regulation, or other configured coercive powers. | Coercive threshold test. |
| SIM-REQ-029 | The engine shall represent a Coordination Council as a temporary review body for Authority scope conflicts. | Scope conflict scenario test. |
| SIM-REQ-030 | The engine shall represent the Charter Court or review body as the institution used for Charter review decisions in first-pass scenarios. | Review event test. |
| SIM-REQ-031 | The engine shall represent Emergency Action as a time-limited Authority action triggered under Article V mechanics. | Emergency lifecycle test. |
| SIM-REQ-032 | The engine shall represent a Review or Reauthorization Event as a scheduled institutional decision point. | Scheduler test. |
| SIM-REQ-033 | The engine shall represent Satisfaction Metric as a simulation abstraction unless later defined by Charter amendment. | Manifest review and gap test. |
| SIM-REQ-034 | The engine shall represent a Scope Conflict as an event where two or more Authorities claim incompatible action over the same function, territory, population, resource, or operation. | Scope conflict detection test. |
| SIM-REQ-035 | The engine shall represent a Consolidation Audit as a decennial review event evaluating Authority structure, overlap, and redundancy. | Audit scheduling test. |
| SIM-REQ-036 | The engine shall represent a Simulation Event as a timestamped state transition request with input data, rule decision output, and provenance. | Event log schema test. |
| SIM-REQ-037 | The engine shall represent a Simulation Tick as one discrete time advance in the configured simulation calendar. | Tick advancement test. |

### Core Data And Event Contracts

The following requirements convert core concepts into minimum testable records. Field names are normative for first-pass implementation unless an implementation supplies a documented compatibility mapping.

| ID | Requirement | Suggested Verification |
| --- | --- | --- |
| SIM-REQ-500 | The engine shall store each Subscriber record with `subscriber_id`, `token_id`, `active_status`, and `group_ids`. | Subscriber record schema test. |
| SIM-REQ-501 | The engine shall reject a Subscriber record missing `subscriber_id` or `token_id`. | Invalid state validation test. |
| SIM-REQ-502 | The engine shall store each Representative record with `representative_id`, `subscriber_id`, `raw_delegation_total`, `weighted_delegation_total`, and `coalition_id`. | Representative record schema test. |
| SIM-REQ-503 | The engine shall compute `raw_delegation_total` from active Delegation records rather than accepting it as authoritative input. | Aggregation test. |
| SIM-REQ-504 | The engine shall compute `weighted_delegation_total` from active Delegation records and configured weighting assumptions. | Weight aggregation test. |
| SIM-REQ-505 | The engine shall store each Delegation record with `delegation_id`, `source_subscriber_id`, `target_representative_id`, `token_share`, `submitted_tick`, `activation_tick`, `status`, and `reason`. | Delegation record schema test. |
| SIM-REQ-506 | The engine shall reject a Delegation record whose `token_share` is less than or equal to zero. | Invalid delegation test. |
| SIM-REQ-507 | The engine shall reject a set of active Delegation records whose `token_share` total exceeds one for a single Subscriber. | Token conservation test. |
| SIM-REQ-508 | The engine shall store each Authority record with `authority_id`, `charter_id`, `authority_type`, `coercive_status`, `scope_id`, `lifecycle_status`, `activation_tick`, `review_due_tick`, and `dissolution_tick`. | Authority record schema test. |
| SIM-REQ-509 | The engine shall reject an active Authority record without an associated Authority Charter record. | Invalid Authority state test. |
| SIM-REQ-510 | The engine shall store each Authority Charter record with `charter_id`, `scope_id`, `funding_sources`, `renewal_process`, `oversight_structures`, `formation_threshold`, and `approval_record_id`. | Authority Charter schema test. |
| SIM-REQ-511 | The engine shall store each Scope record with `scope_id`, `function`, `territory`, `population_affected`, `permitted_powers`, `prohibited_powers`, `resource_authority`, `enforcement_authority`, `review_interval`, `emergency_powers`, and `authority_references`. | Scope schema test. |
| SIM-REQ-512 | The engine shall store each Simulation Event with `event_id`, `event_type`, `submitted_tick`, `effective_tick`, `actor_id`, `target_id`, `payload`, `status`, and `provenance`. | Event schema test. |
| SIM-REQ-513 | The engine shall assign a stable `event_id` to every accepted Simulation Event. | Event creation test. |
| SIM-REQ-514 | The engine shall record every rule decision with `decision_id`, `event_id`, `rule_id`, `input_state_hash`, `result`, `reason`, and `decision_tick`. | Rule decision log test. |
| SIM-REQ-515 | The engine shall reject any event whose `event_type` is not defined by the engine or scenario schema. | Invalid event test. |
| SIM-REQ-516 | The engine shall preserve rejected events in the validation report with rejection reason and source provenance. | Invalid event output test. |
| SIM-REQ-517 | The engine shall produce a state hash after each tick. | Replay integrity test. |
| SIM-REQ-518 | The engine shall produce identical state hashes for identical inputs, engine version, and seed. | Deterministic replay test. |

### Approval Record Schema

Approval records are the common input for Authority formation, Authority renewal, National Decisions, amendments, emergency extensions, and governance credit overrides. Approval mechanics remain constrained by `SIM-GAP-002` where the Charter does not yet define denominator, quorum, abstention, or snapshot rules.

| ID | Requirement | Suggested Verification |
| --- | --- | --- |
| SIM-REQ-530 | The engine shall store each Approval Record with `approval_record_id`, `decision_type`, `subject_id`, `electorate_basis`, `eligible_count`, `approval_count`, `rejection_count`, `abstention_count`, `approval_ratio`, `threshold_required`, `threshold_result`, `snapshot_tick`, and `assumptions_used`. | Approval record schema test. |
| SIM-REQ-531 | The engine shall compute `approval_ratio` from approval record counts and declared denominator assumptions. | Approval formula test. |
| SIM-REQ-532 | The engine shall reject an Approval Record whose `approval_count`, `rejection_count`, or `abstention_count` is negative. | Invalid approval record test. |
| SIM-REQ-533 | The engine shall reject an Approval Record whose counted votes exceed `eligible_count` under the declared denominator assumption. | Approval conservation test. |
| SIM-REQ-534 | The engine shall identify the threshold source rule used for `threshold_required`. | Approval traceability test. |
| SIM-REQ-535 | The engine shall mark `threshold_result` as pass only when `approval_ratio` is greater than or equal to `threshold_required`. | Threshold comparison test. |
| SIM-REQ-536 | The engine shall include `assumptions_used` when approval mechanics rely on unresolved Charter denominator, quorum, abstention, or snapshot assumptions. | Gap assumption test. |
| SIM-REQ-537 | The engine shall fail validation when an Approval Record requires unresolved approval assumptions and `assumptions_used` is empty. | Invalid approval scenario test. |
| SIM-REQ-538 | The engine shall preserve the original Approval Record used for each threshold decision in the event log or final state provenance. | Provenance test. |
| SIM-REQ-539 | The engine shall support Approval Record `decision_type` values for `authority_formation`, `authority_renewal`, `national_decision`, `charter_amendment`, `emergency_extension`, and `governance_credit_override`. | Approval decision type validation test. |

### Event Processing Requirements

| ID | Requirement | Suggested Verification |
| --- | --- | --- |
| SIM-REQ-520 | The engine shall process events in ascending `effective_tick` order. | Event ordering test. |
| SIM-REQ-521 | The engine shall process events with the same `effective_tick` using a deterministic priority order. | Same-tick ordering test. |
| SIM-REQ-522 | The deterministic priority order shall be declared in scenario manifest or engine metadata. | Manifest validation test. |
| SIM-REQ-523 | The engine shall transform accepted input events into state changes only through rule decisions. | State transition audit test. |
| SIM-REQ-524 | The engine shall record a no-op rule decision when an accepted event produces no state change. | No-op event test. |
| SIM-REQ-525 | The engine shall expose pre-state and post-state references for each state-changing rule decision. | Audit log test. |
| SIM-REQ-526 | The engine shall complete all event processing for a tick before calculating per-tick metrics. | Metrics timing test. |
| SIM-REQ-527 | The engine shall report unresolved required assumptions before processing the first tick. | Startup validation test. |

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

## 5. Institutional Mechanics

### Rationale

Institutional mechanics are the core of the first useful engine. These requirements translate Charter rules into testable mechanical behavior while leaving unresolved Charter ambiguities explicit.

### Delegation And Representation

| ID | Requirement | Suggested Verification |
| --- | --- | --- |
| SIM-REQ-110 | The engine shall allow Subscribers to create delegation changes. | Delegation creation test. |
| SIM-REQ-111 | The engine shall allow Subscribers to revoke delegation changes. | Revocation test. |
| SIM-REQ-112 | The engine shall allow Subscribers to transfer delegation to another Representative. | Transfer test. |
| SIM-REQ-113 | The engine shall enforce a thirty-day activation delay for delegation changes. | Activation scheduling test. |
| SIM-REQ-114 | The engine shall enforce no more than two delegation changes per Subscriber per twelve-month period. | Frequency limit test. |
| SIM-REQ-115 | The engine shall accept fractional delegation events when enabled by scenario configuration. | Fractional delegation test. |
| SIM-REQ-116 | The engine shall compute delegation weight using `W = R^0.75` when the unresolved normalization assumptions are provided. | Weighting test. |
| SIM-REQ-117 | The engine shall block or flag weighting calculations when required unresolved weighting assumptions are absent. | Gap validation test. |
| SIM-REQ-118 | The engine shall enforce a one-percent raw delegation cap per Representative. | Raw cap test. |
| SIM-REQ-119 | The engine shall enforce a one-percent weighted delegation cap per Representative when weighted totals are computable. | Weighted cap test. |
| SIM-REQ-120 | The engine shall return excess delegation to Subscribers for reassignment. | Excess reassignment test. |
| SIM-REQ-121 | The engine shall apply coalition aggregation for cap purposes when coalition membership is configured. | Coalition cap test. |
| SIM-REQ-122 | The engine shall trigger stabilization when more than five percent of representation tokens are scheduled to activate delegation shifts within a fourteen-day period. | Stabilization trigger test. |
| SIM-REQ-123 | The engine shall uniformly extend affected delegation activation dates by thirty days when stabilization triggers. | Stabilization extension test. |
| SIM-REQ-124 | The engine shall log stabilization extensions. | Event log test. |
| SIM-REQ-125 | The engine shall convert an accepted `delegation_create` event into a pending Delegation record in the same tick. | Delegation state transition test. |
| SIM-REQ-126 | The engine shall convert a pending Delegation record into active status at `activation_tick` unless blocked by cap, change-frequency, stabilization, or review rules. | Delegation activation test. |
| SIM-REQ-127 | The engine shall record the exact blocking rule when a pending Delegation does not activate on `activation_tick`. | Blocked activation log test. |
| SIM-REQ-128 | The engine shall set revoked Delegation records to inactive status and preserve their history. | Revocation state test. |
| SIM-REQ-129 | The engine shall recalculate Representative raw and weighted totals after each delegation activation, revocation, transfer, or cap reassignment. | Delegation total recalculation test. |

### Authority Lifecycle

| ID | Requirement | Suggested Verification |
| --- | --- | --- |
| SIM-REQ-130 | The engine shall require an Authority Charter before Authority activation. | Charter validation test. |
| SIM-REQ-131 | The engine shall require Authority Charters to include scope, funding sources, renewal process, and oversight structures. | Schema validation test. |
| SIM-REQ-132 | The engine shall apply a seventy-five-percent approval threshold to coercive Authority formation. | Threshold test. |
| SIM-REQ-133 | The engine shall apply a sixty-percent approval threshold to non-coercive Authority formation. | Threshold test. |
| SIM-REQ-134 | The engine shall treat coercive classification criteria as a configuration requirement until the Charter defines a full test. | Gap validation test. |
| SIM-REQ-135 | The engine shall mark out-of-scope Authority actions void in simulation state. | Scope invalidation test. |
| SIM-REQ-136 | The engine shall require full rechartering for Authority scope expansion. | Rechartering test. |
| SIM-REQ-137 | The engine shall require full rechartering for Authority scope transfer. | Rechartering test. |
| SIM-REQ-138 | The engine shall process Authority dissolution according to configured Authority Charter procedures. | Dissolution test. |
| SIM-REQ-139 | The engine shall schedule structural and performance review every five years for each Authority. | Review scheduling test. |
| SIM-REQ-140 | The engine shall require simple majority approval of Subscribers within Authority scope for renewal. | Renewal test. |
| SIM-REQ-141 | The engine shall trigger mandatory reauthorization review after twelve consecutive months below forty-percent satisfaction. | Satisfaction trigger test. |
| SIM-REQ-142 | The engine shall label satisfaction metric rules as simulation abstractions until the Charter defines measurement mechanics. | Manifest review. |
| SIM-REQ-143 | The engine shall accept Authority formation requests with `proposed_authority_id`, `charter_id`, `coercive_status`, `approval_record_id`, and `submitted_tick`. | Formation event schema test. |
| SIM-REQ-144 | The engine shall approve Authority formation only when the approval record meets the threshold selected by `coercive_status`. | Formation threshold test. |
| SIM-REQ-145 | The engine shall reject Authority formation when the Authority Charter fails required-field validation. | Formation rejection test. |
| SIM-REQ-146 | The engine shall emit an Authority activation event when a formation request passes charter and threshold validation. | Activation event test. |
| SIM-REQ-147 | The engine shall emit an Authority formation rejection event when a formation request fails validation. | Rejection event test. |
| SIM-REQ-148 | The engine shall store Authority lifecycle transitions as append-only events. | Lifecycle history test. |
| SIM-REQ-149 | The engine shall produce a reauthorization decision event with approval percentage, electorate basis, result, and next review tick. | Reauthorization output test. |

### Authority Lifecycle State Machine

The first-pass engine uses a formal state machine for Authority lifecycle behavior. State names are simulation state labels for testing Charter mechanics; they do not create additional Charter powers.

| State | Meaning |
| --- | --- |
| `proposed` | Authority formation has been requested but not approved. |
| `rejected` | Authority formation failed validation or threshold approval. |
| `chartered` | Authority formation passed threshold and charter validation but is not yet active. |
| `active` | Authority may submit actions within sealed scope. |
| `under_review` | Authority is undergoing scheduled, mandatory, court, or consolidation review. |
| `reauthorization_required` | Authority requires renewal or reauthorization before normal continuation. |
| `suspended` | Authority is temporarily unable to execute configured actions due to review, emergency review, or scenario-defined court order. |
| `dissolving` | Authority has entered dissolution process under its Authority Charter or consolidation order. |
| `dissolved` | Authority no longer executes actions. |
| `merged` | Authority has been merged into another Authority through a valid process. |
| `separated` | Authority has been split into successor Authorities through a valid process. |

| ID | Requirement | Suggested Verification |
| --- | --- | --- |
| SIM-REQ-550 | The engine shall store Authority lifecycle state as one of the formal state machine values. | Lifecycle enum validation test. |
| SIM-REQ-551 | The engine shall allow transition from `proposed` to `chartered` only after formation threshold and Authority Charter validation pass. | Lifecycle transition test. |
| SIM-REQ-552 | The engine shall allow transition from `proposed` to `rejected` when formation threshold or Authority Charter validation fails. | Lifecycle transition test. |
| SIM-REQ-553 | The engine shall allow transition from `chartered` to `active` only through an Authority activation event. | Activation transition test. |
| SIM-REQ-554 | The engine shall allow transition from `active` to `under_review` when a scheduled review, mandatory review, court review, or consolidation review event is accepted. | Review transition test. |
| SIM-REQ-555 | The engine shall allow transition from `under_review` to `active` when review passes without requiring reauthorization, suspension, dissolution, merger, or separation. | Review outcome test. |
| SIM-REQ-556 | The engine shall allow transition from `under_review` to `reauthorization_required` when renewal or mandatory reauthorization is required. | Review outcome test. |
| SIM-REQ-557 | The engine shall allow transition from `reauthorization_required` to `active` only when a valid reauthorization Approval Record passes. | Reauthorization transition test. |
| SIM-REQ-558 | The engine shall allow transition from `reauthorization_required` to `dissolving` when reauthorization fails and configured dissolution procedures require dissolution. | Reauthorization failure test. |
| SIM-REQ-559 | The engine shall allow transition from `active` or `under_review` to `suspended` only through a review or court decision event. | Suspension transition test. |
| SIM-REQ-560 | The engine shall allow transition from `suspended` to `active` only through a review or court decision event. | Suspension release test. |
| SIM-REQ-561 | The engine shall allow transition to `dissolving` only from `active`, `under_review`, `reauthorization_required`, or `suspended`. | Dissolution transition test. |
| SIM-REQ-562 | The engine shall allow transition from `dissolving` to `dissolved` only after configured dissolution procedures complete. | Dissolution completion test. |
| SIM-REQ-563 | The engine shall allow transition from `active`, `under_review`, or `dissolving` to `merged` only through a valid merger event. | Merger transition test. |
| SIM-REQ-564 | The engine shall allow transition from `active`, `under_review`, or `dissolving` to `separated` only through a valid separation event. | Separation transition test. |
| SIM-REQ-565 | The engine shall reject lifecycle transitions not listed in this state machine unless a future requirement explicitly adds them. | Invalid transition test. |
| SIM-REQ-566 | Each lifecycle transition event shall include `authority_id`, `from_state`, `to_state`, `trigger_event_id`, `decision_id`, and `transition_tick`. | Lifecycle event schema test. |
| SIM-REQ-567 | The engine shall prevent Authorities in `proposed`, `rejected`, `chartered`, `suspended`, `dissolving`, `dissolved`, `merged`, or `separated` states from executing ordinary Authority actions. | State action gating test. |
| SIM-REQ-568 | The engine shall allow Authorities in `under_review` to execute ordinary actions only when the review decision or scenario configuration explicitly permits continued operation. | Review action gating test. |

### Emergency Mechanics

| ID | Requirement | Suggested Verification |
| --- | --- | --- |
| SIM-REQ-150 | The engine shall allow emergency declaration only for configured threats to life, essential infrastructure, security, or governance continuity. | Emergency validation test. |
| SIM-REQ-151 | The engine shall allow a Lead Emergency Authority to exercise emergency powers for thirty days after a qualifying declaration. | Emergency duration test. |
| SIM-REQ-152 | The engine shall require approval by all affected Authorities for extension to ninety days. | Extension test. |
| SIM-REQ-153 | The engine shall require National Decision approval for extension beyond one year. | Long extension test. |
| SIM-REQ-154 | The engine shall require emergency measures to be publicly posted within seven days. | Deadline test. |
| SIM-REQ-155 | The engine shall expire emergency powers when the emergency ends. | Expiration test. |
| SIM-REQ-156 | The engine shall process provisional emergency measures for no more than seventy-two hours. | Provisional activation test. |
| SIM-REQ-157 | The engine shall require immediate ECO and Charter Court notification for provisional measures. | Notification event test. |
| SIM-REQ-158 | The engine shall subject emergency actions to configured Charter Court review for Articles XVI and XVII compliance. | Review scenario test. |
| SIM-REQ-159 | The engine shall reject emergency declarations whose `qualifying_condition` is not one of the Charter-recognized emergency categories. | Invalid emergency test. |
| SIM-REQ-160 | The engine shall store emergency declarations with `emergency_id`, `lead_authority_id`, `qualifying_condition`, `start_tick`, `scheduled_expiry_tick`, `affected_authority_ids`, and `publication_due_tick`. | Emergency record schema test. |
| SIM-REQ-161 | The engine shall emit an emergency expiry event at `scheduled_expiry_tick` unless a valid extension event exists. | Emergency expiry test. |
| SIM-REQ-162 | The engine shall reject an emergency extension event that lacks required affected-Authority approvals. | Extension rejection test. |
| SIM-REQ-163 | The engine shall record whether emergency publication occurred before `publication_due_tick`. | Publication deadline test. |
| SIM-REQ-164 | The engine shall flag late emergency publication as a reviewable violation event. | Late publication test. |

### Conflict, Consolidation, And Review

| ID | Requirement | Suggested Verification |
| --- | --- | --- |
| SIM-REQ-170 | The engine shall detect scope conflicts from incompatible Authority scope claims. | Conflict detection test. |
| SIM-REQ-171 | The engine shall assign scope conflicts to a randomly selected Coordination Council for no more than twelve months. | Council scheduling test. |
| SIM-REQ-172 | The engine shall apply higher Subscriber approval majority as the first harmonization rule for conflicting Legislative Acts. | Harmonization test. |
| SIM-REQ-173 | The engine shall apply narrower functional scope as the tie-breaker when approval majorities are equal. | Tie-break test. |
| SIM-REQ-174 | The engine shall allow Charter Court harmonization orders for up to twelve months when functional boundaries cannot be determined. | Court order duration test. |
| SIM-REQ-175 | The engine shall apply territorial fallback only to physical operations. | Territorial fallback test. |
| SIM-REQ-176 | The engine shall schedule a consolidation audit every ten years. | Audit scheduling test. |
| SIM-REQ-177 | The engine shall calculate Authority sprawl against the one-Authority-per-fifty-thousand-Subscribers governance credit limit. | Sprawl metric test. |
| SIM-REQ-178 | The engine shall process National Decision override events for the governance credit limit. | Override test. |
| SIM-REQ-179 | The engine shall process Consolidation Conflict Authority decision events for configured consolidation disputes. | CCA scenario test. |
| SIM-REQ-180 | The engine shall prevent CCA decisions from modifying Charter text, Legislative Acts, funding levels, or expanding Authority scope. | CCA validation test. |
| SIM-REQ-181 | The engine shall store each scope conflict with `conflict_id`, `authority_ids`, `scope_ids`, `conflict_basis`, `detected_tick`, and `resolution_status`. | Conflict record schema test. |
| SIM-REQ-182 | The engine shall emit a Coordination Council selection event with seed-derived selection provenance. | Council selection replay test. |
| SIM-REQ-183 | The engine shall emit a conflict resolution event with applied rule, winning authority or act if any, expiry tick if temporary, and unresolved status if no rule resolves it. | Conflict resolution output test. |
| SIM-REQ-184 | The engine shall store each consolidation audit with `audit_id`, `scheduled_tick`, `authority_count`, `subscriber_count`, `governance_credit_limit`, `sprawl_result`, and `recommended_actions`. | Audit record schema test. |
| SIM-REQ-185 | The engine shall emit CCA order events with `order_type`, `authority_ids`, `permitted_action_check`, and appeal window if configured. | CCA order event test. |
| SIM-REQ-186 | The engine shall reject CCA order events whose `order_type` is outside the Charter-derived permitted order list. | CCA invalid order test. |

### First-Pass Scope Conflict Detection Mechanics

First-pass conflict detection is structural. It compares machine-readable scope and action records; it does not interpret natural-language legal text.

| ID | Requirement | Suggested Verification |
| --- | --- | --- |
| SIM-REQ-570 | The engine shall evaluate scope conflict whenever an Authority action event is accepted. | Conflict trigger test. |
| SIM-REQ-571 | The engine shall evaluate scope conflict whenever a new Authority becomes active. | Activation conflict test. |
| SIM-REQ-572 | The engine shall evaluate scope conflict whenever an Authority scope changes through valid rechartering, merger, separation, or consolidation order. | Scope change conflict test. |
| SIM-REQ-573 | The engine shall compare scope conflicts using `function`, `territory`, `population_affected`, `permitted_powers`, `prohibited_powers`, `resource_authority`, and `enforcement_authority`. | Conflict comparison test. |
| SIM-REQ-574 | The engine shall detect a functional conflict when two active Authorities claim incompatible permitted powers over the same configured function. | Functional conflict test. |
| SIM-REQ-575 | The engine shall detect a territorial conflict when two active Authorities issue incompatible physical-operation directives over overlapping territory. | Territorial conflict test. |
| SIM-REQ-576 | The engine shall detect a population conflict when two active Authorities issue incompatible directives affecting overlapping configured populations. | Population conflict test. |
| SIM-REQ-577 | The engine shall detect a resource conflict when two active Authorities claim exclusive use of the same configured resource. | Resource conflict test. |
| SIM-REQ-578 | The engine shall detect an enforcement conflict when an Authority action uses enforcement authority not present in that Authority scope. | Enforcement conflict test. |
| SIM-REQ-579 | The engine shall detect a prohibited-power conflict when an Authority action requests a power listed in that Authority scope `prohibited_powers`. | Prohibited power test. |
| SIM-REQ-580 | The engine shall classify each detected scope conflict as `functional`, `territorial`, `population`, `resource`, `enforcement`, `prohibited_power`, or `mixed`. | Conflict classification test. |
| SIM-REQ-581 | The engine shall mark a conflict as `mixed` when more than one conflict classification applies. | Mixed conflict test. |
| SIM-REQ-582 | The engine shall not mark overlap alone as conflict unless configured incompatibility, exclusivity, prohibited power, or incompatible directive criteria are present. | Benign overlap test. |
| SIM-REQ-583 | The engine shall represent territory overlap using scenario-defined territory identifiers or geometry abstraction. | Territory overlap test. |
| SIM-REQ-584 | The engine shall represent population overlap using scenario-defined population group identifiers or membership sets. | Population overlap test. |
| SIM-REQ-585 | The engine shall represent incompatible directives using scenario-defined directive types and incompatibility matrix. | Incompatibility matrix test. |
| SIM-REQ-586 | The engine shall label the incompatibility matrix as a simulation abstraction unless derived directly from a Charter rule. | Manifest review. |
| SIM-REQ-587 | The engine shall emit exactly one scope conflict event for each unique conflict key per tick. | Duplicate conflict test. |
| SIM-REQ-588 | The unique conflict key shall include sorted Authority IDs, conflict classification, affected scope identifiers, and tick. | Conflict key test. |
| SIM-REQ-589 | The engine shall preserve unresolved scope conflicts until a resolution event, expiry event, or scenario termination. | Conflict persistence test. |

## 6. Machine-Readable Scope Model

### Rationale

Authority scope is the main boundary mechanism in the Charter. The engine needs a structured representation that can be checked mechanically. This representation is a simulation representation of Charter scope, not new legal text.

### Requirements

| ID | Requirement | Suggested Verification |
| --- | --- | --- |
| SIM-REQ-190 | The engine shall require each Authority scope model to identify a function. | Scope schema validation test. |
| SIM-REQ-191 | The engine shall allow each Authority scope model to identify territory when territory is relevant. | Territory scenario test. |
| SIM-REQ-192 | The engine shall allow each Authority scope model to identify the population affected. | Population scope test. |
| SIM-REQ-193 | The engine shall require each Authority scope model to list permitted powers. | Scope schema validation test. |
| SIM-REQ-194 | The engine shall allow each Authority scope model to list prohibited powers. | Prohibited-power test. |
| SIM-REQ-195 | The engine shall allow each Authority scope model to specify resource authority. | Resource constraint test. |
| SIM-REQ-196 | The engine shall allow each Authority scope model to specify enforcement authority. | Enforcement scope test. |
| SIM-REQ-197 | The engine shall require each Authority scope model to specify review interval or inherit the Charter five-year default. | Review interval test. |
| SIM-REQ-198 | The engine shall allow each Authority scope model to specify emergency powers. | Emergency scope test. |
| SIM-REQ-199 | The engine shall allow each Authority scope model to specify parent or peer Authority references when compacts, overlaps, or dependencies are configured. | Reference validation test. |
| SIM-REQ-200 | The engine shall identify the scope model as a simulation representation in output manifests. | Manifest review. |

Suggested minimum scope fields:

| Field | Required | Notes |
| --- | --- | --- |
| `function` | Yes | Functional domain governed by the Authority. |
| `territory` | Conditional | Required for territorial scenarios. |
| `population_affected` | Conditional | Required when decisions depend on scoped electorate or satisfaction. |
| `permitted_powers` | Yes | Enumerated powers. |
| `prohibited_powers` | No | Explicit exclusions for tests. |
| `resource_authority` | No | Budget, assets, or operational resources. |
| `enforcement_authority` | No | Aligns with coercive classification. |
| `review_interval` | No | Defaults to five years. |
| `emergency_powers` | No | Constrained by Article V mechanics. |
| `authority_references` | No | Parent, peer, compact, overlap, or dependency references. |

## 7. Simulation Time Model

### Rationale

The Charter uses days, months, years, review intervals, activation delays, emergency deadlines, and audit cycles. A discrete time model is required for reproducibility.

### Requirements

| ID | Requirement | Suggested Verification |
| --- | --- | --- |
| SIM-REQ-210 | The engine shall use discrete ticks. | Tick test. |
| SIM-REQ-211 | The engine shall map each tick to a configured calendar duration. | Calendar mapping test. |
| SIM-REQ-212 | The first-pass default tick duration shall be one day. | Default config test. |
| SIM-REQ-213 | The engine shall schedule future events by tick and calendar date. | Event scheduling test. |
| SIM-REQ-214 | The engine shall schedule review windows with start tick, end tick, and review type. | Review window test. |
| SIM-REQ-215 | The engine shall schedule delegation activation delays with submitted tick and activation tick. | Delegation schedule test. |
| SIM-REQ-216 | The engine shall schedule emergency deadlines with deadline type and due tick. | Emergency deadline test. |
| SIM-REQ-217 | The engine shall calculate reporting periods for metrics from configured period boundaries. | Metrics period test. |
| SIM-REQ-218 | The engine shall preserve event ordering within a tick according to a deterministic ordering rule. | Replay ordering test. |

## 8. Scenario Configuration

### Rationale

Scenario files define initial conditions and behavior parameters without changing engine code. YAML or JSON are acceptable because both can be versioned and diffed.

### Requirements

| ID | Requirement | Suggested Verification |
| --- | --- | --- |
| SIM-REQ-230 | The engine shall load scenario configuration from YAML or JSON. | Config loading test. |
| SIM-REQ-231 | Scenario configuration shall include population size. | Schema validation test. |
| SIM-REQ-232 | Scenario configuration shall include agent distributions. | Schema validation test. |
| SIM-REQ-233 | Scenario configuration shall allow initial delegations. | Initialization test. |
| SIM-REQ-234 | Scenario configuration shall allow initial Authorities. | Initialization test. |
| SIM-REQ-235 | Scenario configuration shall allow geography or territory model configuration. | Territory scenario test. |
| SIM-REQ-236 | Scenario configuration shall allow an event schedule. | Event scheduling test. |
| SIM-REQ-237 | Scenario configuration shall allow adversarial behavior settings. | Adversarial scenario test. |
| SIM-REQ-238 | Scenario configuration shall require a random seed. | Validation test. |
| SIM-REQ-239 | Scenario configuration shall require simulation duration. | Validation test. |
| SIM-REQ-240 | Scenario configuration shall include output settings. | Output test. |
| SIM-REQ-241 | Scenario configuration shall include a scenario schema version. | Manifest validation test. |
| SIM-REQ-242 | Scenario configuration shall identify any simulation abstractions used by the scenario. | Manifest validation test. |
| SIM-REQ-243 | Scenario configuration shall include `scenario_id`, `scenario_version`, `charter_derivative_path`, `random_seed`, `duration`, `tick_duration`, and `output_path`. | Scenario schema validation test. |
| SIM-REQ-244 | Scenario configuration shall include agent configuration sections for every enabled agent type. | Scenario schema validation test. |
| SIM-REQ-245 | Scenario configuration shall fail validation when an enabled agent type lacks required state or behavior parameters. | Invalid scenario test. |
| SIM-REQ-246 | Scenario configuration shall include initial state records or generation rules for Subscribers, Representatives, Authorities, and Delegations. | Initialization validation test. |
| SIM-REQ-247 | Scenario configuration shall declare any assumptions used to resolve `SIM-GAP-*` items. | Gap assumption validation test. |
| SIM-REQ-248 | Scenario configuration shall fail validation when a scenario requires an unresolved `SIM-GAP-*` assumption that is not declared. | Invalid scenario test. |

## 9. Engine Determinism And Reproducibility

### Rationale

Stress tests are only useful if outcomes can be reproduced, audited, and traced to rule decisions.

### Requirements

| ID | Requirement | Suggested Verification |
| --- | --- | --- |
| SIM-REQ-250 | The engine shall require random seed control for every run. | Config validation test. |
| SIM-REQ-251 | The engine shall produce deterministic replay for identical inputs, engine version, and random seed. | Replay test. |
| SIM-REQ-252 | The engine shall include versioned scenario inputs in run provenance. | Manifest test. |
| SIM-REQ-253 | The engine shall include Charter derivative version metadata in run provenance. | Manifest test. |
| SIM-REQ-254 | The engine shall log rule decisions. | Event log review. |
| SIM-REQ-255 | Each logged rule decision shall include input reference, rule reference, decision result, and timestamp. | Event schema test. |
| SIM-REQ-256 | The engine shall export an event log. | Output test. |
| SIM-REQ-257 | The engine shall report validation errors before running invalid scenarios. | Invalid scenario test. |
| SIM-REQ-258 | The engine shall not use unseeded randomness. | Static and replay tests. |
| SIM-REQ-259 | The engine shall include a hash of the scenario configuration in the scenario manifest. | Manifest test. |
| SIM-REQ-260 | The engine shall include a hash of `charter_sim.yaml` in the scenario manifest. | Manifest test. |
| SIM-REQ-261 | The engine shall include engine package version and Mesa adapter version in run provenance when available. | Manifest test. |
| SIM-REQ-262 | The engine shall include random seed, tick duration, start tick, end tick, and event ordering policy in run provenance. | Manifest test. |
| SIM-REQ-263 | The engine shall fail deterministic replay if final state hash differs from the recorded final state hash. | Replay failure test. |

## 10. Metrics And Outputs

### Rationale

The first pass needs metrics that expose mechanical stress points: concentration, churn, load, sprawl, conflict, emergency duration, capture attempts, and review outcomes.

### Required Metrics

| ID | Requirement | Suggested Verification |
| --- | --- | --- |
| SIM-REQ-270 | The engine shall measure power concentration by raw delegation share. | Metrics unit test. |
| SIM-REQ-271 | The engine shall measure power concentration by weighted delegation share when weighting is configured. | Metrics unit test. |
| SIM-REQ-272 | The engine shall measure delegation churn. | Metrics unit test. |
| SIM-REQ-273 | The engine shall measure Authority count. | Metrics unit test. |
| SIM-REQ-274 | The engine shall measure Authority sprawl against the governance credit limit. | Metrics unit test. |
| SIM-REQ-275 | The engine shall measure scope conflict count. | Metrics unit test. |
| SIM-REQ-276 | The engine shall measure emergency action count. | Metrics unit test. |
| SIM-REQ-277 | The engine shall measure emergency action duration. | Metrics unit test. |
| SIM-REQ-278 | The engine shall measure court or review load. | Metrics unit test. |
| SIM-REQ-279 | The engine shall measure satisfaction by configured population group. | Metrics unit test. |
| SIM-REQ-280 | The engine shall measure capture attempts. | Metrics unit test. |
| SIM-REQ-281 | The engine shall measure capture attempt success rate using scenario-defined success criteria. | Metrics unit test. |
| SIM-REQ-282 | The engine shall measure reauthorization outcomes. | Metrics unit test. |
| SIM-REQ-283 | The engine shall measure dissolution outcomes. | Metrics unit test. |
| SIM-REQ-284 | The engine shall measure time-to-response after crisis events. | Metrics unit test. |
| SIM-REQ-285 | The engine shall measure rights violation events as simulation abstractions. | Metrics and manifest test. |
| SIM-REQ-286 | The engine shall measure scope violation events as simulation abstractions unless directly determined by scope rules. | Metrics and manifest test. |

### Metric Formula Requirements

Metric formulas are first-pass engineering definitions for simulation outputs. They do not define Charter legal standards.

| Metric | First-Pass Formula |
| --- | --- |
| Raw power concentration | `max_representative_raw_delegation_share = max(raw_delegation_total) / total_active_representation_tokens` |
| Weighted power concentration | `max_representative_weighted_share = max(weighted_delegation_total) / total_weighted_delegation` |
| Delegation churn | `delegation_churn = count(delegation_create, delegation_revoke, delegation_transfer events in window) / active_subscriber_count` |
| Authority count | `authority_count = count(Authority records where lifecycle_status in active_counted_states)` |
| Authority sprawl | `authority_sprawl_ratio = authority_count / floor(active_subscriber_count / 50000)` when denominator is greater than zero |
| Scope conflict count | `scope_conflict_count = count(scope_conflict events in window)` |
| Emergency action count | `emergency_action_count = count(emergency_declaration, emergency_extension, provisional_emergency events in window)` |
| Emergency action duration | `emergency_duration_ticks = emergency_end_tick - emergency_start_tick` |
| Court or review load | `review_load = count(review_request events pending or processed in window)` |
| Satisfaction by group | `group_satisfaction_mean = sum(satisfaction_value for group members) / group_member_count` |
| Capture attempts | `capture_attempt_count = count(capture_attempt events in window)` |
| Capture success rate | `capture_success_rate = successful_capture_attempt_count / capture_attempt_count` when attempts are greater than zero |
| Reauthorization outcomes | `reauthorization_pass_rate = passed_reauthorization_count / total_reauthorization_decisions` when decisions are greater than zero |
| Dissolution outcomes | `dissolution_count = count(Authority lifecycle transitions to dissolved in window)` |
| Time-to-response after crisis | `time_to_response_ticks = first_valid_response_tick - crisis_start_tick` |
| Rights violation events | `rights_violation_count = count(rights_violation events in window)` |
| Scope violation events | `scope_violation_count = count(scope_violation or prohibited_power conflict events in window)` |

| ID | Requirement | Suggested Verification |
| --- | --- | --- |
| SIM-REQ-590 | The engine shall calculate raw power concentration using the first-pass raw power concentration formula. | Metric formula test. |
| SIM-REQ-591 | The engine shall calculate weighted power concentration using the first-pass weighted power concentration formula when weighting is configured. | Metric formula test. |
| SIM-REQ-592 | The engine shall return `not_applicable` for weighted power concentration when weighting assumptions are unresolved. | Metric gap test. |
| SIM-REQ-593 | The engine shall calculate delegation churn using the first-pass delegation churn formula. | Metric formula test. |
| SIM-REQ-594 | The engine shall calculate Authority count using configured active-counted lifecycle states. | Metric formula test. |
| SIM-REQ-595 | The first-pass active-counted lifecycle states shall include `active`, `under_review`, `reauthorization_required`, and `suspended`. | Metric configuration test. |
| SIM-REQ-596 | The engine shall calculate Authority sprawl using the first-pass Authority sprawl formula. | Metric formula test. |
| SIM-REQ-597 | The engine shall return `not_applicable` for Authority sprawl when active Subscriber count is below fifty-thousand unless scenario configuration defines a small-population scaling abstraction. | Metric edge case test. |
| SIM-REQ-598 | The engine shall calculate scope conflict count using unique scope conflict events. | Metric formula test. |
| SIM-REQ-599 | The engine shall calculate emergency duration from emergency start and end ticks. | Metric formula test. |
| SIM-REQ-600 | The engine shall calculate court or review load from review queue and review decision events. | Metric formula test. |
| SIM-REQ-601 | The engine shall calculate satisfaction by group only for groups declared in scenario configuration. | Metric formula test. |
| SIM-REQ-602 | The engine shall calculate capture success rate using scenario-defined success criteria. | Metric formula test. |
| SIM-REQ-603 | The engine shall return `not_applicable` for capture success rate when no capture attempts occur. | Metric edge case test. |
| SIM-REQ-604 | The engine shall calculate time-to-response only when a crisis event and valid response event are linked by event references. | Metric formula test. |
| SIM-REQ-605 | Each metric output shall include `metric_id`, `formula_id`, `window_start_tick`, `window_end_tick`, `value`, `unit`, and `not_applicable_reason` when applicable. | Metric output schema test. |
| SIM-REQ-606 | Each metric formula shall be listed in the scenario manifest or engine metadata. | Manifest test. |

### Required Output Artifacts

| ID | Requirement | Suggested Verification |
| --- | --- | --- |
| SIM-REQ-290 | Each run shall output an event log. | Output existence test. |
| SIM-REQ-291 | Each run shall output final state. | Output existence test. |
| SIM-REQ-292 | Each run shall output metrics summary. | Output existence test. |
| SIM-REQ-293 | Each run shall output per-tick time series. | Output existence test. |
| SIM-REQ-294 | Each run shall output scenario manifest. | Output existence test. |
| SIM-REQ-295 | Each run shall output validation and errors report. | Output existence test. |
| SIM-REQ-296 | Output artifacts shall include enough provenance to reproduce the run. | Replay provenance test. |
| SIM-REQ-297 | The event log shall contain one row or object per accepted, rejected, generated, or derived event. | Event log schema test. |
| SIM-REQ-298 | The final state artifact shall include Subscribers, Representatives, Delegations, Authorities, active emergencies, pending reviews, and unresolved conflicts. | Final state schema test. |
| SIM-REQ-299 | The metrics summary shall include metric name, value, unit, calculation window, and calculation source. | Metrics summary schema test. |
| SIM-REQ-300 | The per-tick time series shall include tick, calendar date, metric name, and value. | Time series schema test. |
| SIM-REQ-301 | The validation and errors report shall distinguish blocking errors, non-blocking warnings, and simulation abstraction notices. | Validation report test. |

## 11. First-Pass Scenario Suite

### Rationale

The starter suite exercises high-value Charter mechanics without requiring high-fidelity social modeling.

### Requirements

| ID | Requirement | Suggested Verification |
| --- | --- | --- |
| SIM-REQ-310 | The scenario suite shall include a Basic Delegation Stability scenario. | Scenario manifest review. |
| SIM-REQ-311 | The Basic Delegation Stability scenario shall test delegation activation delay, change limits, caps, and churn metrics. | Scenario acceptance test. |
| SIM-REQ-312 | The scenario suite shall include an Authority Creation And Reauthorization scenario. | Scenario manifest review. |
| SIM-REQ-313 | The Authority Creation And Reauthorization scenario shall test formation threshold, activation, five-year review, and renewal. | Scenario acceptance test. |
| SIM-REQ-314 | The scenario suite shall include a Local Coercive Authority or Neighborhood Patrol scenario. | Scenario manifest review. |
| SIM-REQ-315 | The Local Coercive Authority or Neighborhood Patrol scenario shall test coercive threshold, territorial scope, enforcement powers, and scoped-electorate gap handling. | Scenario acceptance test. |
| SIM-REQ-316 | The scenario suite shall include an Emergency Power Expiration And Review scenario. | Scenario manifest review. |
| SIM-REQ-317 | The Emergency Power Expiration And Review scenario shall test provisional activation, thirty-day duration, extension, publication, expiry, and review. | Scenario acceptance test. |
| SIM-REQ-318 | The scenario suite shall include a Scope Conflict Between Overlapping Authorities scenario. | Scenario manifest review. |
| SIM-REQ-319 | The Scope Conflict scenario shall test Coordination Council assignment, harmonization rule, territorial fallback, and Charter Court order duration. | Scenario acceptance test. |
| SIM-REQ-320 | The scenario suite shall include an Authority Sprawl And Consolidation Audit scenario. | Scenario manifest review. |
| SIM-REQ-321 | The Authority Sprawl scenario shall test governance credit limit, audit scheduling, CCA constraints, and dissolution or merger outcomes. | Scenario acceptance test. |
| SIM-REQ-322 | The scenario suite shall include an Adversarial Capture Attempt scenario. | Scenario manifest review. |
| SIM-REQ-323 | The Adversarial Capture Attempt scenario shall test coordinated delegation shifts, cap enforcement, stabilization, coalition aggregation, and capture metrics. | Scenario acceptance test. |
| SIM-REQ-324 | The scenario suite shall include a Public Dissatisfaction And Delegation Migration scenario. | Scenario manifest review. |
| SIM-REQ-325 | The Public Dissatisfaction scenario shall test satisfaction-triggered review, delegation migration, reauthorization, and review load. | Scenario acceptance test. |

## 12. Non-Goals For First Pass

### Rationale

Explicit exclusions prevent the first implementation from absorbing speculative or high-complexity features before the mechanical Charter layer is testable.

### Requirements

| ID | Requirement | Suggested Verification |
| --- | --- | --- |
| SIM-REQ-330 | The first pass shall not perform real-world election prediction. | Documentation review. |
| SIM-REQ-331 | The first pass shall not model high-fidelity sociology. | Documentation review. |
| SIM-REQ-332 | The first pass shall not use full LLM deliberation as a required component. | Dependency and design review. |
| SIM-REQ-333 | The first pass shall not include economic simulation beyond simple configured resource constraints. | Scenario schema review. |
| SIM-REQ-334 | The first pass shall not perform legal natural-language interpretation. | Design review. |
| SIM-REQ-335 | The first pass shall not make predictive claims about real populations. | Output text review. |
| SIM-REQ-336 | The first pass shall not add new Charter powers except as explicitly labeled simulation abstractions. | Rule and scenario review. |

## 13. Mesa Integration Boundary

### Rationale

Mesa provides the agent-based runtime, not the constitutional interpreter. Keeping the boundary narrow makes the engine testable and allows future replacement or alternate runtimes.

### Requirements

| ID | Requirement | Suggested Verification |
| --- | --- | --- |
| SIM-REQ-350 | The Mesa adapter shall consume initialized engine state. | Adapter initialization test. |
| SIM-REQ-351 | The Mesa adapter shall create Mesa agents from scenario configuration. | Adapter initialization test. |
| SIM-REQ-352 | The Mesa adapter shall coordinate model step order without duplicating Charter rule logic. | Adapter code review and unit test. |
| SIM-REQ-353 | Mesa agents shall call engine services for Charter-constrained decisions. | Mock engine interaction test. |
| SIM-REQ-354 | The Mesa adapter shall collect metrics from engine state and agent state. | Metrics integration test. |
| SIM-REQ-355 | The Mesa adapter shall use seeded random selection for lot-selected bodies and stochastic scenario behavior. | Replay test. |

## 14. Initial Folder Structure

### Rationale

The folder structure separates documentation, rules configuration, pure engine code, Mesa integration, and tests.

### Requirements

| ID | Requirement | Suggested Verification |
| --- | --- | --- |
| SIM-REQ-360 | The executable simulation package shall live under `simulation/src/jefferson_sim/`. | Repository structure review. |
| SIM-REQ-361 | Pure Charter mechanics shall live under `simulation/src/jefferson_sim/engine/`. | Repository structure review. |
| SIM-REQ-362 | Mesa integration shall live under `simulation/src/jefferson_sim/mesa_adapter/`. | Repository structure review. |
| SIM-REQ-363 | Simulation tests shall live under `simulation/tests/`. | Repository structure review. |
| SIM-REQ-364 | Charter-derived YAML and schema artifacts shall remain under `derivatives/simulation/`. | Repository structure review. |

Current intended structure:

```text
simulation/
├── README.md
├── src/
│   └── jefferson_sim/
│       ├── __init__.py
│       ├── engine/
│       │   └── __init__.py
│       └── mesa_adapter/
│           └── __init__.py
└── tests/
    └── README.md
```

## 15. Phased Compliance Plan

### Rationale

The user-specified workflow requires testable design requirements, code that complies with requirements, and tests that prove compliance. This document is Phase 1 for the simulation engine.

### Requirements

| ID | Requirement | Suggested Verification |
| --- | --- | --- |
| SIM-REQ-370 | Phase 1 shall define testable requirements before implementation. | Requirements review. |
| SIM-REQ-371 | Phase 2 shall implement a pure rules engine before Mesa-specific behavior. | Implementation review. |
| SIM-REQ-372 | Phase 3 shall implement the Mesa adapter against the engine interface. | Adapter tests. |
| SIM-REQ-373 | Phase 4 shall implement scenario tests and compliance review. | Test suite review. |
| SIM-REQ-374 | Any intermediate gap list created during implementation shall be closed into the open questions section or resolved before phase completion. | Phase closeout review. |

## 16. Acceptance Criteria

### Requirements Document Acceptance

| ID | Criterion | Suggested Verification |
| --- | --- | --- |
| SIM-REQ-390 | This document shall define atomic, testable, traceable requirements. | Requirements review. |
| SIM-REQ-391 | This document shall include rationale for each major requirement group. | Requirements review. |
| SIM-REQ-392 | This document shall include suggested verification methods. | Requirements review. |
| SIM-REQ-393 | This document shall identify simulation abstractions. | Requirements review. |
| SIM-REQ-394 | This document shall include open questions for Charter ambiguities that block implementation. | Requirements review. |

### Future First Implementation Acceptance

| ID | Criterion | Suggested Verification |
| --- | --- | --- |
| SIM-REQ-400 | The first implementation shall pass unit tests for each implemented rules-engine requirement. | Test suite. |
| SIM-REQ-401 | The first implementation shall run the starter scenario suite deterministically. | Replay tests. |
| SIM-REQ-402 | The first implementation shall emit all required output artifacts. | Output tests. |
| SIM-REQ-403 | The first implementation shall fail validation for scenarios requiring unresolved Charter mechanics without configured assumptions. | Invalid scenario tests. |
| SIM-REQ-404 | The first implementation shall label simulation abstractions in scenario manifests and outputs. | Manifest tests. |
| SIM-REQ-405 | The first implementation shall keep Mesa adapter tests separate from pure engine tests. | Test organization review. |

## 17. Open Questions Blocking Or Constraining Implementation

These questions are known Charter ambiguities or first-pass design blockers. The engine may accept configurable assumptions for scenario testing, but those assumptions shall be labeled as simulation abstractions unless the Charter is amended or authoritative guidance is added.

| ID | Open Question | Impact |
| --- | --- | --- |
| SIM-GAP-001 | What are the domain, normalization rule, aggregation rule, and voting-power relationship for `W = R^0.75`? | Blocks definitive weighted voting and weighted cap implementation. |
| SIM-GAP-002 | How is Subscriber approval measured for denominator, quorum, abstention, eligibility snapshot, and rapid membership changes? | Blocks definitive threshold implementation for contested scenarios. |
| SIM-GAP-003 | What precise test classifies an Authority as coercive when powers are mixed? | Blocks definitive 60% versus 75% threshold selection in mixed cases. |
| SIM-GAP-004 | How are Temporary Authorities staffed, funded, reviewed, limited, and dissolved? | Blocks detailed Temporary Authority lifecycle simulation. |
| SIM-GAP-005 | How are initial scoped electorates determined for inherently territorial Authorities? | Blocks definitive local Authority formation scenarios. |
| SIM-GAP-006 | How is satisfaction rating measured institutionally? | Blocks non-abstract satisfaction-triggered review. |
| SIM-GAP-007 | What evidentiary standard determines coalition or consolidated-persona aggregation? | Blocks definitive adversarial coalition detection. |
| SIM-GAP-008 | What powers does a Deliberation Assembly have beyond scope, feasibility, and rights compliance evaluation? | Blocks detailed petition pipeline simulation. |
| SIM-GAP-009 | What fallback exists if emergency extension requires all affected Authorities and one Authority blocks extension during a genuine emergency? | Blocks deadlock scenario resolution. |
| SIM-GAP-010 | What standards of review does the Charter Court apply to scope, emergency action, rights burdens, and procedural defects? | Blocks high-fidelity review simulation. |
| SIM-GAP-011 | How do Authority-Certification Bodies handle competition, appeals, recertification, discipline, and anti-cartel safeguards? | Blocks detailed Qualified Person pipeline simulation. |
| SIM-GAP-012 | What are the exact mechanics of Article XV Funding Acts, rate caps, transfer rules, conditional releases, and individual distributions? | Blocks detailed fiscal simulation beyond simple resource constraints. |
