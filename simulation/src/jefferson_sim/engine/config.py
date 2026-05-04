"""Configuration loading and validation for Charter simulation inputs."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

import yaml

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


def _validate_required_fields(
    report: ValidationReport,
    data: dict[str, Any],
    required_fields: set[str],
    code: str,
) -> None:
    for field_name in sorted(required_fields):
        if field_name not in data:
            report.error(code, f"missing required field: {field_name}", field_name)
