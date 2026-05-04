"""Rule metadata and traceability validation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .records import to_primitive
from .validation import ValidationReport


@dataclass(frozen=True, slots=True)
class RuleMetadata:
    rule_id: str
    source_document: str | None = None
    source_article: str | None = None
    source_section: str | None = None
    source_clause: str | None = None
    derivative_path: str | None = None
    abstraction_label: str | None = None
    abstraction_rationale: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return to_primitive(self)


def validate_rule_metadata(rule: RuleMetadata) -> ValidationReport:
    report = ValidationReport()

    if not rule.rule_id:
        report.error("rule.rule_id.missing", "rule_id is required", "rule_id")

    has_charter_trace = all(
        (
            rule.source_document,
            rule.source_article,
            rule.source_section,
            rule.source_clause,
        )
    )
    has_abstraction_trace = bool(rule.abstraction_label and rule.abstraction_rationale)

    if not has_charter_trace and not has_abstraction_trace:
        report.error(
            "rule.traceability.missing",
            "rule must include Charter source traceability or simulation abstraction metadata",
            "rule",
        )

    if _is_yaml_derivative_rule(rule) and not rule.derivative_path:
        report.error(
            "rule.derivative_path.missing",
            "rules derived from charter_sim.yaml must include derivative_path",
            "derivative_path",
        )

    if has_abstraction_trace:
        report.notice(
            "rule.simulation_abstraction.enabled",
            f"simulation abstraction rule enabled: {rule.abstraction_label}",
            "abstraction_label",
        )

    return report


def _is_yaml_derivative_rule(rule: RuleMetadata) -> bool:
    if rule.derivative_path:
        return False
    source = rule.source_document or ""
    return source.endswith("charter_sim.yaml")
