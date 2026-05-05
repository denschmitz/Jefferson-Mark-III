# Integration, Structure, And Acceptance Requirements

This file is part of the split simulation requirements set. Requirement IDs and requirement text are preserved from the original monolithic requirements document.

## 13. Mesa Integration Boundary

### Rationale

Mesa provides the agent-based runtime, not the constitutional interpreter. Keeping the boundary narrow makes the engine testable and allows future replacement or alternate runtimes.

### Requirements

| ID | Requirement | Suggested Verification |
| --- | --- | --- |
| SIM-REQ-350 | The Mesa adapter shall consume initialized engine state. | Adapter initialization test. |
| SIM-REQ-351 | The Mesa adapter shall create Mesa agents from scenario configuration. | Adapter initialization test. |
| SIM-REQ-352 | The Mesa adapter shall coordinate model step order without duplicating Charter rule logic. | Adapter code review and unit test. |
| SIM-REQ-353 | Mesa agents shall call engine services for Charter-constrained decisions. | Mock engine interaction test. |
| SIM-REQ-354 | The Mesa adapter shall collect metrics from engine state and agent state. | Metrics integration test. |
| SIM-REQ-355 | The Mesa adapter shall use seeded random selection for lot-selected bodies and stochastic scenario behavior. | Replay test. |

## 14. Initial Folder Structure

### Rationale

The folder structure separates documentation, rules configuration, pure engine code, Mesa integration, and tests.

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


