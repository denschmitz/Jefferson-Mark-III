# Simulation Engine First-Test Readiness Plan

## Purpose

This plan defines the next simulator pass after the `baseline simulator tests passing` commit. The goal is to make the pure simulation engine ready for first meaningful engine-level tests before Mesa integration.

This pass should not attempt full simulator completeness. It should strengthen the deterministic engine surface so that later Mesa agents can emit events into stable, tested engine contracts.

## Requirements Position

The current split requirements are sufficient to begin the next engine-readiness pass. They do not need a broad rewrite first.

The pass should make only targeted requirement or gap updates when one of these conditions applies:

- A requirement is too broad for first-engine-test readiness and needs an explicit first-pass acceptance boundary.
- A blocked Charter ambiguity would otherwise force hidden implementation assumptions.
- A partial implementation is being closed and `docs/simulation_gaps.md` or the compliance matrix must be updated.

The pass should not silently implement Charter-ambiguous behavior. Weighted delegation, subscriber approval denominator mechanics, and mixed-power Coercive Authority classification should remain blocked or assumption-gated unless a separate requirements decision is made.

## Readiness Definition

The engine is first-test ready when:

- Invalid scenario inputs fail before event processing.
- Authority lifecycle transitions have complete first-pass tests for allowed and rejected transitions.
- Scope conflict detection has a narrow, deterministic, documented first-pass behavior.
- Minimal scenarios still run deterministically and emit required artifacts.
- Every deferred, blocked, or partial item touched by the pass is closed, retained, or newly recorded in `docs/simulation_gaps.md`.
- The full simulator test suite passes in `.venv`.

## Phase 0 - Requirements Triage

Goal: decide whether each planned implementation area can proceed under existing requirements, needs a narrow requirement clarification, or must remain blocked/deferred.

Requirements focus:

- `SIM-REQ-370` through `SIM-REQ-374`
- `SIM-REQ-390` through `SIM-REQ-405`
- `docs/simulation_gaps.md`
- `docs/simulation/requirements/compliance_matrix.md`

Design requirements:

- The pass shall check known gaps before implementation begins.
- The pass shall not broaden the simulator scope through code before the requirement boundary is recorded.
- Each planned phase shall classify its requirements as one of: ready, needs narrow clarification, assumption-gated, deferred, or blocked.
- Narrow clarifications shall be added to the relevant requirement file, the compliance matrix, or `docs/simulation_gaps.md` before implementation.
- Nice-to-have behavior shall not be added unless it is promoted through a proposed requirements update.

Implementation targets:

- `docs/simulation_engine_test_readiness_plan.md`
- `docs/simulation_gaps.md`
- `docs/simulation/requirements/compliance_matrix.md`
- Relevant files under `docs/simulation/requirements/`

Verification:

- Scenario validation hardening has a ready requirement boundary.
- Authority lifecycle coverage has a ready requirement boundary or explicit deferred exclusions.
- Scope conflict detection has a narrow first-pass requirement boundary before implementation.
- Weighted delegation remains blocked or assumption-gated unless a separate requirement decision is made.

Closeout:

- Record any newly discovered blocked, deferred, partial, or open items in `docs/simulation_gaps.md`.
- Update the compliance matrix when a requirement status changes.
- Do not proceed to implementation for an area whose requirement boundary is still unclear.

### Phase 0 Triage Results

Phase 0 reviewed the current split requirements, the compliance matrix, and `docs/simulation_gaps.md`. No broad requirements rewrite is needed before implementation. The next pass can proceed with targeted boundaries.

