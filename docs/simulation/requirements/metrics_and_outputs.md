# Metrics And Output Requirements

This file is part of the split simulation requirements set. Requirement IDs and requirement text are preserved from the original monolithic requirements document.

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


