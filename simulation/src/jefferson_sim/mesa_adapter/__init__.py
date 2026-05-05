"""Thin Mesa-facing boundary for the Charter simulation engine.

This module intentionally does not implement full Mesa agents yet. It provides
the first-test boundary: Mesa-facing code can queue engine events, advance a
tick, and receive engine rule decisions without mutating engine state directly
or duplicating Charter rule logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from jefferson_sim.engine import (
    EventInput,
    EventProcessor,
    RuleDecision,
    SimulationState,
    TickProcessingResult,
)
from jefferson_sim.engine.records import to_primitive


__version__ = "0.1.0-boundary"


@dataclass(slots=True)
class MesaBoundaryStepResult:
    tick: int
    processing_result: TickProcessingResult
    decisions: list[RuleDecision] = field(default_factory=list)


class CharterMesaModel:
    """Minimal Mesa-facing model boundary backed by the pure engine.

    The adapter owns event queueing and tick advancement. Charter decisions stay
    inside ``EventProcessor``.
    """

    def __init__(
        self,
        state: SimulationState | None = None,
        random_seed: int | None = None,
        start_tick: int = 0,
    ) -> None:
        self.processor = EventProcessor(state)
        self.random_seed = random_seed
        self.current_tick = start_tick
        self._queued_events: list[EventInput] = []

    def queue_event(self, event: EventInput) -> None:
        self._queued_events.append(event)

    def emit_event(
        self,
        event_type: str,
        actor_id: str,
        payload: dict[str, Any] | None = None,
        target_id: str | None = None,
        effective_tick: int | None = None,
        provenance: dict[str, Any] | None = None,
    ) -> None:
        tick = self.current_tick if effective_tick is None else effective_tick
        self.queue_event(
            EventInput(
                event_type=event_type,
                submitted_tick=self.current_tick,
                effective_tick=tick,
                actor_id=actor_id,
                target_id=target_id,
                payload=payload or {},
                provenance=provenance or {},
            )
        )

    def step(self) -> MesaBoundaryStepResult:
        queued_events = list(self._queued_events)
        self._queued_events.clear()
        result = self.processor.submit_events(self.current_tick, queued_events)
        decisions = [
            decision
            for decision in self.processor.state.rule_decisions
            if decision.decision_id in result.decision_ids
        ]
        step_result = MesaBoundaryStepResult(
            tick=self.current_tick,
            processing_result=result,
            decisions=decisions,
        )
        self.current_tick += 1
        return step_result

    def state_snapshot(self) -> dict[str, Any]:
        return to_primitive(self.processor.state.to_dict())

    @property
    def queued_event_count(self) -> int:
        return len(self._queued_events)


__all__ = [
    "__version__",
    "CharterMesaModel",
    "MesaBoundaryStepResult",
]
