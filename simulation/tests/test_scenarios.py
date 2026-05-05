import json
from pathlib import Path

import pytest

from jefferson_sim.engine import (
    AuthorityLifecycleState,
    DelegationStatus,
    StateValidationError,
    load_scenario,
    run_scenario_config,
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
    assert manifest["enabled_rules"]["charter_derived"]
    assert manifest["enabled_rules"]["simulation_abstractions"]
    assert final_state["authorities"]["authority-1"]["lifecycle_status"] == "active"


def test_initial_state_recalculates_representative_totals_from_active_delegations() -> None:
    scenario_path = SCENARIO_DIR / "basic_delegation_stability.yaml"
    scenario = load_scenario(scenario_path)
    data = dict(scenario.data)
    data["duration"] = 0
    data["event_schedule"] = []
    data["initial_state"] = {
        "subscribers": [
            {"subscriber_id": "sub-1", "token_id": "token-1"},
            {"subscriber_id": "sub-2", "token_id": "token-2"},
        ],
        "representatives": [
            {
                "representative_id": "rep-1",
                "subscriber_id": "sub-1",
                "raw_delegation_total": 99.0,
            }
        ],
        "delegations": [
            {
                "delegation_id": "delegation-1",
                "source_subscriber_id": "sub-2",
                "target_representative_id": "rep-1",
                "token_share": 1.0,
                "submitted_tick": 0,
                "activation_tick": 0,
                "status": "active",
            }
        ],
    }

    result = run_scenario_config(
        type(scenario)(path=scenario.path, data=data, validation_report=scenario.validation_report),
        write_outputs=False,
    )

    assert result.processor.state.representatives["rep-1"].raw_delegation_total == 1.0


def test_initial_state_rejects_active_delegation_share_total_above_one() -> None:
    scenario_path = SCENARIO_DIR / "basic_delegation_stability.yaml"
    scenario = load_scenario(scenario_path)
    data = dict(scenario.data)
    data["duration"] = 0
    data["event_schedule"] = []
    data["initial_state"] = {
        "subscribers": [{"subscriber_id": "sub-1", "token_id": "token-1"}],
        "representatives": [
            {"representative_id": "rep-1", "subscriber_id": "sub-1"},
            {"representative_id": "rep-2", "subscriber_id": "sub-1"},
        ],
        "delegations": [
            {
                "delegation_id": "delegation-1",
                "source_subscriber_id": "sub-1",
                "target_representative_id": "rep-1",
                "token_share": 0.75,
                "submitted_tick": 0,
                "activation_tick": 0,
                "status": "active",
            },
            {
                "delegation_id": "delegation-2",
                "source_subscriber_id": "sub-1",
                "target_representative_id": "rep-2",
                "token_share": 0.5,
                "submitted_tick": 0,
                "activation_tick": 0,
                "status": "active",
            },
        ],
    }

    with pytest.raises(StateValidationError):
        run_scenario_config(
            type(scenario)(
                path=scenario.path,
                data=data,
                validation_report=scenario.validation_report,
            ),
            write_outputs=False,
        )
