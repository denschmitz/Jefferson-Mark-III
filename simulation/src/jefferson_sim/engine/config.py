"""Configuration loading and validation for Charter simulation inputs."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

import yaml

from .events import KNOWN_EVENT_TYPES
from .validation import ValidationReport


class ConfigLoadError(ValueError):
    """Raised when a config file cannot be loaded."""


REQUIRED_CHARTER_DERIVATIVE_FIELDS = {
    "meta",
    "polity",
    "actors",
    "authority_rules",
    "legislation",
    "emergency",
    "representation",
    "rights",
    "supremacy_and_transition",
    "known_simulation_gaps",
}

REQUIRED_SCENARIO_FIELDS = {
    "scenario_id",
    "scenario_version",
    "charter_derivative_path",
    "random_seed",
    "duration",
    "tick_duration",
    "output_path",
    "population_size",
    "agent_distributions",
    "output_settings",
}

SCENARIO_TEXT_FIELDS = {
    "scenario_id",
    "scenario_version",
    "charter_derivative_path",
    "tick_duration",
    "output_path",
}

INITIAL_STATE_COLLECTION_FIELDS = {
    "subscribers": {"subscriber_id", "token_id"},
    "representatives": {"representative_id", "subscriber_id"},
    "approval_records": {
        "approval_record_id",
        "decision_type",
        "subject_id",
        "electorate_basis",
        "eligible_count",
        "approval_count",
        "rejection_count",
        "abstention_count",
        "approval_ratio",
        "threshold_required",
        "threshold_result",
        "snapshot_tick",
    },
    "scopes": {"scope_id", "function"},
    "authority_charters": {
        "charter_id",
        "scope_id",
        "funding_sources",
        "renewal_process",
        "oversight_structures",
        "formation_threshold",
        "approval_record_id",
    },
    "authorities": {
        "authority_id",
        "charter_id",
        "authority_type",
        "coercive_status",
        "scope_id",
    },
    "delegations": {
        "delegation_id",
        "source_subscriber_id",
        "target_representative_id",
        "token_share",
        "submitted_tick",
        "activation_tick",
    },
}

EVENT_SCHEDULE_REQUIRED_FIELDS = {
    "event_type",
    "effective_tick",
    "actor_id",
}


@dataclass(frozen=True, slots=True)
class CharterDerivativeConfig:
    path: Path
    data: dict[str, Any]
    validation_report: ValidationReport


@dataclass(frozen=True, slots=True)
class ScenarioConfig:
    path: Path
    data: dict[str, Any]
    validation_report: ValidationReport


def load_structured_file(path: str | Path) -> dict[str, Any]:
    resolved = Path(path)
    try:
        text = resolved.read_text(encoding="utf-8")
    except OSError as exc:
        raise ConfigLoadError(f"cannot read config file: {resolved}") from exc

    suffix = resolved.suffix.lower()
    try:
        if suffix in {".yaml", ".yml"}:
            data = yaml.safe_load(text)
        elif suffix == ".json":
            data = json.loads(text)
        else:
            raise ConfigLoadError(f"unsupported config file extension: {suffix}")
    except (yaml.YAMLError, json.JSONDecodeError) as exc:
        raise ConfigLoadError(f"cannot parse config file: {resolved}") from exc

    if not isinstance(data, dict):
        raise ConfigLoadError(f"config root must be a mapping: {resolved}")
    return data


def load_charter_derivative(path: str | Path) -> CharterDerivativeConfig:
    resolved = Path(path)
    data = load_structured_file(resolved)
    report = validate_charter_derivative(data)
    return CharterDerivativeConfig(path=resolved, data=data, validation_report=report)


def load_scenario(path: str | Path) -> ScenarioConfig:
    resolved = Path(path)
    data = load_structured_file(resolved)
    report = validate_scenario(data)
    return ScenarioConfig(path=resolved, data=data, validation_report=report)


def validate_charter_derivative(data: dict[str, Any]) -> ValidationReport:
    report = ValidationReport()

    _validate_required_fields(
        report=report,
        data=data,
        required_fields=REQUIRED_CHARTER_DERIVATIVE_FIELDS,
        code="charter_derivative.missing_field",
    )

    meta = data.get("meta")
    if not isinstance(meta, dict):
        report.error("charter_derivative.meta.invalid", "meta must be a mapping", "meta")
        return report

    if meta.get("source") != "charter/charter.md":
        report.error(
            "charter_derivative.source.invalid",
            "meta.source must be charter/charter.md",
            "meta.source",
        )

    if meta.get("derivative_type") != "rules_configuration":
        report.warning(
            "charter_derivative.derivative_type.unexpected",
            "meta.derivative_type is expected to be rules_configuration",
            "meta.derivative_type",
        )

    gaps = data.get("known_simulation_gaps")
    if not isinstance(gaps, list) or not gaps:
        report.error(
            "charter_derivative.gaps.missing",
            "known_simulation_gaps must be a non-empty list",
            "known_simulation_gaps",
        )

    return report


def validate_scenario(data: dict[str, Any]) -> ValidationReport:
    report = ValidationReport()

    _validate_required_fields(
        report=report,
        data=data,
        required_fields=REQUIRED_SCENARIO_FIELDS,
        code="scenario.missing_field",
    )

    for field_name in sorted(SCENARIO_TEXT_FIELDS):
        if field_name in data and not _is_non_empty_text(data[field_name]):
            report.error(
                f"scenario.{field_name}.invalid",
                f"{field_name} must be a non-empty string",
                field_name,
            )

    if "random_seed" in data and not isinstance(data["random_seed"], int):
        report.error("scenario.random_seed.invalid", "random_seed must be an integer", "random_seed")

    for field_name in ("duration", "population_size"):
        if field_name in data and (not isinstance(data[field_name], int) or data[field_name] <= 0):
            report.error(
                f"scenario.{field_name}.invalid",
                f"{field_name} must be a positive integer",
                field_name,
            )

    if "agent_distributions" in data and not isinstance(data["agent_distributions"], dict):
        report.error(
            "scenario.agent_distributions.invalid",
            "agent_distributions must be a mapping",
            "agent_distributions",
        )

    if "output_settings" in data and not isinstance(data["output_settings"], dict):
        report.error(
            "scenario.output_settings.invalid",
            "output_settings must be a mapping",
            "output_settings",
        )

    _validate_initial_state(report, data.get("initial_state"))
    _validate_event_schedule(report, data.get("event_schedule"))

    required_gap_assumptions = data.get("required_gap_assumptions", [])
    gap_assumptions = data.get("gap_assumptions", {})
    if required_gap_assumptions and not isinstance(required_gap_assumptions, list):
        report.error(
            "scenario.required_gap_assumptions.invalid",
            "required_gap_assumptions must be a list",
            "required_gap_assumptions",
        )
    if gap_assumptions and not isinstance(gap_assumptions, dict):
        report.error("scenario.gap_assumptions.invalid", "gap_assumptions must be a mapping", "gap_assumptions")

    if isinstance(required_gap_assumptions, list) and isinstance(gap_assumptions, dict):
        for gap_id in required_gap_assumptions:
            if gap_id not in gap_assumptions:
                report.error(
                    "scenario.gap_assumption.missing",
                    f"required gap assumption is not declared: {gap_id}",
                    f"gap_assumptions.{gap_id}",
                )

    abstractions = data.get("simulation_abstractions", [])
    if abstractions:
        if not isinstance(abstractions, list):
            report.error(
                "scenario.simulation_abstractions.invalid",
                "simulation_abstractions must be a list",
                "simulation_abstractions",
            )
        else:
            for abstraction in abstractions:
                report.notice(
                    "scenario.simulation_abstraction.enabled",
                    f"simulation abstraction enabled: {abstraction}",
                    "simulation_abstractions",
                )

    return report


def _validate_initial_state(report: ValidationReport, initial_state: Any) -> None:
    if initial_state is None:
        return
    if not isinstance(initial_state, dict):
        report.error(
            "scenario.initial_state.invalid",
            "initial_state must be a mapping",
            "initial_state",
        )
        return

    for collection_name, required_fields in INITIAL_STATE_COLLECTION_FIELDS.items():
        if collection_name not in initial_state:
            continue
        collection = initial_state[collection_name]
        collection_path = f"initial_state.{collection_name}"
        if not isinstance(collection, list):
            report.error(
                "scenario.initial_state.collection.invalid",
                f"{collection_path} must be a list",
                collection_path,
            )
            continue
        for index, record in enumerate(collection):
            record_path = f"{collection_path}.{index}"
            if not isinstance(record, dict):
                report.error(
                    "scenario.initial_state.record.invalid",
                    f"{record_path} must be a mapping",
                    record_path,
                )
                continue
            for field_name in sorted(required_fields):
                if field_name not in record:
                    report.error(
                        "scenario.initial_state.record.missing_field",
                        f"missing required field: {field_name}",
                        f"{record_path}.{field_name}",
                    )


def _validate_event_schedule(report: ValidationReport, event_schedule: Any) -> None:
    if event_schedule is None:
        return
    if not isinstance(event_schedule, list):
        report.error(
            "scenario.event_schedule.invalid",
            "event_schedule must be a list",
            "event_schedule",
        )
        return

    for index, event in enumerate(event_schedule):
        event_path = f"event_schedule.{index}"
        if not isinstance(event, dict):
            report.error(
                "scenario.event_schedule.event.invalid",
                f"{event_path} must be a mapping",
                event_path,
            )
            continue
        for field_name in sorted(EVENT_SCHEDULE_REQUIRED_FIELDS):
            if field_name not in event:
                report.error(
                    "scenario.event_schedule.event.missing_field",
                    f"missing required field: {field_name}",
                    f"{event_path}.{field_name}",
                )
        _validate_event_schedule_text_field(report, event, event_path, "event_type")
        _validate_event_schedule_text_field(report, event, event_path, "actor_id")
        _validate_event_schedule_text_field(report, event, event_path, "target_id", required=False)
        _validate_non_negative_int_field(report, event, event_path, "submitted_tick", required=False)
        _validate_non_negative_int_field(report, event, event_path, "effective_tick")
        if "event_type" in event and isinstance(event["event_type"], str) and event["event_type"] not in KNOWN_EVENT_TYPES:
            report.error(
                "scenario.event_schedule.event_type.unknown",
                f"unknown event_type: {event['event_type']}",
                f"{event_path}.event_type",
            )
        for field_name in ("payload", "provenance"):
            if field_name in event and not isinstance(event[field_name], dict):
                report.error(
                    f"scenario.event_schedule.{field_name}.invalid",
                    f"{field_name} must be a mapping",
                    f"{event_path}.{field_name}",
                )


def _validate_event_schedule_text_field(
    report: ValidationReport,
    event: dict[str, Any],
    event_path: str,
    field_name: str,
    required: bool = True,
) -> None:
    if field_name not in event:
        return
    if event[field_name] is None and not required:
        return
    if not _is_non_empty_text(event[field_name]):
        report.error(
            f"scenario.event_schedule.{field_name}.invalid",
            f"{field_name} must be a non-empty string",
            f"{event_path}.{field_name}",
        )


def _validate_non_negative_int_field(
    report: ValidationReport,
    event: dict[str, Any],
    event_path: str,
    field_name: str,
    required: bool = True,
) -> None:
    if field_name not in event:
        return
    if event[field_name] is None and not required:
        return
    if not isinstance(event[field_name], int) or event[field_name] < 0:
        report.error(
            f"scenario.event_schedule.{field_name}.invalid",
            f"{field_name} must be a non-negative integer",
            f"{event_path}.{field_name}",
        )


def _is_non_empty_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value)


def _validate_required_fields(
    report: ValidationReport,
    data: dict[str, Any],
    required_fields: set[str],
    code: str,
) -> None:
    for field_name in sorted(required_fields):
        if field_name not in data:
            report.error(code, f"missing required field: {field_name}", field_name)