| Area | Classification | Requirement Decision | User Input Needed Before Coding? |
| --- | --- | --- | --- |
| Scenario validation hardening | ready | Existing `SIM-REQ-230` through `SIM-REQ-248` and `SIM-REQ-257` support this work. Keep unknown top-level fields allowed unless a later strict-mode requirement is proposed. | No |
| Authority lifecycle coverage | ready with deferred exclusions | Existing `SIM-REQ-130` through `SIM-REQ-149` and `SIM-REQ-550` through `SIM-REQ-568` support first-pass transition and gating tests. Merger, separation, consolidation, detailed review continuation, renewal, satisfaction, and dissolution procedure behavior remain deferred unless explicitly implemented. | No |
| Narrow scope conflict detection | ready with narrow first-pass boundary | Existing `SIM-REQ-190` through `SIM-REQ-200` and `SIM-REQ-570` through `SIM-REQ-589` support a structural detector. This pass shall implement only deterministic identifier-based checks and shall not implement Coordination Council selection, harmonization, Charter Court orders, or conflict resolution. | No |
| Engine acceptance scenarios | ready after prior phases | Existing `SIM-REQ-310` through `SIM-REQ-313` support the current minimal scenarios. New scenarios should cover Authority rejection and any implemented scope conflict behavior. Full starter suite remains deferred under `SIM-IMPL-GAP-011`. | No |
| Mesa boundary check | deferred / stub-only | Existing `SIM-REQ-350` through `SIM-REQ-355` describe full adapter expectations, but `SIM-IMPL-GAP-001` and `SIM-IMPL-GAP-002` defer full Mesa work. A boundary test may be added only to prove event submission without duplicating rules. | No |
| Weighted delegation | blocked or assumption-gated | `SIM-GAP-001`, `SIM-IMPL-GAP-006`, `SIM-PARTIAL-002`, and `SIM-REQ-504` block definitive weighted behavior. Do not implement weighted aggregation or weighted caps without a separate assumption decision. | Yes, only if this pass is expanded to weighted behavior |
| Subscriber approval mechanics | blocked or assumption-gated | `SIM-GAP-002` and `SIM-PARTIAL-001` block definitive denominator, quorum, abstention, and eligibility snapshot behavior. Continue using declared assumptions for first-pass Approval Records. | Yes, only if this pass is expanded to approval mechanics |
| Coercive classification for mixed powers | blocked or assumption-gated | `SIM-GAP-003` blocks a definitive mixed-power coercive classification test. Existing scenarios may supply `coercive_status`; mixed classification rules should not be inferred. | Yes, only if this pass is expanded to mixed-power classification |

### Phase 0 Closeout

Phase 0 closes with these implementation boundaries:

- Proceed to Phase 1 without additional user input.
- Treat scope conflict detection as structural detection only, not conflict resolution.
- Keep Mesa work to a boundary check unless a separate adapter implementation pass is approved.
- Keep weighted delegation, approval denominator mechanics, and mixed-power coercive classification out of scope unless the user supplies explicit assumptions or new requirements.
- Update `docs/simulation_gaps.md` and the compliance matrix during later phases only when a partial item is closed, retained with a changed boundary, or newly discovered.

## Phase 1 - Scenario Validation Hardening

Goal: make bad first-test scenarios fail clearly before engine behavior is evaluated.

Requirements focus:

- `SIM-REQ-230` through `SIM-REQ-248`
- `SIM-REQ-257`
- `SIM-PARTIAL-005`

Design requirements:

- Scenario validation shall require all fields used by `run_scenario_config`.
- Scenario validation shall validate `initial_state` collection types before record construction.
- Scenario validation shall validate scheduled event fields before event submission.
- Scenario validation shall reject unknown top-level fields only if an explicit strict mode is added; otherwise unknown fields shall remain allowed for forward compatibility.
- Scenario validation errors shall include stable issue codes and field paths.

Implementation targets:

- `simulation/src/jefferson_sim/engine/config.py`
- `simulation/src/jefferson_sim/engine/runner.py`
- `simulation/tests/test_config.py`
- `simulation/tests/test_scenarios.py`

Verification:

- Missing required runner fields fail validation.
- Invalid `initial_state` shapes fail validation.
- Invalid scheduled event shapes fail validation.
- Valid existing scenarios still pass.

Closeout:

- Update `docs/simulation/requirements/compliance_matrix.md` for `SIM-REQ-230` through `SIM-REQ-248`.
- Update or retain `SIM-PARTIAL-005` depending on remaining scenario-schema gaps.

### Phase 1 Closeout

Phase 1 implemented runner-facing scenario validation hardening.

Completed:

