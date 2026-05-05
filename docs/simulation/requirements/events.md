# Event, Time, And Determinism Requirements

This file is part of the split simulation requirements set. Requirement IDs and requirement text are preserved from the original monolithic requirements document.

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


