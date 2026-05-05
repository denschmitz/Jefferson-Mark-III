"""Simulation state container and deterministic serialization."""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
from typing import Any

from .records import (
    ApprovalRecord,
    AuthorityCharterRecord,
    AuthorityRecord,
    DelegationRecord,
    DelegationStatus,
    MetricRecord,
    RepresentativeRecord,
    RuleDecision,
    ScopeRecord,
    SimulationEvent,
    SubscriberRecord,
    to_primitive,
)


class StateValidationError(ValueError):
    """Raised when records cannot be added to simulation state."""


@dataclass(slots=True)
class SimulationState:
    subscribers: dict[str, SubscriberRecord] = field(default_factory=dict)
    representatives: dict[str, RepresentativeRecord] = field(default_factory=dict)
    delegations: dict[str, DelegationRecord] = field(default_factory=dict)
    authorities: dict[str, AuthorityRecord] = field(default_factory=dict)
    authority_charters: dict[str, AuthorityCharterRecord] = field(default_factory=dict)
    scopes: dict[str, ScopeRecord] = field(default_factory=dict)
    approval_records: dict[str, ApprovalRecord] = field(default_factory=dict)
    events: dict[str, SimulationEvent] = field(default_factory=dict)
    rule_decisions: list[RuleDecision] = field(default_factory=list)
    metrics: list[MetricRecord] = field(default_factory=list)

    def add_subscriber(self, record: SubscriberRecord) -> None:
        self._add_unique(self.subscribers, record.subscriber_id, record)

    def add_representative(self, record: RepresentativeRecord) -> None:
        self._add_unique(self.representatives, record.representative_id, record)

    def add_delegation(self, record: DelegationRecord) -> None:
        if record.source_subscriber_id not in self.subscribers:
            raise StateValidationError("delegation source subscriber does not exist")
        if record.target_representative_id not in self.representatives:
            raise StateValidationError("delegation target representative does not exist")
        self._validate_active_delegation_shares(record)
        self._add_unique(self.delegations, record.delegation_id, record)
        self.recalculate_representative_totals()

    def add_authority(self, record: AuthorityRecord) -> None:
        if record.charter_id not in self.authority_charters:
            raise StateValidationError("authority charter does not exist")
        if record.scope_id not in self.scopes:
            raise StateValidationError("authority scope does not exist")
        self._add_unique(self.authorities, record.authority_id, record)

    def add_authority_charter(self, record: AuthorityCharterRecord) -> None:
        if record.scope_id not in self.scopes:
            raise StateValidationError("authority charter scope does not exist")
        if record.approval_record_id not in self.approval_records:
            raise StateValidationError("authority charter approval record does not exist")
        self._add_unique(self.authority_charters, record.charter_id, record)

    def add_scope(self, record: ScopeRecord) -> None:
        self._add_unique(self.scopes, record.scope_id, record)

    def add_approval_record(self, record: ApprovalRecord) -> None:
        self._add_unique(self.approval_records, record.approval_record_id, record)

    def add_event(self, record: SimulationEvent) -> None:
        self._add_unique(self.events, record.event_id, record)

    def add_rule_decision(self, record: RuleDecision) -> None:
        self.rule_decisions.append(record)

    def add_metric(self, record: MetricRecord) -> None:
        self.metrics.append(record)

    def to_dict(self) -> dict[str, Any]:
        return {
            "subscribers": to_primitive(self.subscribers),
            "representatives": to_primitive(self.representatives),
            "delegations": to_primitive(self.delegations),
            "authorities": to_primitive(self.authorities),
            "authority_charters": to_primitive(self.authority_charters),
            "scopes": to_primitive(self.scopes),
            "approval_records": to_primitive(self.approval_records),
            "events": to_primitive(self.events),
            "rule_decisions": to_primitive(self.rule_decisions),
            "metrics": to_primitive(self.metrics),
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"))

    def state_hash(self) -> str:
        return hashlib.sha256(self.to_json().encode("utf-8")).hexdigest()

    def recalculate_representative_totals(self) -> None:
        for representative in self.representatives.values():
            representative.raw_delegation_total = 0.0
        for delegation in self.delegations.values():
            if delegation.status != DelegationStatus.ACTIVE:
                continue
            self.representatives[
                delegation.target_representative_id
            ].raw_delegation_total += delegation.token_share

    def validate_active_delegation_shares(self) -> None:
        self._validate_active_delegation_shares()

    def _validate_active_delegation_shares(
        self, proposed_record: DelegationRecord | None = None
    ) -> None:
        active_share_by_subscriber: dict[str, float] = {}
        delegations = list(self.delegations.values())
        if proposed_record is not None:
            delegations.append(proposed_record)
        for delegation in delegations:
            if delegation.status != DelegationStatus.ACTIVE:
                continue
            active_share_by_subscriber[delegation.source_subscriber_id] = (
                active_share_by_subscriber.get(delegation.source_subscriber_id, 0.0)
                + delegation.token_share
            )
        for subscriber_id, token_share in active_share_by_subscriber.items():
            if token_share > 1:
                raise StateValidationError(
                    f"active delegation token_share total exceeds one for subscriber: {subscriber_id}"
                )

    @staticmethod
    def _add_unique(records: dict[str, Any], record_id: str, record: Any) -> None:
        if record_id in records:
            raise StateValidationError(f"duplicate record id: {record_id}")
        records[record_id] = record
