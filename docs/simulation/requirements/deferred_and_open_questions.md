# Deferred Scope And Open Questions

This file is part of the split simulation requirements set. Requirement IDs and requirement text are preserved from the original monolithic requirements document.

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

