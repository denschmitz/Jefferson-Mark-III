import csv
import json
from datetime import date
from pathlib import Path

from jefferson_sim.engine import (
    EventInput,
    EventProcessor,
    MetricRecord,
    RunOutputContext,
    SubscriberRecord,
    ValidationReport,
    ValidationSeverity,
    enabled_rule_manifest,
    raw_power_concentration,
    write_run_outputs,
)


OUTPUT_DIR = Path(__file__).with_name("_generated_outputs") / "phase5"


def build_output_state():
    processor = EventProcessor()
    processor.state.add_subscriber(SubscriberRecord("sub-1", "token-1"))
    processor.submit_events(
        0,
        [
            EventInput(
                event_type="noop",
                submitted_tick=0,
                effective_tick=0,
                actor_id="system",
            )
        ],
    )
    processor.state.add_metric(raw_power_concentration(processor.state, 0, 0))
    processor.state.add_metric(
        MetricRecord(
            metric_id="custom_metric",
            formula_id="SIM-FORMULA-CUSTOM",
            window_start_tick=0,
            window_end_tick=1,
            value=2,
            unit="count",
        )
    )
    return processor


def test_write_run_outputs_creates_required_artifacts() -> None:
    processor = build_output_state()
    report = ValidationReport()
    report.warning("test.warning", "non-blocking warning")
    report.notice("test.notice", "simulation abstraction notice")
    context = RunOutputContext(
        scenario_id="phase5-output-test",
        scenario_version="0.1.0",
        random_seed=123,
        start_tick=0,
        end_tick=1,
        start_date=date(2026, 1, 1),
        charter_derivative_path="derivatives/simulation/charter_sim.yaml",
        scenario_hash="scenario-hash",
        charter_derivative_hash="charter-hash",
        event_ordering_policy=processor.event_ordering_policy(),
    )

    paths = write_run_outputs(OUTPUT_DIR, processor.state, report, context)

    for path in paths.to_dict().values():
        assert Path(path).exists()


def test_manifest_contains_replay_provenance() -> None:
    processor = build_output_state()
    context = RunOutputContext(
        scenario_id="phase5-output-test",
        scenario_version="0.1.0",
        random_seed=123,
        start_tick=0,
        end_tick=1,
        scenario_hash="scenario-hash",
        charter_derivative_hash="charter-hash",
    )

    paths = write_run_outputs(OUTPUT_DIR, processor.state, ValidationReport(), context)
    manifest = json.loads(paths.manifest.read_text(encoding="utf-8"))

    assert manifest["scenario_id"] == "phase5-output-test"
    assert manifest["random_seed"] == 123
    assert manifest["scenario_hash"] == "scenario-hash"
    assert manifest["charter_derivative_hash"] == "charter-hash"
    assert len(manifest["final_state_hash"]) == 64


def test_manifest_lists_enabled_rules() -> None:
    processor = build_output_state()
    context = RunOutputContext(
        scenario_id="phase5-output-test",
        scenario_version="0.1.0",
        random_seed=123,
        start_tick=0,
        end_tick=1,
        enabled_rules=enabled_rule_manifest(["satisfaction_metric"]),
    )

    paths = write_run_outputs(OUTPUT_DIR, processor.state, ValidationReport(), context)
    manifest = json.loads(paths.manifest.read_text(encoding="utf-8"))

    charter_rule_ids = {
        rule["rule_id"] for rule in manifest["enabled_rules"]["charter_derived"]
    }
    abstraction_labels = {
        rule["abstraction_label"]
        for rule in manifest["enabled_rules"]["simulation_abstractions"]
    }

    assert "SIM-RULE-AUTHORITY-FORMATION" in charter_rule_ids
    assert "SIM-RULE-DELEGATION-CREATE" in charter_rule_ids
    assert "event_noop" in abstraction_labels
    assert "satisfaction_metric" in abstraction_labels


def test_event_and_decision_logs_are_json_lines() -> None:
    processor = build_output_state()
    paths = write_run_outputs(
        OUTPUT_DIR,
        processor.state,
        ValidationReport(),
        RunOutputContext(
            scenario_id="phase5-output-test",
            scenario_version="0.1.0",
            random_seed=123,
            start_tick=0,
            end_tick=1,
        ),
    )

    event_rows = [
        json.loads(line)
        for line in paths.event_log.read_text(encoding="utf-8").splitlines()
    ]
    decision_rows = [
        json.loads(line)
        for line in paths.rule_decisions.read_text(encoding="utf-8").splitlines()
    ]

    assert event_rows[0]["event_id"] == "event-000001"
    assert decision_rows[0]["decision_id"] == "decision-000001"
    assert len(decision_rows[0]["input_state_hash"]) == 64
    assert len(decision_rows[0]["output_state_hash"]) == 64


def test_final_state_includes_core_and_placeholder_sections() -> None:
    processor = build_output_state()
    paths = write_run_outputs(
        OUTPUT_DIR,
        processor.state,
        ValidationReport(),
        RunOutputContext(
            scenario_id="phase5-output-test",
            scenario_version="0.1.0",
            random_seed=123,
            start_tick=0,
            end_tick=1,
        ),
    )

    final_state = json.loads(paths.final_state.read_text(encoding="utf-8"))

    assert "subscribers" in final_state
    assert "representatives" in final_state
    assert "delegations" in final_state
    assert "authorities" in final_state
    assert final_state["active_emergencies"] == []
    assert final_state["pending_reviews"] == []
    assert final_state["unresolved_conflicts"] == []


def test_metrics_summary_and_time_series_schema() -> None:
    processor = build_output_state()
    paths = write_run_outputs(
        OUTPUT_DIR,
        processor.state,
        ValidationReport(),
        RunOutputContext(
            scenario_id="phase5-output-test",
            scenario_version="0.1.0",
            random_seed=123,
            start_tick=0,
            end_tick=1,
            start_date=date(2026, 1, 1),
        ),
    )

    metrics = json.loads(paths.metrics_summary.read_text(encoding="utf-8"))["metrics"]
    with paths.time_series.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    assert metrics[0]["metric_name"] == "raw_power_concentration"
    assert metrics[0]["calculation_source"] == "SIM-FORMULA-RAW-POWER-CONCENTRATION"
    assert rows[0] == {
        "tick": "0",
        "calendar_date": "2026-01-01",
        "metric_name": "raw_power_concentration",
        "value": "0.0",
    }


def test_validation_report_distinguishes_issue_severity() -> None:
    report = ValidationReport()
    report.error("blocking", "blocking error")
    report.warning("warning", "non-blocking warning")
    report.notice("notice", "simulation abstraction notice")
    processor = build_output_state()

    paths = write_run_outputs(
        OUTPUT_DIR,
        processor.state,
        report,
        RunOutputContext(
            scenario_id="phase5-output-test",
            scenario_version="0.1.0",
            random_seed=123,
            start_tick=0,
            end_tick=1,
        ),
    )

    validation = json.loads(paths.validation_report.read_text(encoding="utf-8"))
    severities = {issue["severity"] for issue in validation["issues"]}

    assert severities == {
        ValidationSeverity.ERROR.value,
        ValidationSeverity.WARNING.value,
        ValidationSeverity.NOTICE.value,
    }
