"""Local output artifact writer for simulation runs."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date, timedelta
import json
from pathlib import Path
from typing import Any

from jefferson_sim import __version__

from .records import MetricRecord, RuleDecision, SimulationEvent, to_primitive
from .state import SimulationState
from .validation import ValidationReport


OUTPUT_FILENAMES = {
    "manifest": "manifest.json",
    "validation_report": "validation_report.json",
    "event_log": "event_log.jsonl",
    "rule_decisions": "rule_decisions.jsonl",
    "metrics_summary": "metrics_summary.json",
    "time_series": "time_series.csv",
    "final_state": "final_state.json",
}


@dataclass(slots=True)
class OutputArtifactPaths:
    manifest: Path
    validation_report: Path
    event_log: Path
    rule_decisions: Path
    metrics_summary: Path
    time_series: Path
    final_state: Path

    def to_dict(self) -> dict[str, str]:
        return {key: str(value) for key, value in to_primitive(self).items()}


@dataclass(slots=True)
class RunOutputContext:
    scenario_id: str
    scenario_version: str
    random_seed: int
    start_tick: int
    end_tick: int
    tick_duration: str = "day"
    start_date: date = date(2000, 1, 1)
    charter_derivative_path: str | None = None
    scenario_hash: str | None = None
    charter_derivative_hash: str | None = None
    event_ordering_policy: dict[str, int] | None = None
    enabled_rules: dict[str, list[dict[str, Any]]] | None = None
    extra_provenance: dict[str, Any] | None = None

    def to_manifest_dict(
        self, state: SimulationState, paths: OutputArtifactPaths
    ) -> dict[str, Any]:
        return {
            "scenario_id": self.scenario_id,
            "scenario_version": self.scenario_version,
            "engine_version": __version__,
            "random_seed": self.random_seed,
            "tick_duration": self.tick_duration,
            "start_tick": self.start_tick,
            "end_tick": self.end_tick,
            "start_date": self.start_date.isoformat(),
            "charter_derivative_path": self.charter_derivative_path,
            "scenario_hash": self.scenario_hash,
            "charter_derivative_hash": self.charter_derivative_hash,
            "event_ordering_policy": self.event_ordering_policy or {},
            "enabled_rules": self.enabled_rules
            or {"charter_derived": [], "simulation_abstractions": []},
            "final_state_hash": state.state_hash(),
            "output_artifacts": {
                key: Path(path).name for key, path in paths.to_dict().items()
            },
            "extra_provenance": self.extra_provenance or {},
        }


def write_run_outputs(
    output_dir: Path | str,
    state: SimulationState,
    validation_report: ValidationReport,
    context: RunOutputContext,
) -> OutputArtifactPaths:
    target_dir = Path(output_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    paths = OutputArtifactPaths(
        manifest=target_dir / OUTPUT_FILENAMES["manifest"],
        validation_report=target_dir / OUTPUT_FILENAMES["validation_report"],
        event_log=target_dir / OUTPUT_FILENAMES["event_log"],
        rule_decisions=target_dir / OUTPUT_FILENAMES["rule_decisions"],
        metrics_summary=target_dir / OUTPUT_FILENAMES["metrics_summary"],
        time_series=target_dir / OUTPUT_FILENAMES["time_series"],
        final_state=target_dir / OUTPUT_FILENAMES["final_state"],
    )

    _write_json(paths.manifest, context.to_manifest_dict(state, paths))
    _write_json(paths.validation_report, validation_report.to_dict())
    _write_jsonl(paths.event_log, state.events.values())
    _write_jsonl(paths.rule_decisions, state.rule_decisions)
    _write_json(paths.metrics_summary, _metrics_summary(state.metrics))
    _write_time_series(paths.time_series, state.metrics, context)
    _write_json(paths.final_state, _final_state_payload(state))
    return paths


def _final_state_payload(state: SimulationState) -> dict[str, Any]:
    payload = state.to_dict()
    payload.setdefault("active_emergencies", [])
    payload.setdefault("pending_reviews", [])
    payload.setdefault("unresolved_conflicts", [])
    payload["state_hash"] = state.state_hash()
    return payload


def _metrics_summary(metrics: list[MetricRecord]) -> dict[str, Any]:
    return {
        "metrics": [
            {
                "metric_name": metric.metric_id,
                "value": metric.value,
                "unit": metric.unit,
                "calculation_window": {
                    "start_tick": metric.window_start_tick,
                    "end_tick": metric.window_end_tick,
                },
                "calculation_source": metric.formula_id,
                "not_applicable_reason": metric.not_applicable_reason,
            }
            for metric in metrics
        ]
    }


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(to_primitive(payload), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _write_jsonl(path: Path, records: Any) -> None:
    lines = [json.dumps(to_primitive(record), sort_keys=True) for record in _ordered(records)]
    path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")


def _ordered(records: Any) -> list[Any]:
    if isinstance(records, dict):
        return [records[key] for key in sorted(records)]
    values = list(records)
    if all(isinstance(item, SimulationEvent) for item in values):
        return sorted(values, key=lambda item: item.event_id)
    if all(isinstance(item, RuleDecision) for item in values):
        return sorted(values, key=lambda item: item.decision_id)
    return values


def _write_time_series(
    path: Path, metrics: list[MetricRecord], context: RunOutputContext
) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=["tick", "calendar_date", "metric_name", "value"]
        )
        writer.writeheader()
        for metric in metrics:
            writer.writerow(
                {
                    "tick": metric.window_end_tick,
                    "calendar_date": _calendar_date_for_tick(
                        metric.window_end_tick, context
                    ),
                    "metric_name": metric.metric_id,
                    "value": metric.value,
                }
            )


def _calendar_date_for_tick(tick: int, context: RunOutputContext) -> str:
    if context.tick_duration != "day":
        return f"tick-{tick}"
    return (context.start_date + timedelta(days=tick - context.start_tick)).isoformat()