- Scenario text fields consumed by the runner are validated as non-empty strings.
- `initial_state` is validated as a mapping before runner state construction.
- Supported `initial_state` collections are validated as lists of mappings.
- Required fields for runner-constructed initial records are validated before record construction.
- `event_schedule` is validated as a list of mappings before event submission.
- Scheduled event type, tick, actor, payload, and provenance fields are validated before event submission.
- Unknown event types fail scenario validation before processing.

Verification:

```text
.\.venv\Scripts\python.exe -m pytest simulation\tests
67 passed
```

Remaining:

- `SIM-PARTIAL-005` remains open for full enabled-agent parameter validation, initial state generation rules, and formal schema coverage.

## Phase 2 - Authority Lifecycle Coverage

Goal: make Authority lifecycle behavior predictable enough for engine-level scenario tests.

Requirements focus:

- `SIM-REQ-130` through `SIM-REQ-149`
- `SIM-REQ-550` through `SIM-REQ-568`
- `SIM-PARTIAL-003`

Design requirements:

- Authority formation shall continue to be driven by Approval Records.
- Ordinary Authority actions shall remain gated by active lifecycle status.
- Every supported first-pass lifecycle transition shall have an allowed-transition test.
- Every explicitly rejected first-pass lifecycle transition shall have a rejection test.
- Unsupported merger, separation, consolidation, review-continuation, and dissolution mechanics shall remain documented gaps unless implemented in this pass.

Implementation targets:

- `simulation/src/jefferson_sim/engine/lifecycle.py`
- `simulation/src/jefferson_sim/engine/events.py`
- `simulation/tests/test_phase4_rules.py`
- `simulation/tests/test_events.py`

Verification:

- Formation pass creates or activates the expected Authority state.
- Formation failure records a rejected decision and does not activate the Authority.
- Invalid transitions fail deterministically.
- Inactive Authorities cannot execute ordinary actions.

Closeout:

- Update `SIM-PARTIAL-003` only if all first-pass lifecycle transition behavior is tested and any remaining non-first-pass behavior is separately deferred.

### Phase 2 Closeout

Phase 2 implemented first-pass Authority lifecycle coverage.

Completed:

- Every supported first-pass lifecycle transition is covered by tests.
- Unsupported first-pass transitions are covered by rejection tests.
- Merger and separation transitions remain unsupported in this pass instead of being silently allowed.
- Ordinary Authority actions are allowed only for active Authorities by default.
- Authorities under review require explicit continuation permission before ordinary actions are allowed.
- Formation pass and formation rejection behavior continue to be tested through engine events.

Verification:

```text
.\.venv\Scripts\python.exe -m pytest simulation\tests
100 passed
```

Remaining:

- `SIM-PARTIAL-003` remains open for lifecycle transition event records, review continuation rules beyond the helper gate, renewal decisions, dissolution procedures, and merger/separation/consolidation behavior.

## Phase 3 - Narrow Scope Conflict Detection

Goal: add the first useful institutional interaction test without pretending to solve the full conflict model.

Requirements focus:

- `SIM-REQ-190` through `SIM-REQ-200`
- `SIM-REQ-570` through `SIM-REQ-589`
- `SIM-IMPL-GAP-007`

Design requirements:

- First-pass conflict detection shall use scenario-defined identifiers, not geometry.
- Overlap alone shall not be a conflict.
- A conflict shall require at least one configured incompatibility, exclusive resource claim, enforcement-power mismatch, or prohibited-power use.
- The engine shall emit one deterministic conflict record or event per unique conflict key per tick.
- Any incompatibility matrix shall be labeled as a simulation abstraction unless directly traceable to a Charter rule.

Implementation targets:

- `simulation/src/jefferson_sim/engine/records.py`
- `simulation/src/jefferson_sim/engine/state.py`
- `simulation/src/jefferson_sim/engine/events.py`
- `simulation/tests/test_records.py`
- `simulation/tests/test_state.py`
- `simulation/tests/test_events.py`

Verification:

