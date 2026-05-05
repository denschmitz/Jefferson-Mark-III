# Institutional Mechanics Requirements

This file is part of the split simulation requirements set. Requirement IDs and requirement text are preserved from the original monolithic requirements document.

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


