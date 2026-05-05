from pathlib import Path

import pytest

from jefferson_sim.engine import (
    ConfigLoadError,
    ValidationSeverity,
    load_charter_derivative,
    load_scenario,
    load_structured_file,
    validate_scenario,
)


REPO_ROOT = Path(__file__).resolve().parents[2]


def minimal_scenario() -> dict[str, object]:
    return {
        "scenario_id": "basic-delegation",
        "scenario_version": "0.1.0",
        "charter_derivative_path": "derivatives/simulation/charter_sim.yaml",
        "random_seed": 123,
        "duration": 30,
        "tick_duration": "day",
        "output_path": "simulation/runs/basic-delegation",
        "population_size": 100,
        "agent_distributions": {"subscriber": 100},
        "output_settings": {"format": "json"},
    }


def test_load_real_charter_derivative() -> None:
    config = load_charter_derivative(REPO_ROOT / "derivatives" / "simulation" / "charter_sim.yaml")

    assert config.data["meta"]["source"] == "charter/charter.md"
    assert not config.validation_report.has_errors


def test_load_json_scenario() -> None:
    scenario_path = Path(__file__).with_name("fixtures") / "scenario.json"
    scenario = load_scenario(scenario_path)

    assert scenario.data["scenario_id"] == "basic-delegation"
    assert not scenario.validation_report.has_errors


def test_load_yaml_scenario() -> None:
    scenario_path = Path(__file__).with_name("fixtures") / "scenario.yaml"
    scenario = load_scenario(scenario_path)

    assert scenario.data["random_seed"] == 123
    assert not scenario.validation_report.has_errors


def test_scenario_missing_required_fields_fails_validation() -> None:
    report = validate_scenario({"scenario_id": "missing-fields"})

    assert report.has_errors
    assert any(issue.code == "scenario.missing_field" for issue in report.issues)


def test_runner_consumed_text_fields_must_be_non_empty_strings() -> None:
    scenario = minimal_scenario()
    scenario["output_path"] = ""

    report = validate_scenario(scenario)

    assert report.has_errors
    assert any(issue.code == "scenario.output_path.invalid" for issue in report.issues)


def test_initial_state_must_be_mapping() -> None:
    scenario = minimal_scenario()
    scenario["initial_state"] = []

    report = validate_scenario(scenario)

    assert report.has_errors
    assert any(issue.code == "scenario.initial_state.invalid" for issue in report.issues)


def test_initial_state_collections_must_be_lists() -> None:
    scenario = minimal_scenario()
    scenario["initial_state"] = {"subscribers": {"subscriber_id": "sub-1"}}

    report = validate_scenario(scenario)

    assert report.has_errors
    assert any(issue.code == "scenario.initial_state.collection.invalid" for issue in report.issues)


def test_initial_state_records_must_include_runner_required_fields() -> None:
    scenario = minimal_scenario()
    scenario["initial_state"] = {"representatives": [{"representative_id": "rep-1"}]}

    report = validate_scenario(scenario)

    assert report.has_errors
    assert any(
        issue.code == "scenario.initial_state.record.missing_field"
        and issue.path == "initial_state.representatives.0.subscriber_id"
        for issue in report.issues
    )


def test_event_schedule_must_be_list_of_mappings() -> None:
    scenario = minimal_scenario()
    scenario["event_schedule"] = ["delegation_create"]

    report = validate_scenario(scenario)

    assert report.has_errors
    assert any(issue.code == "scenario.event_schedule.event.invalid" for issue in report.issues)


def test_event_schedule_requires_fields_used_for_event_input() -> None:
    scenario = minimal_scenario()
    scenario["event_schedule"] = [{"event_type": "noop"}]

    report = validate_scenario(scenario)

    assert report.has_errors
    assert any(
        issue.code == "scenario.event_schedule.event.missing_field"
        and issue.path == "event_schedule.0.actor_id"
        for issue in report.issues
    )
    assert any(
        issue.code == "scenario.event_schedule.event.missing_field"
        and issue.path == "event_schedule.0.effective_tick"
        for issue in report.issues
    )


def test_event_schedule_rejects_unknown_event_type_before_processing() -> None:
    scenario = minimal_scenario()
    scenario["event_schedule"] = [
        {"event_type": "unknown", "effective_tick": 0, "actor_id": "sub-1"}
    ]

    report = validate_scenario(scenario)

    assert report.has_errors
    assert any(issue.code == "scenario.event_schedule.event_type.unknown" for issue in report.issues)


def test_event_schedule_payload_and_provenance_must_be_mappings() -> None:
    scenario = minimal_scenario()
    scenario["event_schedule"] = [
        {
            "event_type": "noop",
            "effective_tick": 0,
            "actor_id": "sub-1",
            "payload": [],
            "provenance": [],
        }
    ]

    report = validate_scenario(scenario)

    assert report.has_errors
    assert any(issue.code == "scenario.event_schedule.payload.invalid" for issue in report.issues)
    assert any(issue.code == "scenario.event_schedule.provenance.invalid" for issue in report.issues)


def test_required_gap_assumption_must_be_declared() -> None:
    scenario = minimal_scenario()
    scenario["required_gap_assumptions"] = ["SIM-GAP-002"]

    report = validate_scenario(scenario)

    assert report.has_errors
    assert any(issue.code == "scenario.gap_assumption.missing" for issue in report.issues)


def test_declared_gap_assumption_passes_validation() -> None:
    scenario = minimal_scenario()
    scenario["required_gap_assumptions"] = ["SIM-GAP-002"]
    scenario["gap_assumptions"] = {"SIM-GAP-002": "fixed eligible snapshot"}

    report = validate_scenario(scenario)

    assert not report.has_errors


def test_simulation_abstraction_emits_notice() -> None:
    scenario = minimal_scenario()
    scenario["simulation_abstractions"] = ["satisfaction_metric"]

    report = validate_scenario(scenario)

    assert any(issue.severity == ValidationSeverity.NOTICE for issue in report.issues)


def test_unsupported_config_extension_fails() -> None:
    path = Path(__file__).with_name("fixtures") / "scenario.txt"

    with pytest.raises(ConfigLoadError):
        load_structured_file(path)
