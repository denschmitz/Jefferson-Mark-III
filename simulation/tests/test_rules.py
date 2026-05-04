from jefferson_sim.engine import RuleMetadata, ValidationSeverity, validate_rule_metadata


def test_charter_traced_rule_metadata_is_valid() -> None:
    rule = RuleMetadata(
        rule_id="authority_formation_coercive_threshold",
        source_document="charter/charter.md",
        source_article="Article II",
        source_section="2",
        source_clause="a",
        derivative_path="authority_rules.formation_thresholds.coercive",
    )

    report = validate_rule_metadata(rule)

    assert not report.has_errors


def test_rule_without_traceability_fails() -> None:
    rule = RuleMetadata(rule_id="missing_trace")

    report = validate_rule_metadata(rule)

    assert report.has_errors
    assert any(issue.code == "rule.traceability.missing" for issue in report.issues)


def test_yaml_derivative_rule_requires_derivative_path() -> None:
    rule = RuleMetadata(
        rule_id="yaml_rule",
        source_document="derivatives/simulation/charter_sim.yaml",
        source_article="authority_rules",
        source_section="formation_thresholds",
        source_clause="coercive",
    )

    report = validate_rule_metadata(rule)

    assert report.has_errors
    assert any(issue.code == "rule.derivative_path.missing" for issue in report.issues)


def test_abstraction_rule_emits_notice() -> None:
    rule = RuleMetadata(
        rule_id="satisfaction_metric_abstraction",
        abstraction_label="satisfaction_metric",
        abstraction_rationale="Charter does not define measurement mechanics.",
    )

    report = validate_rule_metadata(rule)

    assert not report.has_errors
    assert any(issue.severity == ValidationSeverity.NOTICE for issue in report.issues)
