# Simulation Gaps

## Purpose

This document tracks known unimplemented, deferred, or blocked simulation work. It exists so implementation passes can close items deliberately instead of losing them in intermediate plans.

Statuses:

- `blocked`: cannot be implemented definitively without Charter clarification or explicit simulation assumptions.
- `deferred`: valid requirement, intentionally outside the first implementation pass.
- `partial`: expected to receive a limited first-pass implementation.
- `open`: needs design detail before implementation.

## Charter Ambiguity Gaps

| ID | Status | Gap | Source |
| --- | --- | --- | --- |
| SIM-GAP-001 | blocked | Weighting formula mechanics: domain, normalization, aggregation, and raw-versus-weighted voting power. | `docs/simulation_requirements.md` |
| SIM-GAP-002 | blocked | Subscriber approval mechanics: denominator, quorum, abstention, eligibility snapshot, and rapid membership changes. | `docs/simulation_requirements.md` |
| SIM-GAP-003 | blocked | Coercive Authority classification test for mixed powers. | `docs/simulation_requirements.md` |
| SIM-GAP-004 | blocked | Temporary Authority staffing, funding, review, limitation, and dissolution mechanics. | `docs/simulation_requirements.md` |
| SIM-GAP-005 | blocked | Initial scoped electorates for inherently territorial Authorities. | `docs/simulation_requirements.md` |
| SIM-GAP-006 | blocked | Institutional satisfaction-rating measurement. | `docs/simulation_requirements.md` |
| SIM-GAP-007 | blocked | Coalition or consolidated-persona evidentiary standard. | `docs/simulation_requirements.md` |
| SIM-GAP-008 | blocked | Deliberation Assembly powers beyond evaluation of scope, feasibility, and rights compliance. | `docs/simulation_requirements.md` |
| SIM-GAP-009 | blocked | Emergency extension deadlock fallback. | `docs/simulation_requirements.md` |
| SIM-GAP-010 | blocked | Charter Court standards of review. | `docs/simulation_requirements.md` |
| SIM-GAP-011 | blocked | Authority-Certification Body operations. | `docs/simulation_requirements.md` |
| SIM-GAP-012 | blocked | Detailed Article XV Funding Act mechanics. | `docs/simulation_requirements.md` |

## Deferred First-Pass Implementation Items

| ID | Status | Gap | Notes |
| --- | --- | --- | --- |
| SIM-IMPL-GAP-001 | deferred | Full Mesa adapter implementation. | First pass should prove pure engine behavior first. |
| SIM-IMPL-GAP-002 | deferred | Mesa agent classes beyond stubs or event-interface tests. | Requires stable engine event API. |
| SIM-IMPL-GAP-003 | deferred | Adversarial faction behavior. | Simulation abstraction; not needed for engine spine. |
| SIM-IMPL-GAP-004 | deferred | Court/review agent behavior. | Review records may exist before review behavior. |
| SIM-IMPL-GAP-005 | deferred | Event generator/environment agent behavior. | Scheduled scenario events are enough for first pass. |
| SIM-IMPL-GAP-006 | partial | Weighted delegation. | Implement only validation and `not_applicable` handling unless assumptions are supplied. |
| SIM-IMPL-GAP-007 | partial | Scope conflict detection. | First pass may define records; full structural detection can wait until after lifecycle and events are stable. |
| SIM-IMPL-GAP-008 | deferred | Emergency lifecycle. | First pass may include emergency records but not full review/extension behavior. |
| SIM-IMPL-GAP-009 | deferred | Consolidation audits and CCA decisions. | Requires more scenario structure. |
| SIM-IMPL-GAP-010 | deferred | Satisfaction-triggered behavior. | Satisfaction remains a stored simulation abstraction. |
| SIM-IMPL-GAP-011 | deferred | Full starter scenario suite. | First pass includes only minimal delegation and Authority formation scenarios. |
| SIM-IMPL-GAP-012 | deferred | Rights violation simulation. | Must remain abstraction until scenario criteria are defined. |
| SIM-IMPL-GAP-013 | deferred | Full output time-series coverage for every metric. | First pass may emit limited metrics for implemented rules. |
| SIM-IMPL-GAP-014 | deferred | Formal JSON Schema for scenario and agent definition files. | Deferred until after the first implementation phases so agent types, behavior parameters, and scenario structure can be defined deliberately. |
| SIM-IMPL-GAP-015 | open | Scenario manifests do not list enabled Charter-derived rules and simulation abstraction rules. | Required by `SIM-REQ-020C`; current manifest records event ordering and provenance only. |
| SIM-IMPL-GAP-016 | open | Rule decisions do not expose post-state references for state-changing decisions. | Required by `SIM-REQ-525`; current `RuleDecision` stores only `input_state_hash`. |
| SIM-IMPL-GAP-017 | open | Approval records accept caller-supplied approval ratios, threshold results, and arbitrary decision types. | Required by `SIM-REQ-531`, `SIM-REQ-535`, and `SIM-REQ-539`; first pass should compute or validate these fields from counts and known decision types. |
| SIM-IMPL-GAP-018 | open | Initial scenario state can import authoritative representative delegation totals and active delegations without aggregate validation. | Required by `SIM-REQ-503` and `SIM-REQ-507`; event-time activation enforces token conservation, but initial state loading does not. |

## First-Pass Partial Implementations To Close Later

| ID | Status | Item | Closeout Condition |
| --- | --- | --- | --- |
| SIM-PARTIAL-001 | partial | Approval Records with declared assumptions. | Close when denominator, quorum, abstention, and snapshot mechanics are fully implemented or formally configured. |
| SIM-PARTIAL-002 | partial | Delegation without complete weighted-power behavior. | Close when weighted delegation and cap behavior are tested with explicit assumptions. |
| SIM-PARTIAL-003 | partial | Authority lifecycle without merger/separation/consolidation order behavior. | Close when all state machine transitions have tests. |
| SIM-PARTIAL-004 | partial | Metrics limited to implemented rule subset. | Close when every `SIM-REQ-270` through `SIM-REQ-286` metric is implemented or explicitly marked not applicable. |
| SIM-PARTIAL-005 | partial | Scenario validation with minimal schema. | Close when all scenario fields from `SIM-REQ-230` through `SIM-REQ-248` are enforced. |

## Gap Closeout Rules

- A `blocked` item can be closed only by Charter clarification, explicit simulation assumption, or a documented decision to keep the behavior unsupported.
- A `deferred` item can be closed by implementation plus tests.
- A `partial` item can be closed only when the final missing behavior is implemented, tested, and removed from this file.
- Any new implementation-phase gap shall be added here before the phase is considered complete.
