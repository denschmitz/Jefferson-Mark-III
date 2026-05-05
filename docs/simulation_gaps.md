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
| SIM-GAP-001 | blocked | Weighting formula mechanics: domain, normalization, aggregation, and raw-versus-weighted voting power. | `docs/simulation/requirements/deferred_and_open_questions.md` |
| SIM-GAP-002 | blocked | Subscriber approval mechanics: denominator, quorum, abstention, eligibility snapshot, and rapid membership changes. | `docs/simulation/requirements/deferred_and_open_questions.md` |
| SIM-GAP-003 | blocked | Coercive Authority classification test for mixed powers. | `docs/simulation/requirements/deferred_and_open_questions.md` |
| SIM-GAP-004 | blocked | Temporary Authority staffing, funding, review, limitation, and dissolution mechanics. | `docs/simulation/requirements/deferred_and_open_questions.md` |
| SIM-GAP-005 | blocked | Initial scoped electorates for inherently territorial Authorities. | `docs/simulation/requirements/deferred_and_open_questions.md` |
| SIM-GAP-006 | blocked | Institutional satisfaction-rating measurement. | `docs/simulation/requirements/deferred_and_open_questions.md` |
| SIM-GAP-007 | blocked | Coalition or consolidated-persona evidentiary standard. | `docs/simulation/requirements/deferred_and_open_questions.md` |
| SIM-GAP-008 | blocked | Deliberation Assembly powers beyond evaluation of scope, feasibility, and rights compliance. | `docs/simulation/requirements/deferred_and_open_questions.md` |
| SIM-GAP-009 | blocked | Emergency extension deadlock fallback. | `docs/simulation/requirements/deferred_and_open_questions.md` |
| SIM-GAP-010 | blocked | Charter Court standards of review. | `docs/simulation/requirements/deferred_and_open_questions.md` |
| SIM-GAP-011 | blocked | Authority-Certification Body operations. | `docs/simulation/requirements/deferred_and_open_questions.md` |
| SIM-GAP-012 | blocked | Detailed Article XV Funding Act mechanics. | `docs/simulation/requirements/deferred_and_open_questions.md` |

## Deferred First-Pass Implementation Items

| ID | Status | Gap | Notes |
| --- | --- | --- | --- |
| SIM-IMPL-GAP-001 | deferred | Full Mesa adapter implementation. | First-test readiness includes a thin Mesa-facing boundary that queues engine events and advances ticks through `EventProcessor`; full Mesa `Model` behavior remains deferred. |
| SIM-IMPL-GAP-002 | deferred | Mesa agent classes beyond stubs or event-interface tests. | Boundary tests prove event submission without rule duplication; real Mesa agent classes remain deferred until the engine event API is stable enough for richer agent behavior. |
| SIM-IMPL-GAP-003 | deferred | Adversarial faction behavior. | Simulation abstraction; not needed for engine spine. |
| SIM-IMPL-GAP-004 | deferred | Court/review agent behavior. | Review records may exist before review behavior. |
| SIM-IMPL-GAP-005 | deferred | Event generator/environment agent behavior. | Scheduled scenario events are enough for first pass. |
| SIM-IMPL-GAP-006 | partial | Weighted delegation. | Implement only validation and `not_applicable` handling unless assumptions are supplied. |
| SIM-IMPL-GAP-007 | partial | Scope conflict detection beyond narrow structural checks. | First-pass structural detection now covers conflict records, benign overlap, incompatible same-tick directives, exclusive resource claims, prohibited-power use, and duplicate suppression. Coordination Council assignment, harmonization, Charter Court order behavior, resolution events, scope-change triggers, and complete conflict classes remain out of scope. |
| SIM-IMPL-GAP-008 | deferred | Emergency lifecycle. | First pass may include emergency records but not full review/extension behavior. |
| SIM-IMPL-GAP-009 | deferred | Consolidation audits and CCA decisions. | Requires more scenario structure. |
| SIM-IMPL-GAP-010 | deferred | Satisfaction-triggered behavior. | Satisfaction remains a stored simulation abstraction. |
| SIM-IMPL-GAP-011 | deferred | Full starter scenario suite. | First-test readiness now includes minimal delegation, Authority creation, Authority rejection, and narrow scope conflict scenarios. Emergency, consolidation, adversarial capture, dissatisfaction, reauthorization, and full local coercive Authority scenarios remain deferred. |
| SIM-IMPL-GAP-012 | deferred | Rights violation simulation. | Must remain abstraction until scenario criteria are defined. |
| SIM-IMPL-GAP-013 | deferred | Full output time-series coverage for every metric. | First pass may emit limited metrics for implemented rules. |
| SIM-IMPL-GAP-014 | deferred | Formal JSON Schema for scenario and agent definition files. | Deferred until after the first implementation phases so agent types, behavior parameters, and scenario structure can be defined deliberately. |

## First-Pass Partial Implementations To Close Later

| ID | Status | Item | Closeout Condition |
| --- | --- | --- | --- |
| SIM-PARTIAL-001 | partial | Approval Records with declared assumptions. | Close when denominator, quorum, abstention, and snapshot mechanics are fully implemented or formally configured. |
| SIM-PARTIAL-002 | partial | Delegation without complete weighted-power behavior. | Close when weighted delegation and cap behavior are tested with explicit assumptions. |
| SIM-PARTIAL-003 | partial | Authority lifecycle without transition-event records, merger/separation/consolidation order behavior, and detailed review/renewal/dissolution procedures. | First-pass supported transitions and ordinary-action gating are tested. Close when lifecycle transition events, review continuation rules, renewal decisions, dissolution procedures, and merger/separation/consolidation behavior are implemented or explicitly split into narrower gaps. |
| SIM-PARTIAL-004 | partial | Metrics limited to implemented rule subset. | Close when every `SIM-REQ-270` through `SIM-REQ-286` metric is implemented or explicitly marked not applicable. |
| SIM-PARTIAL-005 | partial | Scenario validation beyond runner-consumed fields. | Runner-consumed fields, `initial_state` collection shapes, and scheduled event shapes are validated. Close when all scenario fields from `SIM-REQ-230` through `SIM-REQ-248`, including enabled-agent parameters and generation rules, are enforced. |

## Gap Closeout Rules

- A `blocked` item can be closed only by Charter clarification, explicit simulation assumption, or a documented decision to keep the behavior unsupported.
- A `deferred` item can be closed by implementation plus tests.
- A `partial` item can be closed only when the final missing behavior is implemented, tested, and removed from this file.
- Any new implementation-phase gap shall be added here before the phase is considered complete.
