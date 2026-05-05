"""Core simulation records for the Charter mechanics engine."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, is_dataclass
from enum import StrEnum
from typing import Any


class RecordValidationError(ValueError):
    """Raised when a simulation record violates its local schema."""


class EventStatus(StrEnum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    PENDING = "pending"
    PROCESSED = "processed"
    NO_OP = "no_op"


class DelegationStatus(StrEnum):
    PENDING = "pending"
    ACTIVE = "active"
    INACTIVE = "inactive"
    BLOCKED = "blocked"


class ThresholdResult(StrEnum):
    PASS = "pass"
    FAIL = "fail"
    NOT_APPLICABLE = "not_applicable"


SUPPORTED_APPROVAL_DECISION_TYPES = frozenset(
    {
        "authority_formation",
        "authority_renewal",
        "national_decision",
        "charter_amendment",
        "emergency_extension",
        "governance_credit_override",
    }
)

FLOAT_TOLERANCE = 1e-9


class AuthorityLifecycleState(StrEnum):
    PROPOSED = "proposed"
    REJECTED = "rejected"
    CHARTERED = "chartered"
    ACTIVE = "active"
    UNDER_REVIEW = "under_review"
    REAUTHORIZATION_REQUIRED = "reauthorization_required"
    SUSPENDED = "suspended"
    DISSOLVING = "dissolving"
    DISSOLVED = "dissolved"
    MERGED = "merged"
    SEPARATED = "separated"


def _require_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value:
        raise RecordValidationError(f"{field_name} is required")


def _require_non_negative(value: int | float, field_name: str) -> None:
    if value < 0:
        raise RecordValidationError(f"{field_name} must be non-negative")


def approval_ratio_from_counts(approval_count: int, eligible_count: int) -> float:
    if eligible_count == 0:
        return 0.0
    return approval_count / eligible_count


def threshold_result_from_ratio(
    approval_ratio: float, threshold_required: float
) -> ThresholdResult:
    return ThresholdResult.PASS if approval_ratio >= threshold_required else ThresholdResult.FAIL


def to_primitive(value: Any) -> Any:
    """Convert dataclasses and enums into deterministic JSON-compatible data."""

    if isinstance(value, StrEnum):
        return value.value
    if is_dataclass(value):
        return to_primitive(asdict(value))
    if isinstance(value, dict):
        return {str(key): to_primitive(item) for key, item in sorted(value.items())}
    if isinstance(value, list | tuple):
        return [to_primitive(item) for item in value]
    return value


@dataclass(slots=True)
class SubscriberRecord:
    subscriber_id: str
    token_id: str
    active_status: bool = True
    group_ids: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        _require_text(self.subscriber_id, "subscriber_id")
        _require_text(self.token_id, "token_id")

    def to_dict(self) -> dict[str, Any]:
        return to_primitive(self)


@dataclass(slots=True)
class RepresentativeRecord:
    representative_id: str
    subscriber_id: str
    raw_delegation_total: float = 0.0
    weighted_delegation_total: float | None = None
    coalition_id: str | None = None

    def __post_init__(self) -> None:
        _require_text(self.representative_id, "representative_id")
        _require_text(self.subscriber_id, "subscriber_id")
        _require_non_negative(self.raw_delegation_total, "raw_delegation_total")
        if self.weighted_delegation_total is not None:
            _require_non_negative(
                self.weighted_delegation_total, "weighted_delegation_total"
            )

    def to_dict(self) -> dict[str, Any]:
        return to_primitive(self)


@dataclass(slots=True)
class DelegationRecord:
    delegation_id: str
    source_subscriber_id: str
    target_representative_id: str
    token_share: float
    submitted_tick: int
    activation_tick: int
    status: DelegationStatus = DelegationStatus.PENDING
    reason: str | None = None

    def __post_init__(self) -> None:
        _require_text(self.delegation_id, "delegation_id")
        _require_text(self.source_subscriber_id, "source_subscriber_id")
        _require_text(self.target_representative_id, "target_representative_id")
        if self.token_share <= 0:
            raise RecordValidationError("token_share must be greater than zero")
        _require_non_negative(self.submitted_tick, "submitted_tick")
        _require_non_negative(self.activation_tick, "activation_tick")

    def to_dict(self) -> dict[str, Any]:
        return to_primitive(self)


@dataclass(slots=True)
class ScopeRecord:
    scope_id: str
    function: str
    territory: list[str] = field(default_factory=list)
    population_affected: list[str] = field(default_factory=list)
    permitted_powers: list[str] = field(default_factory=list)
    prohibited_powers: list[str] = field(default_factory=list)
    resource_authority: list[str] = field(default_factory=list)
    enforcement_authority: list[str] = field(default_factory=list)
    review_interval: str | None = None
    emergency_powers: list[str] = field(default_factory=list)
    authority_references: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        _require_text(self.scope_id, "scope_id")
        _require_text(self.function, "function")

    def to_dict(self) -> dict[str, Any]:
        return to_primitive(self)


@dataclass(slots=True)
class AuthorityCharterRecord:
    charter_id: str
    scope_id: str
    funding_sources: list[str]
    renewal_process: str
    oversight_structures: list[str]
    formation_threshold: float
    approval_record_id: str

    def __post_init__(self) -> None:
        _require_text(self.charter_id, "charter_id")
        _require_text(self.scope_id, "scope_id")
        _require_text(self.renewal_process, "renewal_process")
        _require_text(self.approval_record_id, "approval_record_id")
        if not self.funding_sources:
            raise RecordValidationError("funding_sources is required")
        if not self.oversight_structures:
            raise RecordValidationError("oversight_structures is required")
        if not 0 <= self.formation_threshold <= 1:
            raise RecordValidationError("formation_threshold must be between 0 and 1")

    def to_dict(self) -> dict[str, Any]:
        return to_primitive(self)


@dataclass(slots=True)
class AuthorityRecord:
    authority_id: str
    charter_id: str
    authority_type: str
    coercive_status: bool
    scope_id: str
    lifecycle_status: AuthorityLifecycleState = AuthorityLifecycleState.PROPOSED
    activation_tick: int | None = None
    review_due_tick: int | None = None
    dissolution_tick: int | None = None

    def __post_init__(self) -> None:
        _require_text(self.authority_id, "authority_id")
        _require_text(self.charter_id, "charter_id")
        _require_text(self.authority_type, "authority_type")
        _require_text(self.scope_id, "scope_id")

    def to_dict(self) -> dict[str, Any]:
        return to_primitive(self)


@dataclass(slots=True)
class ApprovalRecord:
    approval_record_id: str
    decision_type: str
    subject_id: str
    electorate_basis: str
    eligible_count: int
    approval_count: int
    rejection_count: int
    abstention_count: int
    approval_ratio: float
    threshold_required: float
    threshold_result: ThresholdResult
    snapshot_tick: int
    assumptions_used: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        _require_text(self.approval_record_id, "approval_record_id")
        _require_text(self.decision_type, "decision_type")
        _require_text(self.subject_id, "subject_id")
        _require_text(self.electorate_basis, "electorate_basis")
        if self.decision_type not in SUPPORTED_APPROVAL_DECISION_TYPES:
            raise RecordValidationError(f"unsupported approval decision_type: {self.decision_type}")
        for field_name in (
            "eligible_count",
            "approval_count",
            "rejection_count",
            "abstention_count",
            "snapshot_tick",
        ):
            _require_non_negative(getattr(self, field_name), field_name)
        if self.approval_count + self.rejection_count + self.abstention_count > self.eligible_count:
            raise RecordValidationError("counted approvals exceed eligible_count")
        if not 0 <= self.approval_ratio <= 1:
            raise RecordValidationError("approval_ratio must be between 0 and 1")
        if not 0 <= self.threshold_required <= 1:
            raise RecordValidationError("threshold_required must be between 0 and 1")
        expected_ratio = approval_ratio_from_counts(self.approval_count, self.eligible_count)
        if abs(self.approval_ratio - expected_ratio) > FLOAT_TOLERANCE:
            raise RecordValidationError(
                "approval_ratio must equal approval_count / eligible_count"
            )
        expected_result = threshold_result_from_ratio(
            self.approval_ratio, self.threshold_required
        )
        if self.threshold_result != expected_result:
            raise RecordValidationError(
                "threshold_result must match approval_ratio and threshold_required"
            )

    def to_dict(self) -> dict[str, Any]:
        return to_primitive(self)


@dataclass(slots=True)
class SimulationEvent:
    event_id: str
    event_type: str
    submitted_tick: int
    effective_tick: int
    actor_id: str
    target_id: str | None
    payload: dict[str, Any] = field(default_factory=dict)
    status: EventStatus = EventStatus.PENDING
    provenance: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_text(self.event_id, "event_id")
        _require_text(self.event_type, "event_type")
        _require_text(self.actor_id, "actor_id")
        _require_non_negative(self.submitted_tick, "submitted_tick")
        _require_non_negative(self.effective_tick, "effective_tick")

    def to_dict(self) -> dict[str, Any]:
        return to_primitive(self)


@dataclass(slots=True)
class RuleDecision:
    decision_id: str
    event_id: str
    rule_id: str
    input_state_hash: str
    output_state_hash: str
    result: str
    reason: str
    decision_tick: int

    def __post_init__(self) -> None:
        _require_text(self.decision_id, "decision_id")
        _require_text(self.event_id, "event_id")
        _require_text(self.rule_id, "rule_id")
        _require_text(self.input_state_hash, "input_state_hash")
        _require_text(self.output_state_hash, "output_state_hash")
        _require_text(self.result, "result")
        _require_non_negative(self.decision_tick, "decision_tick")

    def to_dict(self) -> dict[str, Any]:
        return to_primitive(self)


@dataclass(slots=True)
class MetricRecord:
    metric_id: str
    formula_id: str
    window_start_tick: int
    window_end_tick: int
    value: int | float | str | None
    unit: str
    not_applicable_reason: str | None = None

    def __post_init__(self) -> None:
        _require_text(self.metric_id, "metric_id")
        _require_text(self.formula_id, "formula_id")
        _require_text(self.unit, "unit")
        _require_non_negative(self.window_start_tick, "window_start_tick")
        _require_non_negative(self.window_end_tick, "window_end_tick")
        if self.window_end_tick < self.window_start_tick:
            raise RecordValidationError("window_end_tick cannot precede window_start_tick")

    def to_dict(self) -> dict[str, Any]:
        return to_primitive(self)
