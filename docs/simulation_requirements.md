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

The simulation must be traceable to the Charter and must not become an alternate constitutional source. Machine-readable derivatives and requirements documents support implementation but do not supersede the canonical Charter.

### Requirements

| ID | Requirement | Suggested Verification |
| --- | --- | --- |
| SIM-REQ-010 | The canonical source of Charter authority shall be `charter/charter.md`. | Documentation review. |
| SIM-REQ-011 | The machine-readable derivative shall be `derivatives/simulation/charter_sim.yaml`. | Configuration loading test. |
| SIM-REQ-012 | If this document conflicts with `charter/charter.md`, `charter/charter.md` shall control. | Documentation review. |
| SIM-REQ-013 | If `charter_sim.yaml` conflicts with `charter/charter.md`, the YAML shall be treated as defective. | Validation test using injected mismatch metadata. |
| SIM-REQ-014 | Simulation-only abstractions shall be explicitly marked as simulation abstractions in requirements, configuration, or output metadata. | Static review of scenario schema and generated manifest. |
| SIM-REQ-015 | Charter ambiguities shall be represented as open questions, configurable assumptions, or implementation-blocking validation errors. | Gap-handling unit tests. |

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

## 4. Agent Types For First Pass

### Rationale

First-pass agents should be simple enough to isolate Charter mechanics. Agent behavior exists to generate rule-relevant inputs, not to model high-fidelity political psychology.

### Common Agent Requirements

| ID | Requirement | Suggested Verification |
| --- | --- | --- |
| SIM-REQ-040 | Each agent shall have a stable identifier. | Agent initialization test. |
| SIM-REQ-041 | Each agent shall expose required state to the engine through typed data structures. | Serialization test. |
| SIM-REQ-042 | Each agent shall emit actions as simulation events. | Agent action test. |
| SIM-REQ-043 | Each agent shall accept deterministic configuration parameters. | Scenario loading test. |
| SIM-REQ-044 | Any stochastic agent choice shall use the scenario random seed. | Deterministic replay test. |

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
| SIM-REQ-050 | Subscriber agents shall be able to hold exactly one representation token. | Initialization test. |
| SIM-REQ-051 | Subscriber agents shall be able to delegate fractional or whole token shares when fractional delegation is enabled. | Delegation test. |
| SIM-REQ-052 | Subscriber agents shall be able to vote in Authority formation, reauthorization, National Decision, and scenario-defined legislative decisions. | Voting event tests. |

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
| SIM-REQ-090 | Court or review agents shall support deterministic decision rules. | Deterministic review test. |
| SIM-REQ-091 | Court or review agents shall record review queue length by tick. | Metrics test. |
| SIM-REQ-092 | Court or review agents shall not create new Authority powers. | Review output validation test. |

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
| SIM-REQ-115 | The engine shall support fractional delegation when enabled by scenario configuration. | Fractional delegation test. |
| SIM-REQ-116 | The engine shall compute delegation weight using `W = R^0.75` when the unresolved normalization assumptions are provided. | Weighting test. |
| SIM-REQ-117 | The engine shall block or flag weighting calculations when required unresolved weighting assumptions are absent. | Gap validation test. |
| SIM-REQ-118 | The engine shall enforce a one-percent raw delegation cap per Representative. | Raw cap test. |
| SIM-REQ-119 | The engine shall enforce a one-percent weighted delegation cap per Representative when weighted totals are computable. | Weighted cap test. |
| SIM-REQ-120 | The engine shall return excess delegation to Subscribers for reassignment. | Excess reassignment test. |
| SIM-REQ-121 | The engine shall apply coalition aggregation for cap purposes when coalition membership is configured. | Coalition cap test. |
| SIM-REQ-122 | The engine shall trigger stabilization when more than five percent of representation tokens are scheduled to activate delegation shifts within a fourteen-day period. | Stabilization trigger test. |
| SIM-REQ-123 | The engine shall uniformly extend affected delegation activation dates by thirty days when stabilization triggers. | Stabilization extension test. |
| SIM-REQ-124 | The engine shall log stabilization extensions. | Event log test. |

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
| SIM-REQ-138 | The engine shall support Authority dissolution according to configured Authority Charter procedures. | Dissolution test. |
| SIM-REQ-139 | The engine shall schedule structural and performance review every five years for each Authority. | Review scheduling test. |
| SIM-REQ-140 | The engine shall require simple majority approval of Subscribers within Authority scope for renewal. | Renewal test. |
| SIM-REQ-141 | The engine shall trigger mandatory reauthorization review after twelve consecutive months below forty-percent satisfaction. | Satisfaction trigger test. |
| SIM-REQ-142 | The engine shall label satisfaction metric rules as simulation abstractions until the Charter defines measurement mechanics. | Manifest review. |

