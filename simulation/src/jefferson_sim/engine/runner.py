"""Minimal deterministic scenario runner for first-pass acceptance scenarios."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Any

from .config import ScenarioConfig, load_scenario
from .events import EventInput, EventProcessor
from .metrics import authority_count, delegation_churn, raw_power_concentration
from .outputs import OutputArtifactPaths, RunOutputContext, write_run_outputs
from .records import (
    ApprovalRecord,
    AuthorityCharterRecord,
    DelegationRecord,
    DelegationStatus,
    RepresentativeRecord,
    ScopeRecord,
    SubscriberRecord,
    ThresholdResult,
    to_primitive,
)
from .state import SimulationState


@dataclass(slots=True)
class ScenarioRunResult:
    scenario_id: str
    processor: EventProcessor
    final_state_hash: str
    output_paths: OutputArtifactPaths | None = None


def run_scenario_file(path: str | Path, write_outputs: bool = True) -> ScenarioRunResult:
    scenario = load_scenario(path)
    scenario.validation_report.assert_valid()
    return run_scenario_config(scenario, write_outputs=write_outputs)


def run_scenario_config(
    scenario: ScenarioConfig, write_outputs: bool = True
) -> ScenarioRunResult:
    state = _state_from_scenario(scenario.data)
    processor = EventProcessor(state)
    duration = int(scenario.data["duration"])
    scheduled_events = _scheduled_events_by_tick(scenario.data.get("event_schedule", []))

    for tick in range(0, duration + 1):
        processor.submit_events(tick, scheduled_events.get(tick, []))

    _add_summary_metrics(processor.state, 0, duration)

    output_paths = None
    if write_outputs:
        output_paths = write_run_outputs(
            scenario.data["output_path"],
            processor.state,
            processor.validation_report,
            _output_context(scenario, processor, duration),
        )

    return ScenarioRunResult(
        scenario_id=str(scenario.data["scenario_id"]),
        processor=processor,
        final_state_hash=processor.state.state_hash(),
        output_paths=output_paths,
    )


def _state_from_scenario(data: dict[str, Any]) -> SimulationState:
    state = SimulationState()
    initial_state = data.get("initial_state", {})
    if not isinstance(initial_state, dict):
        return state

    for record in initial_state.get("subscribers", []):
        state.add_subscriber(
            SubscriberRecord(
                subscriber_id=str(record["subscriber_id"]),
                token_id=str(record["token_id"]),
                active_status=bool(record.get("active_status", True)),
                group_ids=list(record.get("group_ids", [])),
            )
        )

    for record in initial_state.get("representatives", []):
        state.add_representative(
            RepresentativeRecord(
                representative_id=str(record["representative_id"]),
                subscriber_id=str(record["subscriber_id"]),
                raw_delegation_total=float(record.get("raw_delegation_total", 0.0)),
                weighted_delegation_total=record.get("weighted_delegation_total"),
                coalition_id=record.get("coalition_id"),
            )
        )

    for record in initial_state.get("approval_records", []):
        state.add_approval_record(
            ApprovalRecord(
                approval_record_id=str(record["approval_record_id"]),
                decision_type=str(record["decision_type"]),
                subject_id=str(record["subject_id"]),
                electorate_basis=str(record["electorate_basis"]),
                eligible_count=int(record["eligible_count"]),
                approval_count=int(record["approval_count"]),
                rejection_count=int(record["rejection_count"]),
                abstention_count=int(record["abstention_count"]),
                approval_ratio=float(record["approval_ratio"]),
                threshold_required=float(record["threshold_required"]),
                threshold_result=ThresholdResult(str(record["threshold_result"])),
                snapshot_tick=int(record["snapshot_tick"]),
                assumptions_used=list(record.get("assumptions_used", [])),
            )
        )

    for record in initial_state.get("scopes", []):
        state.add_scope(
            ScopeRecord(
                scope_id=str(record["scope_id"]),
                function=str(record["function"]),
                territory=list(record.get("territory", [])),
                population_affected=list(record.get("population_affected", [])),
                permitted_powers=list(record.get("permitted_powers", [])),
                prohibited_powers=list(record.get("prohibited_powers", [])),
                resource_authority=list(record.get("resource_authority", [])),
                enforcement_authority=list(record.get("enforcement_authority", [])),
                review_interval=record.get("review_interval"),
                emergency_powers=list(record.get("emergency_powers", [])),
                authority_references=list(record.get("authority_references", [])),
            )
        )

    for record in initial_state.get("authority_charters", []):
        state.add_authority_charter(
            AuthorityCharterRecord(
                charter_id=str(record["charter_id"]),
                scope_id=str(record["scope_id"]),
                funding_sources=list(record["funding_sources"]),
                renewal_process=str(record["renewal_process"]),
                oversight_structures=list(record["oversight_structures"]),
                formation_threshold=float(record["formation_threshold"]),
                approval_record_id=str(record["approval_record_id"]),
            )
        )

    for record in initial_state.get("delegations", []):
        state.add_delegation(
            DelegationRecord(
                delegation_id=str(record["delegation_id"]),
                source_subscriber_id=str(record["source_subscriber_id"]),
                target_representative_id=str(record["target_representative_id"]),
                token_share=float(record["token_share"]),
                submitted_tick=int(record["submitted_tick"]),
                activation_tick=int(record["activation_tick"]),
                status=DelegationStatus(str(record.get("status", "pending"))),
                reason=record.get("reason"),
            )
        )

    return state


def _scheduled_events_by_tick(events: list[dict[str, Any]]) -> dict[int, list[EventInput]]:
    scheduled: dict[int, list[EventInput]] = {}
    for event in events:
        submitted_tick = int(event.get("submitted_tick", event["effective_tick"]))
        effective_tick = int(event["effective_tick"])
        scheduled.setdefault(submitted_tick, []).append(
            EventInput(
                event_type=str(event["event_type"]),
                submitted_tick=submitted_tick,
                effective_tick=effective_tick,
                actor_id=str(event["actor_id"]),
                target_id=event.get("target_id"),
                payload=dict(event.get("payload", {})),
                provenance=dict(event.get("provenance", {})),
                event_id=event.get("event_id"),
            )
        )
    return scheduled


def _add_summary_metrics(state: SimulationState, start_tick: int, end_tick: int) -> None:
    state.add_metric(raw_power_concentration(state, start_tick, end_tick))
    state.add_metric(delegation_churn(state, start_tick, end_tick))
    state.add_metric(authority_count(state, start_tick, end_tick))


def _output_context(
    scenario: ScenarioConfig, processor: EventProcessor, duration: int
) -> RunOutputContext:
    data = scenario.data
    charter_derivative_path = str(data.get("charter_derivative_path"))
    return RunOutputContext(
        scenario_id=str(data["scenario_id"]),
        scenario_version=str(data["scenario_version"]),
        random_seed=int(data["random_seed"]),
        start_tick=0,
        end_tick=duration,
        tick_duration=str(data.get("tick_duration", "day")),
        charter_derivative_path=charter_derivative_path,
        scenario_hash=_hash_mapping(data),
        charter_derivative_hash=_hash_file_if_present(scenario.path.parent, charter_derivative_path),
        event_ordering_policy=processor.event_ordering_policy(),
    )


def _hash_mapping(data: dict[str, Any]) -> str:
    payload = json.dumps(to_primitive(data), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _hash_file_if_present(base_path: Path, configured_path: str) -> str | None:
    path = Path(configured_path)
    candidates = [path, base_path / path]
    for candidate in candidates:
        if candidate.exists():
            return hashlib.sha256(candidate.read_bytes()).hexdigest()
    return None
