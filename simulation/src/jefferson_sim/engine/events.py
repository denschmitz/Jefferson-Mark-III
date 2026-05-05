"""Deterministic event processing spine for the simulation engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable

from .approvals import approval_passes_threshold, authority_formation_threshold
from .lifecycle import can_execute_ordinary_action, transition_authority
from .records import (
    AuthorityLifecycleState,
    AuthorityRecord,
    DelegationRecord,
    DelegationStatus,
    EventStatus,
    RuleDecision,
    ScopeConflictClassification,
    ScopeConflictRecord,
    SimulationEvent,
)
from .state import SimulationState, StateValidationError
from .validation import ValidationReport


KNOWN_EVENT_TYPES = frozenset(
    {
        "authority_action",
        "authority_formation",
        "capture_attempt",
        "delegation_create",
        "delegation_revoke",
        "delegation_transfer",
        "emergency_declaration",
        "emergency_extension",
        "noop",
        "provisional_emergency",
        "review_request",
        "satisfaction_update",
        "scope_conflict",
        "vote",
    }
)

EVENT_PRIORITY = {
    "emergency_declaration": 10,
    "provisional_emergency": 20,
    "emergency_extension": 30,
    "review_request": 40,
    "authority_formation": 50,
    "authority_action": 60,
    "delegation_revoke": 70,
    "delegation_transfer": 80,
    "delegation_create": 90,
    "vote": 100,
    "satisfaction_update": 110,
    "scope_conflict": 120,
    "capture_attempt": 130,
    "noop": 900,
}

NO_OP_RULE_ID = "SIM-RULE-EVENT-NOOP"
DELEGATION_CREATE_RULE_ID = "SIM-RULE-DELEGATION-CREATE"
DELEGATION_REVOKE_RULE_ID = "SIM-RULE-DELEGATION-REVOKE"
DELEGATION_ACTIVATE_RULE_ID = "SIM-RULE-DELEGATION-ACTIVATE"
AUTHORITY_FORMATION_RULE_ID = "SIM-RULE-AUTHORITY-FORMATION"
AUTHORITY_ACTION_RULE_ID = "SIM-RULE-AUTHORITY-ACTION"
SCOPE_CONFLICT_RULE_ID = "SIM-RULE-SCOPE-CONFLICT"


@dataclass(slots=True)
class EventInput:
    event_type: str
    submitted_tick: int
    effective_tick: int
    actor_id: str
    target_id: str | None = None
    payload: dict[str, Any] = field(default_factory=dict)
    provenance: dict[str, Any] = field(default_factory=dict)
    event_id: str | None = None


@dataclass(slots=True)
class TickProcessingResult:
    tick: int
    accepted_event_ids: list[str] = field(default_factory=list)
    rejected_event_ids: list[str] = field(default_factory=list)
    decision_ids: list[str] = field(default_factory=list)
    state_hash: str = ""


class EventProcessor:
    """Process input events through a deterministic, auditable no-op rule spine."""

    def __init__(
        self,
        state: SimulationState | None = None,
        event_priority: dict[str, int] | None = None,
    ) -> None:
        self.state = state if state is not None else SimulationState()
        self.event_priority = event_priority if event_priority is not None else EVENT_PRIORITY
        self.validation_report = ValidationReport()
        self.state_hashes_by_tick: dict[int, str] = {}
        self._event_counter = len(self.state.events)
        self._decision_counter = len(self.state.rule_decisions)

    def submit_events(self, tick: int, inputs: Iterable[EventInput]) -> TickProcessingResult:
        events = [self._materialize_event(item) for item in inputs]
        result = TickProcessingResult(tick=tick)

        for event in events:
            if self._validate_event(event):
                event.status = EventStatus.ACCEPTED
                result.accepted_event_ids.append(event.event_id)
            else:
                event.status = EventStatus.REJECTED
                result.rejected_event_ids.append(event.event_id)
            self._store_event(event)

        for event in self._events_to_process(tick):
            decision = self._process_event(event, tick)
            result.decision_ids.append(decision.decision_id)

        for decision in self._activate_due_delegations(tick):
            result.decision_ids.append(decision.decision_id)

        result.state_hash = self.state.state_hash()
        self.state_hashes_by_tick[tick] = result.state_hash
        return result

    def replay(self, events_by_tick: dict[int, Iterable[EventInput]]) -> str:
        for tick in sorted(events_by_tick):
            self.submit_events(tick, events_by_tick[tick])
        return self.state.state_hash()

    def event_ordering_policy(self) -> dict[str, int]:
        return dict(sorted(self.event_priority.items(), key=lambda item: (item[1], item[0])))

    def _materialize_event(self, item: EventInput) -> SimulationEvent:
        event_id = item.event_id or self._next_event_id()
        return SimulationEvent(
            event_id=event_id,
            event_type=item.event_type,
            submitted_tick=item.submitted_tick,
            effective_tick=item.effective_tick,
            actor_id=item.actor_id,
            target_id=item.target_id,
            payload=dict(item.payload),
            provenance=dict(item.provenance),
        )

    def _validate_event(self, event: SimulationEvent) -> bool:
        valid = True
        if event.event_type not in KNOWN_EVENT_TYPES:
            self.validation_report.error(
                "event.type.unknown",
                f"Unknown event type: {event.event_type}",
                path=f"events.{event.event_id}.event_type",
            )
            valid = False
        if event.effective_tick < event.submitted_tick:
            self.validation_report.error(
                "event.effective_tick.before_submitted_tick",
                "Event effective_tick cannot precede submitted_tick",
                path=f"events.{event.event_id}.effective_tick",
            )
            valid = False
        if event.event_id in self.state.events:
            self.validation_report.error(
                "event.event_id.duplicate",
                f"Duplicate event_id: {event.event_id}",
                path=f"events.{event.event_id}.event_id",
            )
            valid = False
        return valid

    def _store_event(self, event: SimulationEvent) -> None:
        try:
            self.state.add_event(event)
        except StateValidationError:
            replacement = SimulationEvent(
                event_id=self._next_event_id(),
                event_type=event.event_type,
                submitted_tick=event.submitted_tick,
                effective_tick=event.effective_tick,
                actor_id=event.actor_id,
                target_id=event.target_id,
                payload=dict(event.payload),
                status=EventStatus.REJECTED,
                provenance={**event.provenance, "duplicate_event_id": event.event_id},
            )
            self.validation_report.error(
                "event.event_id.duplicate",
                f"Duplicate event_id: {event.event_id}",
                path=f"events.{event.event_id}.event_id",
            )
            self.state.add_event(replacement)

    def _events_to_process(self, tick: int) -> list[SimulationEvent]:
        return sorted(
            [
                event
                for event in self.state.events.values()
                if event.status == EventStatus.ACCEPTED and event.effective_tick <= tick
            ],
            key=lambda event: (
                event.effective_tick,
                self.event_priority.get(event.event_type, 10_000),
                event.event_id,
            ),
        )

    def _process_event(self, event: SimulationEvent, tick: int) -> RuleDecision:
        if event.event_type == "delegation_create":
            return self._handle_delegation_create(event, tick)
        if event.event_type == "delegation_revoke":
            return self._handle_delegation_revoke(event, tick)
        if event.event_type == "delegation_transfer":
            return self._handle_delegation_transfer(event, tick)
        if event.event_type == "authority_formation":
            return self._handle_authority_formation(event, tick)
        if event.event_type == "authority_action":
            return self._handle_authority_action(event, tick)
        return self._record_no_op_decision(event, tick)

    def _handle_delegation_create(
        self, event: SimulationEvent, tick: int, input_state_hash: str | None = None
    ) -> RuleDecision:
        pre_state_hash = input_state_hash or self.state.state_hash()
        required = ("source_subscriber_id", "target_representative_id", "token_share")
        missing = [field for field in required if field not in event.payload]
        if missing:
            event.status = EventStatus.REJECTED
            return self._record_rule_decision(
                event,
                DELEGATION_CREATE_RULE_ID,
                "rejected",
                f"missing payload fields: {', '.join(missing)}",
                tick,
                input_state_hash=pre_state_hash,
            )

        source_id = str(event.payload["source_subscriber_id"])
        target_id = str(event.payload["target_representative_id"])
        if source_id not in self.state.subscribers:
            event.status = EventStatus.REJECTED
            return self._record_rule_decision(
                event,
                DELEGATION_CREATE_RULE_ID,
                "rejected",
                f"unknown source Subscriber: {source_id}",
                tick,
                input_state_hash=pre_state_hash,
            )
        if target_id not in self.state.representatives:
            event.status = EventStatus.REJECTED
            return self._record_rule_decision(
                event,
                DELEGATION_CREATE_RULE_ID,
                "rejected",
                f"unknown target Representative: {target_id}",
                tick,
                input_state_hash=pre_state_hash,
            )

        delegation_id = str(event.payload.get("delegation_id") or f"delegation-{event.event_id}")
        activation_delay = int(event.payload.get("activation_delay_ticks", 30))
        try:
            delegation = DelegationRecord(
                delegation_id=delegation_id,
                source_subscriber_id=source_id,
                target_representative_id=target_id,
                token_share=float(event.payload["token_share"]),
                submitted_tick=event.submitted_tick,
                activation_tick=event.submitted_tick + activation_delay,
                status=DelegationStatus.PENDING,
                reason=f"created_by={event.event_id}",
            )
            self.state.add_delegation(delegation)
        except (StateValidationError, ValueError) as exc:
            event.status = EventStatus.REJECTED
            return self._record_rule_decision(
                event,
                DELEGATION_CREATE_RULE_ID,
                "rejected",
                str(exc),
                tick,
                input_state_hash=pre_state_hash,
            )

        event.status = EventStatus.PROCESSED
        return self._record_rule_decision(
            event,
            DELEGATION_CREATE_RULE_ID,
            "accepted",
            f"delegation_id={delegation_id}; activation_tick={delegation.activation_tick}",
            tick,
            input_state_hash=pre_state_hash,
        )

    def _handle_delegation_revoke(self, event: SimulationEvent, tick: int) -> RuleDecision:
        pre_state_hash = self.state.state_hash()
        delegation_id = event.payload.get("delegation_id")
        if not delegation_id:
            event.status = EventStatus.REJECTED
            return self._record_rule_decision(
                event,
                DELEGATION_REVOKE_RULE_ID,
                "rejected",
                "missing payload field: delegation_id",
                tick,
                input_state_hash=pre_state_hash,
            )
        delegation = self.state.delegations.get(str(delegation_id))
        if delegation is None:
            event.status = EventStatus.REJECTED
            return self._record_rule_decision(
                event,
                DELEGATION_REVOKE_RULE_ID,
                "rejected",
                f"unknown delegation_id={delegation_id}",
                tick,
                input_state_hash=pre_state_hash,
            )
        delegation.status = DelegationStatus.INACTIVE
        delegation.reason = f"revoked_by={event.event_id}"
        self._recalculate_representative_totals()
        event.status = EventStatus.PROCESSED
        return self._record_rule_decision(
            event,
            DELEGATION_REVOKE_RULE_ID,
            "accepted",
            f"delegation_id={delegation_id}; to_status=inactive",
            tick,
            input_state_hash=pre_state_hash,
        )

    def _handle_delegation_transfer(self, event: SimulationEvent, tick: int) -> RuleDecision:
        pre_state_hash = self.state.state_hash()
        old_delegation_id = event.payload.get("delegation_id")
        target_id = event.payload.get("target_representative_id")
        if not old_delegation_id or not target_id:
            event.status = EventStatus.REJECTED
            return self._record_rule_decision(
                event,
                DELEGATION_CREATE_RULE_ID,
                "rejected",
                "missing payload fields: delegation_id, target_representative_id",
                tick,
                input_state_hash=pre_state_hash,
            )
        old_delegation = self.state.delegations.get(str(old_delegation_id))
        if old_delegation is None:
            event.status = EventStatus.REJECTED
            return self._record_rule_decision(
                event,
                DELEGATION_CREATE_RULE_ID,
                "rejected",
                f"unknown delegation_id={old_delegation_id}",
                tick,
                input_state_hash=pre_state_hash,
            )
        old_delegation.status = DelegationStatus.INACTIVE
        event.payload.setdefault("source_subscriber_id", old_delegation.source_subscriber_id)
        event.payload.setdefault("token_share", old_delegation.token_share)
        decision = self._handle_delegation_create(event, tick, input_state_hash=pre_state_hash)
        decision.reason = f"transfer_from={old_delegation_id}; {decision.reason}"
        return decision

    def _handle_authority_formation(self, event: SimulationEvent, tick: int) -> RuleDecision:
        pre_state_hash = self.state.state_hash()
        required = (
            "proposed_authority_id",
            "charter_id",
            "coercive_status",
            "authority_type",
            "scope_id",
        )
        missing = [field for field in required if field not in event.payload]
        if missing:
            event.status = EventStatus.REJECTED
            return self._record_rule_decision(
                event,
                AUTHORITY_FORMATION_RULE_ID,
                "rejected",
                f"missing payload fields: {', '.join(missing)}",
                tick,
                input_state_hash=pre_state_hash,
            )

        charter_id = str(event.payload["charter_id"])
        scope_id = str(event.payload["scope_id"])
        authority_id = str(event.payload["proposed_authority_id"])
        coercive_status = bool(event.payload["coercive_status"])
        charter = self.state.authority_charters.get(charter_id)
        if charter is None or scope_id not in self.state.scopes:
            event.status = EventStatus.REJECTED
            return self._record_rule_decision(
                event,
                AUTHORITY_FORMATION_RULE_ID,
                "rejected",
                "Authority Charter and scope are required before activation",
                tick,
                input_state_hash=pre_state_hash,
            )

        approval = self.state.approval_records.get(charter.approval_record_id)
        threshold = authority_formation_threshold(coercive_status)
        if approval is None or not approval_passes_threshold(approval, threshold):
            try:
                self.state.add_authority(
                    AuthorityRecord(
                        authority_id=authority_id,
                        charter_id=charter_id,
                        authority_type=str(event.payload["authority_type"]),
                        coercive_status=coercive_status,
                        scope_id=scope_id,
                        lifecycle_status=AuthorityLifecycleState.REJECTED,
                    )
                )
            except StateValidationError:
                pass
            event.status = EventStatus.PROCESSED
            return self._record_rule_decision(
                event,
                AUTHORITY_FORMATION_RULE_ID,
                "rejected",
                f"threshold_required={threshold}; to_state=rejected",
                tick,
                input_state_hash=pre_state_hash,
            )

        authority = AuthorityRecord(
            authority_id=authority_id,
            charter_id=charter_id,
            authority_type=str(event.payload["authority_type"]),
            coercive_status=coercive_status,
            scope_id=scope_id,
            lifecycle_status=AuthorityLifecycleState.PROPOSED,
        )
        transition_authority(authority, AuthorityLifecycleState.CHARTERED)
        transition_authority(authority, AuthorityLifecycleState.ACTIVE)
        authority.activation_tick = tick
        authority.review_due_tick = tick + int(event.payload.get("review_interval_ticks", 1825))
        try:
            self.state.add_authority(authority)
        except StateValidationError as exc:
            event.status = EventStatus.REJECTED
            return self._record_rule_decision(
                event,
                AUTHORITY_FORMATION_RULE_ID,
                "rejected",
                str(exc),
                tick,
                input_state_hash=pre_state_hash,
            )
        event.status = EventStatus.PROCESSED
        return self._record_rule_decision(
            event,
            AUTHORITY_FORMATION_RULE_ID,
            "accepted",
            f"threshold_required={threshold}; to_state=active; review_due_tick={authority.review_due_tick}",
            tick,
            input_state_hash=pre_state_hash,
        )

    def _handle_authority_action(self, event: SimulationEvent, tick: int) -> RuleDecision:
        pre_state_hash = self.state.state_hash()
        authority_id = str(event.payload.get("authority_id") or event.actor_id)
        authority = self.state.authorities.get(authority_id)
        if authority is None:
            event.status = EventStatus.REJECTED
            return self._record_rule_decision(
                event,
                AUTHORITY_ACTION_RULE_ID,
                "rejected",
                f"unknown Authority: {authority_id}",
                tick,
                input_state_hash=pre_state_hash,
            )
        if not can_execute_ordinary_action(
            authority,
            review_continuation_allowed=bool(
                event.payload.get("review_continuation_allowed", False)
            ),
        ):
            event.status = EventStatus.REJECTED
            return self._record_rule_decision(
                event,
                AUTHORITY_ACTION_RULE_ID,
                "rejected",
                f"Authority cannot execute ordinary action in state: {authority.lifecycle_status}",
                tick,
                input_state_hash=pre_state_hash,
            )

        conflict_ids = self._detect_scope_conflicts(event, authority, tick)
        event.status = EventStatus.PROCESSED
        result = "accepted"
        reason = "authority action accepted"
        if conflict_ids:
            result = "accepted_with_conflicts"
            reason = f"authority action accepted; conflicts={','.join(conflict_ids)}"
        return self._record_rule_decision(
            event,
            AUTHORITY_ACTION_RULE_ID,
            result,
            reason,
            tick,
            input_state_hash=pre_state_hash,
        )

    def _detect_scope_conflicts(
        self, event: SimulationEvent, authority: AuthorityRecord, tick: int
    ) -> list[str]:
        scope = self.state.scopes[authority.scope_id]
        conflict_ids: list[str] = []

        self_basis = self._self_conflict_basis(event, scope)
        if self_basis:
            conflict = self._scope_conflict_record(
                [authority.authority_id],
                [scope.scope_id],
                self_basis,
                tick,
                event.event_id,
            )
            if self._add_unique_scope_conflict(conflict):
                conflict_ids.append(conflict.conflict_id)

        for other_event in self._prior_authority_action_events(event, tick):
            other_authority_id = str(other_event.payload.get("authority_id") or other_event.actor_id)
            if other_authority_id == authority.authority_id:
                continue
            other_authority = self.state.authorities.get(other_authority_id)
            if (
                other_authority is None
                or other_authority.lifecycle_status != AuthorityLifecycleState.ACTIVE
            ):
                continue
            other_scope = self.state.scopes[other_authority.scope_id]
            basis = self._cross_authority_conflict_basis(
                event,
                scope,
                other_event,
                other_scope,
            )
            if not basis:
                continue
            conflict = self._scope_conflict_record(
                [authority.authority_id, other_authority.authority_id],
                [scope.scope_id, other_scope.scope_id],
                basis,
                tick,
                event.event_id,
            )
            if self._add_unique_scope_conflict(conflict):
                conflict_ids.append(conflict.conflict_id)

        return conflict_ids

    def _self_conflict_basis(
        self, event: SimulationEvent, scope: Any
    ) -> list[ScopeConflictClassification]:
        basis: list[ScopeConflictClassification] = []
        requested_powers = set(_text_list(event.payload.get("requested_powers")))
        if "requested_power" in event.payload:
            requested_powers.add(str(event.payload["requested_power"]))
        if requested_powers.intersection(scope.prohibited_powers):
            basis.append(ScopeConflictClassification.PROHIBITED_POWER)

        enforcement_power = event.payload.get("enforcement_power")
        if enforcement_power and str(enforcement_power) not in set(scope.enforcement_authority):
            basis.append(ScopeConflictClassification.ENFORCEMENT)
        return basis

    def _cross_authority_conflict_basis(
        self,
        event: SimulationEvent,
        scope: Any,
        other_event: SimulationEvent,
        other_scope: Any,
    ) -> list[ScopeConflictClassification]:
        basis: list[ScopeConflictClassification] = []
        if _overlaps(scope.territory, other_scope.territory) and self._directives_incompatible(
            event, other_event
        ):
            basis.append(ScopeConflictClassification.TERRITORIAL)
        if _overlaps(scope.population_affected, other_scope.population_affected) and self._directives_incompatible(
            event, other_event
        ):
            basis.append(ScopeConflictClassification.POPULATION)
        if _overlaps(scope.resource_authority, other_scope.resource_authority) and (
            event.payload.get("exclusive_resource_claim")
            or other_event.payload.get("exclusive_resource_claim")
        ):
            basis.append(ScopeConflictClassification.RESOURCE)
        if (
            scope.function == other_scope.function
            and self._powers_incompatible(event, other_event)
        ):
            basis.append(ScopeConflictClassification.FUNCTIONAL)
        return basis

    def _directives_incompatible(
        self, event: SimulationEvent, other_event: SimulationEvent
    ) -> bool:
        directive = event.payload.get("directive_type")
        other_directive = other_event.payload.get("directive_type")
        if not directive or not other_directive:
            return False
        matrix = _incompatibility_matrix(event.payload, other_event.payload)
        return str(other_directive) in set(matrix.get(str(directive), [])) or str(directive) in set(
            matrix.get(str(other_directive), [])
        )

    def _powers_incompatible(
        self, event: SimulationEvent, other_event: SimulationEvent
    ) -> bool:
        power = event.payload.get("requested_power")
        other_power = other_event.payload.get("requested_power")
        if not power or not other_power:
            return False
        matrix = _incompatibility_matrix(event.payload, other_event.payload)
        return str(other_power) in set(matrix.get(str(power), [])) or str(power) in set(
            matrix.get(str(other_power), [])
        )

    def _prior_authority_action_events(
        self, event: SimulationEvent, tick: int
    ) -> list[SimulationEvent]:
        return [
            item
            for item in self.state.events.values()
            if item.event_type == "authority_action"
            and item.event_id != event.event_id
            and item.status in {EventStatus.PROCESSED, EventStatus.NO_OP}
            and item.effective_tick == tick
        ]

    def _scope_conflict_record(
        self,
        authority_ids: list[str],
        scope_ids: list[str],
        basis: list[ScopeConflictClassification],
        tick: int,
        trigger_event_id: str,
    ) -> ScopeConflictRecord:
        unique_basis = sorted(set(basis), key=lambda item: item.value)
        stored_basis = (
            [ScopeConflictClassification.MIXED]
            if len(unique_basis) > 1
            else unique_basis
        )
        sorted_authorities = sorted(set(authority_ids))
        sorted_scopes = sorted(set(scope_ids))
        classification_key = "+".join(item.value for item in stored_basis)
        conflict_id = (
            f"scope-conflict-t{tick}-"
            f"{'-'.join(sorted_authorities)}-"
            f"{classification_key}-"
            f"{'-'.join(sorted_scopes)}"
        )
        return ScopeConflictRecord(
            conflict_id=conflict_id,
            authority_ids=sorted_authorities,
            scope_ids=sorted_scopes,
            conflict_basis=stored_basis,
            detected_tick=tick,
            trigger_event_id=trigger_event_id,
        )

    def _add_unique_scope_conflict(self, conflict: ScopeConflictRecord) -> bool:
        if conflict.conflict_id in self.state.scope_conflicts:
            return False
        self.state.add_scope_conflict(conflict)
        return True

    def _activate_due_delegations(self, tick: int) -> list[RuleDecision]:
        decisions: list[RuleDecision] = []
        for delegation in sorted(
            self.state.delegations.values(), key=lambda item: item.delegation_id
        ):
            if delegation.status != DelegationStatus.PENDING or delegation.activation_tick > tick:
                continue
            pre_state_hash = self.state.state_hash()
            source_event = self._source_event_for_delegation(delegation)
            active_share = sum(
                item.token_share
                for item in self.state.delegations.values()
                if item.source_subscriber_id == delegation.source_subscriber_id
                and item.status == DelegationStatus.ACTIVE
            )
            if active_share + delegation.token_share > 1:
                delegation.status = DelegationStatus.BLOCKED
                delegation.reason = "token_share_total_exceeds_one"
                result = "rejected"
            else:
                delegation.status = DelegationStatus.ACTIVE
                delegation.reason = f"activated_tick={tick}"
                result = "accepted"
            self._recalculate_representative_totals()
            decisions.append(
                self._record_rule_decision(
                    source_event,
                    DELEGATION_ACTIVATE_RULE_ID,
                    result,
                    f"delegation_id={delegation.delegation_id}; to_status={delegation.status.value}",
                    tick,
                    input_state_hash=pre_state_hash,
                )
            )
        return decisions

    def _source_event_for_delegation(self, delegation: DelegationRecord) -> SimulationEvent:
        if delegation.reason and delegation.reason.startswith("created_by="):
            event_id = delegation.reason.removeprefix("created_by=")
            event = self.state.events.get(event_id)
            if event is not None:
                return event
        if self.state.events:
            return next(iter(self.state.events.values()))
        synthetic = SimulationEvent(
            event_id=self._next_event_id(),
            event_type="noop",
            submitted_tick=delegation.submitted_tick,
            effective_tick=delegation.activation_tick,
            actor_id="engine",
            target_id=delegation.delegation_id,
            status=EventStatus.PROCESSED,
            provenance={"generated_for": "delegation_activation"},
        )
        self.state.add_event(synthetic)
        return synthetic

    def _recalculate_representative_totals(self) -> None:
        self.state.recalculate_representative_totals()

    def _record_rule_decision(
        self,
        event: SimulationEvent,
        rule_id: str,
        result: str,
        reason: str,
        tick: int,
        input_state_hash: str | None = None,
    ) -> RuleDecision:
        decision = RuleDecision(
            decision_id=self._next_decision_id(),
            event_id=event.event_id,
            rule_id=rule_id,
            input_state_hash=input_state_hash or self.state.state_hash(),
            output_state_hash=self.state.state_hash(),
            result=result,
            reason=reason,
            decision_tick=tick,
        )
        self.state.add_rule_decision(decision)
        return decision

    def _record_no_op_decision(self, event: SimulationEvent, tick: int) -> RuleDecision:
        pre_state_hash = self.state.state_hash()
        event.status = EventStatus.NO_OP
        return self._record_rule_decision(
            event,
            NO_OP_RULE_ID,
            EventStatus.NO_OP.value,
            "No state-changing rule registered for event type",
            tick,
            input_state_hash=pre_state_hash,
        )

    def _next_event_id(self) -> str:
        self._event_counter += 1
        return f"event-{self._event_counter:06d}"

    def _next_decision_id(self) -> str:
        self._decision_counter += 1
        return f"decision-{self._decision_counter:06d}"


def _text_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


def _overlaps(first: list[str], second: list[str]) -> bool:
    return bool(set(first).intersection(second))


def _incompatibility_matrix(*payloads: dict[str, Any]) -> dict[str, list[str]]:
    matrix: dict[str, list[str]] = {}
    for payload in payloads:
        raw_matrix = payload.get("incompatibility_matrix", {})
        if not isinstance(raw_matrix, dict):
            continue
        for key, values in raw_matrix.items():
            matrix.setdefault(str(key), [])
            matrix[str(key)].extend(_text_list(values))
    return matrix