### Emergency Mechanics

| ID | Requirement | Suggested Verification |
| --- | --- | --- |
| SIM-REQ-150 | The engine shall allow emergency declaration only for configured threats to life, essential infrastructure, security, or governance continuity. | Emergency validation test. |
| SIM-REQ-151 | The engine shall allow a Lead Emergency Authority to exercise emergency powers for thirty days after a qualifying declaration. | Emergency duration test. |
| SIM-REQ-152 | The engine shall require approval by all affected Authorities for extension to ninety days. | Extension test. |
| SIM-REQ-153 | The engine shall require National Decision approval for extension beyond one year. | Long extension test. |
| SIM-REQ-154 | The engine shall require emergency measures to be publicly posted within seven days. | Deadline test. |
| SIM-REQ-155 | The engine shall expire emergency powers when the emergency ends. | Expiration test. |
| SIM-REQ-156 | The engine shall support provisional emergency measures for up to seventy-two hours. | Provisional activation test. |
| SIM-REQ-157 | The engine shall require immediate ECO and Charter Court notification for provisional measures. | Notification event test. |
| SIM-REQ-158 | The engine shall subject emergency actions to configured Charter Court review for Articles XVI and XVII compliance. | Review scenario test. |

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
| SIM-REQ-178 | The engine shall support National Decision override of the governance credit limit. | Override test. |
| SIM-REQ-179 | The engine shall support Consolidation Conflict Authority decisions for configured consolidation disputes. | CCA scenario test. |
| SIM-REQ-180 | The engine shall prevent CCA decisions from modifying Charter text, Legislative Acts, funding levels, or expanding Authority scope. | CCA validation test. |

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
| `enforcement_authority` | No | Must align with coercive classification. |
| `review_interval` | No | Defaults to five years. |
| `emergency_powers` | No | Must be Article V constrained. |
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
| SIM-REQ-214 | The engine shall support review windows. | Review window test. |
| SIM-REQ-215 | The engine shall support delegation activation delays. | Delegation schedule test. |
| SIM-REQ-216 | The engine shall support emergency deadlines. | Emergency deadline test. |
| SIM-REQ-217 | The engine shall support reporting periods for metrics. | Metrics period test. |
| SIM-REQ-218 | The engine shall preserve event ordering within a tick according to a deterministic ordering rule. | Replay ordering test. |

## 8. Scenario Configuration

### Rationale

Scenario files should define initial conditions and behavior parameters without changing engine code. YAML or JSON are acceptable because both can be versioned and diffed.

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

## 11. First-Pass Scenario Suite

### Rationale

The starter suite should exercise high-value Charter mechanics without requiring high-fidelity social modeling.

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

Mesa should provide the agent-based runtime, not the constitutional interpreter. Keeping the boundary narrow makes the engine testable and allows future replacement or alternate runtimes.

### Requirements

| ID | Requirement | Suggested Verification |
| --- | --- | --- |
| SIM-REQ-350 | The Mesa adapter shall consume initialized engine state. | Adapter initialization test. |
| SIM-REQ-351 | The Mesa adapter shall create Mesa agents from scenario configuration. | Adapter initialization test. |
| SIM-REQ-352 | The Mesa adapter shall coordinate model step order without duplicating Charter rule logic. | Adapter code review and unit test. |
| SIM-REQ-353 | Mesa agents shall call engine services for Charter-constrained decisions. | Mock engine interaction test. |
| SIM-REQ-354 | The Mesa adapter shall collect metrics from engine state and agent state. | Metrics integration test. |
| SIM-REQ-355 | The Mesa adapter shall support seeded random selection for lot-selected bodies and stochastic scenario behavior. | Replay test. |

## 14. Initial Folder Structure

### Rationale

The folder structure should separate documentation, rules configuration, pure engine code, Mesa integration, and tests.

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

These questions are known Charter ambiguities or first-pass design blockers. The engine may support configurable assumptions for scenario testing, but those assumptions must be labeled as simulation abstractions unless the Charter is amended or authoritative guidance is added.

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
