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


DEFAULT_CHARTER_RULES: tuple[RuleMetadata, ...] = (
    RuleMetadata(
        rule_id="SIM-RULE-DELEGATION-CREATE",
        source_document="charter/charter.md",
        source_article="Article IV",
        source_section="Delegation",
        source_clause="voluntary reversible delegation",
        derivative_path="representation.delegation",
    ),
    RuleMetadata(
        rule_id="SIM-RULE-DELEGATION-REVOKE",
        source_document="charter/charter.md",
        source_article="Article IV",
        source_section="Delegation",
        source_clause="voluntary reversible delegation",
        derivative_path="representation.delegation",
    ),
    RuleMetadata(
        rule_id="SIM-RULE-DELEGATION-ACTIVATE",
        source_document="charter/charter.md",
        source_article="Article IV",
        source_section="Delegation",
        source_clause="representation token delegation",
        derivative_path="representation.delegation",
    ),
    RuleMetadata(
        rule_id="SIM-RULE-AUTHORITY-FORMATION",
        source_document="charter/charter.md",
        source_article="Article II",
        source_section="Authority Formation",
        source_clause="formation threshold",
        derivative_path="authority_rules.formation_thresholds",
    ),
)

DEFAULT_SIMULATION_ABSTRACTION_RULES: tuple[RuleMetadata, ...] = (
    RuleMetadata(
        rule_id="SIM-RULE-EVENT-NOOP",
        abstraction_label="event_noop",
        abstraction_rationale=(
            "First-pass engine records accepted events with no registered "
            "state-changing rule as auditable no-op decisions."
        ),
    ),
)


def simulation_abstraction_rule(label: str) -> RuleMetadata:
    return RuleMetadata(
        rule_id=f"SIM-ABSTRACTION-{_normalize_rule_label(label)}",
        abstraction_label=label,
        abstraction_rationale=(
            "Scenario declares this behavior as a simulation abstraction because "
            "the Charter does not define complete mechanics for it."
        ),
    )


def enabled_rule_manifest(
    scenario_abstractions: list[str] | None = None,
) -> dict[str, list[dict[str, Any]]]:
    abstraction_rules = list(DEFAULT_SIMULATION_ABSTRACTION_RULES)
    abstraction_rules.extend(
        simulation_abstraction_rule(label) for label in sorted(set(scenario_abstractions or []))
    )
    return {
        "charter_derived": [rule.to_dict() for rule in DEFAULT_CHARTER_RULES],
        "simulation_abstractions": [rule.to_dict() for rule in abstraction_rules],
    }


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


def _normalize_rule_label(label: str) -> str:
    return "".join(character if character.isalnum() else "_" for character in label.upper()).strip("_")
