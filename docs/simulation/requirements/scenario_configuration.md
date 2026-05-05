# Scenario Configuration And Suite Requirements

This file is part of the split simulation requirements set. Requirement IDs and requirement text are preserved from the original monolithic requirements document.

## 8. Scenario Configuration

### Rationale

Scenario files define initial conditions and behavior parameters without changing engine code. YAML or JSON are acceptable because both can be versioned and diffed.

### Requirements

| ID | Requirement | Suggested Verification |
| --- | --- | --- |
| SIM-REQ-230 | The engine shall load scenario configuration from YAML or JSON. | Config loading test. |
| SIM-REQ-231 | Scenario configuration shall include population size. | Schema validation test. |
| SIM-REQ-232 | Scenario configuration shall include agent distributions. | Schema validation test. |
| SIM-REQ-233 | Scenario configuration shall allow initial delegations. | Initialization test. |
| SIM-REQ-234 | Scenario configuration shall allow initial Authorities. | Initialization test. |
| SIM-REQ-235 | Scenario configuration shall allow geography or territory model configuration. | Territory scenario test. |
| SIM-REQ-236 | Scenario configuration shall allow an event schedule. | Event scheduling test. |
| SIM-REQ-237 | Scenario configuration shall allow adversarial behavior settings. | Adversarial scenario test. |
| SIM-REQ-238 | Scenario configuration shall require a random seed. | Validation test. |
| SIM-REQ-239 | Scenario configuration shall require simulation duration. | Validation test. |
| SIM-REQ-240 | Scenario configuration shall include output settings. | Output test. |
| SIM-REQ-241 | Scenario configuration shall include a scenario schema version. | Manifest validation test. |
| SIM-REQ-242 | Scenario configuration shall identify any simulation abstractions used by the scenario. | Manifest validation test. |
| SIM-REQ-243 | Scenario configuration shall include `scenario_id`, `scenario_version`, `charter_derivative_path`, `random_seed`, `duration`, `tick_duration`, and `output_path`. | Scenario schema validation test. |
| SIM-REQ-244 | Scenario configuration shall include agent configuration sections for every enabled agent type. | Scenario schema validation test. |
| SIM-REQ-245 | Scenario configuration shall fail validation when an enabled agent type lacks required state or behavior parameters. | Invalid scenario test. |
| SIM-REQ-246 | Scenario configuration shall include initial state records or generation rules for Subscribers, Representatives, Authorities, and Delegations. | Initialization validation test. |
| SIM-REQ-247 | Scenario configuration shall declare any assumptions used to resolve `SIM-GAP-*` items. | Gap assumption validation test. |
| SIM-REQ-248 | Scenario configuration shall fail validation when a scenario requires an unresolved `SIM-GAP-*` assumption that is not declared. | Invalid scenario test. |


## 11. First-Pass Scenario Suite

### Rationale

The starter suite exercises high-value Charter mechanics without requiring high-fidelity social modeling.

### Requirements

| ID | Requirement | Suggested Verification |
| --- | --- | --- |
| SIM-REQ-310 | The scenario suite shall include a Basic Delegation Stability scenario. | Scenario manifest review. |
| SIM-REQ-311 | The Basic Delegation Stability scenario shall test delegation activation delay, change limits, caps, and churn metrics. | Scenario acceptance test. |
| SIM-REQ-312 | The scenario suite shall include an Authority Creation And Reauthorization scenario. | Scenario manifest review. |
| SIM-REQ-313 | The Authority Creation And Reauthorization scenario shall test formation threshold, activation, five-year review, and renewal. | Scenario acceptance test. |
| SIM-REQ-314 | The scenario suite shall include a Local Coercive Authority or Neighborhood Patrol scenario. | Scenario manifest review. |
| SIM-REQ-315 | The Local Coercive Authority or Neighborhood Patrol scenario shall test coercive threshold, territorial scope, enforcement powers, and scoped-electorate gap handling. | Scenario acceptance test. |
| SIM-REQ-316 | The scenario suite shall include an Emergency Power Expiration And Review scenario. | Scenario manifest review. |
| SIM-REQ-317 | The Emergency Power Expiration And Review scenario shall test provisional activation, thirty-day duration, extension, publication, expiry, and review. | Scenario acceptance test. |
| SIM-REQ-318 | The scenario suite shall include a Scope Conflict Between Overlapping Authorities scenario. | Scenario manifest review. |
| SIM-REQ-319 | The Scope Conflict scenario shall test Coordination Council assignment, harmonization rule, territorial fallback, and Charter Court order duration. | Scenario acceptance test. |
| SIM-REQ-320 | The scenario suite shall include an Authority Sprawl And Consolidation Audit scenario. | Scenario manifest review. |
| SIM-REQ-321 | The Authority Sprawl scenario shall test governance credit limit, audit scheduling, CCA constraints, and dissolution or merger outcomes. | Scenario acceptance test. |
| SIM-REQ-322 | The scenario suite shall include an Adversarial Capture Attempt scenario. | Scenario manifest review. |
| SIM-REQ-323 | The Adversarial Capture Attempt scenario shall test coordinated delegation shifts, cap enforcement, stabilization, coalition aggregation, and capture metrics. | Scenario acceptance test. |
| SIM-REQ-324 | The scenario suite shall include a Public Dissatisfaction And Delegation Migration scenario. | Scenario manifest review. |
| SIM-REQ-325 | The Public Dissatisfaction scenario shall test satisfaction-triggered review, delegation migration, reauthorization, and review load. | Scenario acceptance test. |


