import json
from pathlib import Path

from jefferson_sim.engine import (
    AuthorityLifecycleState,
    DelegationStatus,
    run_scenario_file,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
SCENARIO_DIR = REPO_ROOT / "simulation" / "scenarios"


def test_basic_delegation_stability_scenario_runs_deterministically() -> None:
    scenario_path = SCENARIO_DIR / "basic_delegation_stability.yaml"

    first = run_scenario_file(scenario_path, write_outputs=False)
    second = run_scenario_file(scenario_path, write_outputs=False)

    assert first.final_state_hash == second.final_state_hash


def test_basic_delegation_stability_expected_state_decisions_and_metrics() -> None:
    scenario_path = SCENARIO_DIR / "basic_delegation_stability.yaml"

    result = run_scenario_file(scenario_path, write_outputs=False)
    state = result.processor.state

    delegation = state.delegations["delegation-event-000001"]
    assert delegation.status == DelegationStatus.ACTIVE
    assert state.representatives["rep-1"].raw_delegation_total == 1.0
    assert [decision.rule_id for decision in state.rule_decisions] == [
        "SIM-RULE-DELEGATION-CREATE",
        "SIM-RULE-DELEGATION-ACTIVATE",
    ]
    metrics = {metric.metric_id: metric.value for metric in state.metrics}
    assert metrics["raw_power_concentration"] == 0.5
    assert metrics["delegation_churn"] == 0.5


def test_authority_creation_scenario_runs_deterministically() -> None:
    scenario_path = SCENARIO_DIR / "authority_creation.yaml"

    first = run_scenario_file(scenario_path, write_outputs=False)
    second = run_scenario_file(scenario_path, write_outputs=False)

    assert first.final_state_hash == second.final_state_hash


def test_authority_creation_expected_state_decisions_and_metrics() -> None:
    scenario_path = SCENARIO_DIR / "authority_creation.yaml"

    result = run_scenario_file(scenario_path, write_outputs=False)
    state = result.processor.state

    authority = state.authorities["authority-1"]
    assert authority.lifecycle_status == AuthorityLifecycleState.ACTIVE
    assert state.rule_decisions[-1].rule_id == "SIM-RULE-AUTHORITY-FORMATION"
    assert state.rule_decisions[-1].result == "accepted"
    metrics = {metric.metric_id: metric.value for metric in state.metrics}
    assert metrics["authority_count"] == 1


def test_minimal_scenario_outputs_are_written() -> None:
    scenario_path = SCENARIO_DIR / "authority_creation.yaml"

    result = run_scenario_file(scenario_path, write_outputs=True)

    assert result.output_paths is not None
    manifest = json.loads(result.output_paths.manifest.read_text(encoding="utf-8"))
    final_state = json.loads(result.output_paths.final_state.read_text(encoding="utf-8"))

    assert manifest["scenario_id"] == "authority_creation"
    assert manifest["final_state_hash"] == result.final_state_hash
    assert final_state["authorities"]["authority-1"]["lifecycle_status"] == "active"
