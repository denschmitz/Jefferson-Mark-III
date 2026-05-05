# Machine-Readable Scope Model Requirements

This file is part of the split simulation requirements set. Requirement IDs and requirement text are preserved from the original monolithic requirements document.

## 6. Machine-Readable Scope Model

### Rationale

Authority scope is the main boundary mechanism in the Charter. The engine needs a structured representation that can be checked mechanically. This representation is a simulation representation of Charter scope, not new legal text.

### Requirements

| ID | Requirement | Suggested Verification |
| --- | --- | --- |
| SIM-REQ-190 | The engine shall require each Authority scope model to identify a function. | Scope schema validation test. |
| SIM-REQ-191 | The engine shall allow each Authority scope model to identify territory when territory is relevant. | Territory scenario test. |
| SIM-REQ-192 | The engine shall allow each Authority scope model to identify the population affected. | Population scope test. |
| SIM-REQ-193 | The engine shall require each Authority scope model to list permitted powers. | Scope schema validation test. |
| SIM-REQ-194 | The engine shall allow each Authority scope model to list prohibited powers. | Prohibited-power test. |
| SIM-REQ-195 | The engine shall allow each Authority scope model to specify resource authority. | Resource constraint test. |
| SIM-REQ-196 | The engine shall allow each Authority scope model to specify enforcement authority. | Enforcement scope test. |
| SIM-REQ-197 | The engine shall require each Authority scope model to specify review interval or inherit the Charter five-year default. | Review interval test. |
| SIM-REQ-198 | The engine shall allow each Authority scope model to specify emergency powers. | Emergency scope test. |
| SIM-REQ-199 | The engine shall allow each Authority scope model to specify parent or peer Authority references when compacts, overlaps, or dependencies are configured. | Reference validation test. |
| SIM-REQ-200 | The engine shall identify the scope model as a simulation representation in output manifests. | Manifest review. |

Suggested minimum scope fields:

| Field | Required | Notes |
| --- | --- | --- |
| `function` | Yes | Functional domain governed by the Authority. |
| `territory` | Conditional | Required for territorial scenarios. |
| `population_affected` | Conditional | Required when decisions depend on scoped electorate or satisfaction. |
| `permitted_powers` | Yes | Enumerated powers. |
| `prohibited_powers` | No | Explicit exclusions for tests. |
| `resource_authority` | No | Budget, assets, or operational resources. |
| `enforcement_authority` | No | Aligns with coercive classification. |
| `review_interval` | No | Defaults to five years. |
| `emergency_powers` | No | Constrained by Article V mechanics. |
| `authority_references` | No | Parent, peer, compact, overlap, or dependency references. |


