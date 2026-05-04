"""Narrow first-pass metric formulas."""

from __future__ import annotations

from .records import AuthorityLifecycleState, MetricRecord
from .state import SimulationState


ACTIVE_COUNTED_AUTHORITY_STATES = {
    AuthorityLifecycleState.ACTIVE,
    AuthorityLifecycleState.UNDER_REVIEW,
    AuthorityLifecycleState.REAUTHORIZATION_REQUIRED,
    AuthorityLifecycleState.SUSPENDED,
}


def raw_power_concentration(
    state: SimulationState, window_start_tick: int, window_end_tick: int
) -> MetricRecord:
    active_tokens = sum(1 for subscriber in state.subscribers.values() if subscriber.active_status)
    max_raw = max(
        (representative.raw_delegation_total for representative in state.representatives.values()),
        default=0.0,
    )
    value = 0.0 if active_tokens == 0 else max_raw / active_tokens
    return MetricRecord(
        metric_id="raw_power_concentration",
        formula_id="SIM-FORMULA-RAW-POWER-CONCENTRATION",
        window_start_tick=window_start_tick,
        window_end_tick=window_end_tick,
        value=value,
        unit="share",
    )


def delegation_churn(
    state: SimulationState, window_start_tick: int, window_end_tick: int
) -> MetricRecord:
    active_subscribers = sum(
        1 for subscriber in state.subscribers.values() if subscriber.active_status
    )
    churn_events = sum(
        1
        for event in state.events.values()
        if window_start_tick <= event.effective_tick <= window_end_tick
        and event.event_type
        in {"delegation_create", "delegation_revoke", "delegation_transfer"}
    )
    value = "not_applicable" if active_subscribers == 0 else churn_events / active_subscribers
    reason = "active_subscriber_count is zero" if active_subscribers == 0 else None
    return MetricRecord(
        metric_id="delegation_churn",
        formula_id="SIM-FORMULA-DELEGATION-CHURN",
        window_start_tick=window_start_tick,
        window_end_tick=window_end_tick,
        value=value,
        unit="events_per_active_subscriber",
        not_applicable_reason=reason,
    )


def authority_count(
    state: SimulationState, window_start_tick: int, window_end_tick: int
) -> MetricRecord:
    count = sum(
        1
        for authority in state.authorities.values()
        if authority.lifecycle_status in ACTIVE_COUNTED_AUTHORITY_STATES
    )
    return MetricRecord(
        metric_id="authority_count",
        formula_id="SIM-FORMULA-AUTHORITY-COUNT",
        window_start_tick=window_start_tick,
        window_end_tick=window_end_tick,
        value=count,
        unit="authorities",
    )


def lifecycle_transition_count(
    state: SimulationState,
    to_state: AuthorityLifecycleState,
    window_start_tick: int,
    window_end_tick: int,
) -> MetricRecord:
    count = sum(
        1
        for decision in state.rule_decisions
        if window_start_tick <= decision.decision_tick <= window_end_tick
        and f"to_state={to_state.value}" in decision.reason
    )
    return MetricRecord(
        metric_id=f"authority_lifecycle_transitions_to_{to_state.value}",
        formula_id="SIM-FORMULA-AUTHORITY-LIFECYCLE-OUTCOMES",
        window_start_tick=window_start_tick,
        window_end_tick=window_end_tick,
        value=count,
        unit="transitions",
    )
