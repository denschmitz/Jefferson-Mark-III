# Simulation Requirements Index

This is the canonical entry point for the split Jefferson Mark III simulation requirements. The requirement IDs remain stable across the split; the source text was moved out of the former monolithic `docs/simulation_requirements.md` to reduce review noise.

## Requirement Files

| File | Scope |
| --- | --- |
| [purpose_and_authority.md](purpose_and_authority.md) | Purpose, scope, source-of-authority, and rule traceability requirements. |
| [core_concepts.md](core_concepts.md) | Core simulation concepts. |
| [records.md](records.md) | Core data and event record contracts. |
| [approvals.md](approvals.md) | Approval record schema and threshold requirements. |
| [events.md](events.md) | Event processing, simulation time, determinism, and replay requirements. |
| [agents.md](agents.md) | First-pass agent type requirements. |
| [institutional_mechanics.md](institutional_mechanics.md) | Delegation, Authority lifecycle, emergency, conflict, consolidation, and review mechanics. |
| [scope_model.md](scope_model.md) | Machine-readable scope model requirements. |
| [scenario_configuration.md](scenario_configuration.md) | Scenario configuration and starter scenario suite requirements. |
| [metrics_and_outputs.md](metrics_and_outputs.md) | Metrics, formulas, and required output artifacts. |
| [integration_structure_and_acceptance.md](integration_structure_and_acceptance.md) | Mesa boundary, folder structure, phased compliance, and acceptance criteria. |
| [deferred_and_open_questions.md](deferred_and_open_questions.md) | Non-goals and open Charter questions that block or constrain implementation. |

## Review Aids

| File | Purpose |
| --- | --- |
| [compliance_matrix.md](compliance_matrix.md) | Compact map from requirement IDs to implementation files, test files, status, and known gaps. |
| [../review_finding_closeout.md](../review_finding_closeout.md) | Closeout record for the first simulator compliance-review findings. |

## Related Documents

- [Simulation design](../../simulation_design.md)
- [Simulation first implementation plan](../../simulation_implementation_plan.md)
- [Simulation gaps](../../simulation_gaps.md)