- Benign territorial overlap produces no conflict.
- Configured incompatible directives over overlapping territory produce one conflict.
- Exclusive resource overlap produces one conflict.
- Prohibited-power use produces a prohibited-power conflict.
- Duplicate detection within a tick is suppressed.

Closeout:

- Keep `SIM-IMPL-GAP-007` as partial unless all structural conflict classes in `SIM-REQ-570` through `SIM-REQ-589` are implemented.

### Phase 3 Closeout

Phase 3 implemented narrow structural scope conflict detection.

Completed:

- Added a scope conflict record model with deterministic IDs, Authority IDs, scope IDs, conflict basis, detected tick, resolution status, and trigger event provenance.
- Added scope conflict storage to `SimulationState` and final-state serialization.
- Added first-pass `authority_action` event handling.
- Benign overlap does not create conflicts.
- Same-tick incompatible directives over overlapping configured scope create a conflict.
- Exclusive resource claims over overlapping configured resources create a resource conflict.
- Prohibited-power use creates a prohibited-power conflict.
- Multi-basis conflicts are classified as `mixed`.
- Duplicate conflict records for the same unique key and tick are suppressed.

Verification:

```text
.\.venv\Scripts\python.exe -m pytest simulation\tests
107 passed
```

Remaining:

- `SIM-IMPL-GAP-007` remains open for complete conflict classes, scope-change triggers, Coordination Council selection, harmonization, Charter Court order behavior, conflict resolution events, and persistence beyond scenario termination rules.

## Phase 4 - Engine Acceptance Scenarios

Goal: prove the strengthened engine with scenarios that are still small enough to audit.

Requirements focus:

- `SIM-REQ-310` through `SIM-REQ-313`
- Current implemented portions of `SIM-REQ-110` through `SIM-REQ-149`
- Current implemented portions of `SIM-REQ-570` through `SIM-REQ-589`

Design requirements:

- Acceptance scenarios shall remain deterministic with fixed seeds.
- Each scenario shall exercise one main behavior and a small number of supporting records.
- Scenario outputs shall include enabled rule metadata, validation report, event log, rule decisions, metrics, and final state.

Implementation targets:

- `simulation/scenarios/*.yaml`
- `simulation/tests/test_scenarios.py`
- `simulation/tests/test_outputs.py`

Verification:

- Existing minimal delegation scenario still passes.
- Existing Authority creation scenario still passes.
- Add one Authority rejection scenario.
- Add one narrow scope conflict scenario if Phase 3 is implemented.

Closeout:

- Update the compliance matrix for any scenario requirements moved from partial to implemented.
- Add any scenario-suite limits that remain to `docs/simulation_gaps.md`.

### Phase 4 Closeout

Phase 4 added engine acceptance scenarios for the strengthened pure engine.

Completed:

- Added a deterministic Authority rejection scenario.
- Added a deterministic narrow scope conflict scenario.
- Added runner support for initial Authority records.
- Extended scenario validation to cover initial Authority record fields.
- Added scenario tests for Authority rejection state, rule decision result, and metrics.
- Added scenario tests for scope conflict state, mixed conflict classification, rule decision result, and metrics.
- Added output verification that the scope conflict scenario writes conflict state and labels the incompatibility matrix as a simulation abstraction.

Verification:

```text
.\.venv\Scripts\python.exe -m pytest simulation\tests
112 passed
```

Remaining:

- `SIM-IMPL-GAP-011` remains deferred for the full starter suite: local coercive Authority, emergency, consolidation, adversarial capture, dissatisfaction, reauthorization, harmonization, review, and resolution scenarios.

## Phase 5 - Mesa Boundary Check

Goal: confirm that the future Mesa adapter can use the engine without rule duplication.

Requirements focus:

- `SIM-REQ-350` through `SIM-REQ-355`
- `SIM-IMPL-GAP-001`
- `SIM-IMPL-GAP-002`

Design requirements:

- Mesa-facing code shall submit typed engine events.
- Mesa-facing code shall not mutate `SimulationState` directly.
- Mesa-facing code shall not duplicate Charter rule decisions.

Implementation targets:

- `simulation/src/jefferson_sim/mesa_adapter/`
- `simulation/tests/`

