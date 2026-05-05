# Approval Record Requirements

This file is part of the split simulation requirements set. Requirement IDs and requirement text are preserved from the original monolithic requirements document.

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


