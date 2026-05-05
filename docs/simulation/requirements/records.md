# Core Record Requirements

This file is part of the split simulation requirements set. Requirement IDs and requirement text are preserved from the original monolithic requirements document.

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