Verification:

- A stub adapter or boundary test can submit one engine event and receive an engine decision.
- No full Mesa agent behavior is required in this pass.

Closeout:

- Keep full Mesa implementation deferred unless this phase deliberately expands into adapter implementation.

### Phase 5 Closeout

Phase 5 implemented the Mesa boundary check without expanding into full Mesa implementation.

Completed:

- Added a thin `CharterMesaModel` boundary object under `simulation/src/jefferson_sim/mesa_adapter/`.
- The boundary consumes initialized `SimulationState` through an `EventProcessor`.
- Mesa-facing code can queue typed `EventInput` records without mutating engine state.
- The boundary advances ticks through the pure engine and returns engine `RuleDecision` records.
- The boundary exposes detached state snapshots for Mesa-facing inspection.
- Tests prove the adapter receives engine rejection decisions instead of duplicating Charter rule logic.

Verification:

```text
.\.venv\Scripts\python.exe -m pytest simulation\tests
117 passed
```

Remaining:

- `SIM-IMPL-GAP-001` remains deferred for a full Mesa `Model` implementation.
- `SIM-IMPL-GAP-002` remains deferred for real Mesa agent classes.
- Seeded stochastic Mesa behavior and Mesa-side metrics integration remain outside first-engine-test readiness.

## Phase 6 - First-Engine-Test Readiness Closeout

Goal: close the readiness pass with an explicit go/no-go result for first pure-engine tests.

Requirements focus:

- `SIM-REQ-370` through `SIM-REQ-374`
- `SIM-REQ-390` through `SIM-REQ-405`
- `docs/simulation_gaps.md`
- `docs/simulation/requirements/compliance_matrix.md`

Design requirements:

- The closeout shall state whether the engine is ready for first pure-engine tests.
- The closeout shall list the implemented readiness surfaces.
- The closeout shall preserve unresolved blocked, deferred, and partial work in `docs/simulation_gaps.md`.
- The closeout shall not mark full simulator or full Mesa readiness as complete.

### Phase 6 Closeout

Result: the pure simulation engine is ready for first engine-level tests under the first-test readiness boundary.

Completed readiness surfaces:

- Runner-facing scenario validation fails invalid scenario inputs before event processing.
- First-pass Authority lifecycle transitions and ordinary-action gating are tested.
- Narrow structural scope conflict detection is implemented and tested.
- Minimal delegation, Authority creation, Authority rejection, and narrow scope conflict scenarios run deterministically.
- Required first-pass output artifacts are emitted and include rule metadata, validation reports, event logs, rule decisions, metrics, and final state.
- Mesa-facing code has a thin event-submission boundary without full Mesa agent behavior or duplicated Charter rule logic.
- Known blocked, deferred, and partial work remains recorded in `docs/simulation_gaps.md`.

Verification:

```text
.\.venv\Scripts\python.exe -m pytest simulation\tests
117 passed
```

Not ready for:

- Full Mesa model and Mesa agent simulation.
- Weighted delegation or weighted cap behavior without explicit assumptions.
- Definitive subscriber approval denominator, quorum, abstention, or snapshot mechanics.
- Emergency lifecycle, consolidation, CCA, satisfaction-triggered behavior, and full review mechanics.
- Full starter scenario suite.
- Full metrics coverage.
- Formal scenario or agent JSON Schema.

## Explicit Non-Goals For This Pass

- Full Mesa model and agent implementation.
- Weighted delegation mechanics without an explicit assumption decision.
- Subscriber approval denominator, quorum, abstention, and snapshot mechanics beyond existing assumption handling.
- Emergency lifecycle behavior.
- Consolidation, CCA, and review-agent behavior.
- Satisfaction-triggered behavior.
- Full metrics coverage.
- Formal JSON Schema files.

## Recommended Work Order

1. Requirements triage.
2. Scenario validation hardening.
3. Authority lifecycle coverage.
4. Narrow scope conflict detection.
5. Engine acceptance scenarios.
6. Mesa boundary check.
7. First-engine-test readiness closeout.

This order reduces later rework because each phase strengthens the contracts used by the next one.
