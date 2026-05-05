# Core Concept Requirements

This file is part of the split simulation requirements set. Requirement IDs and requirement text are preserved from the original monolithic requirements document.

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


