import pytest

from jefferson_sim.engine import (
    ApprovalRecord,
    AuthorityCharterRecord,
    AuthorityLifecycleState,
    AuthorityRecord,
    DelegationRecord,
    DelegationStatus,
    EventStatus,
    MetricRecord,
    RecordValidationError,
    RepresentativeRecord,
    RuleDecision,
    ScopeRecord,
    SimulationEvent,
    SubscriberRecord,
    ThresholdResult,
)


def test_subscriber_requires_ids() -> None:
    with pytest.raises(RecordValidationError):
        SubscriberRecord(subscriber_id="", token_id="token-1")

    with pytest.raises(RecordValidationError):
        SubscriberRecord(subscriber_id="sub-1", token_id="")


def test_delegation_requires_positive_token_share() -> None:
    with pytest.raises(RecordValidationError):
        DelegationRecord(
            delegation_id="del-1",
            source_subscriber_id="sub-1",
            target_representative_id="rep-1",
            token_share=0,
            submitted_tick=0,
            activation_tick=30,
        )


def test_approval_record_rejects_invalid_counts() -> None:
    with pytest.raises(RecordValidationError):
        ApprovalRecord(
            approval_record_id="approval-1",
            decision_type="authority_formation",
            subject_id="authority-1",
            electorate_basis="all_subscribers",
            eligible_count=10,
            approval_count=9,
            rejection_count=2,
            abstention_count=0,
            approval_ratio=0.9,
            threshold_required=0.75,
            threshold_result=ThresholdResult.PASS,
            snapshot_tick=0,
        )


def test_authority_charter_requires_charter_fields() -> None:
    with pytest.raises(RecordValidationError):
        AuthorityCharterRecord(
            charter_id="charter-1",
            scope_id="scope-1",
            funding_sources=[],
            renewal_process="five_year_review",
            oversight_structures=["public_audit"],
            formation_threshold=0.75,
            approval_record_id="approval-1",
        )


def test_records_serialize_enums_to_strings() -> None:
    event = SimulationEvent(
        event_id="event-1",
        event_type="delegation_create",
        submitted_tick=0,
        effective_tick=30,
        actor_id="sub-1",
        target_id="rep-1",
        status=EventStatus.ACCEPTED,
    )

    assert event.to_dict()["status"] == "accepted"

    delegation = DelegationRecord(
        delegation_id="del-1",
        source_subscriber_id="sub-1",
        target_representative_id="rep-1",
        token_share=1.0,
        submitted_tick=0,
        activation_tick=30,
        status=DelegationStatus.PENDING,
    )

    assert delegation.to_dict()["status"] == "pending"


def test_all_phase_one_records_can_be_constructed() -> None:
    SubscriberRecord("sub-1", "token-1")
    RepresentativeRecord("rep-1", "sub-1")
    ScopeRecord("scope-1", "public_safety")
    AuthorityRecord(
        authority_id="authority-1",
        charter_id="charter-1",
        authority_type="public_safety",
        coercive_status=True,
        scope_id="scope-1",
        lifecycle_status=AuthorityLifecycleState.PROPOSED,
    )
    RuleDecision(
        decision_id="decision-1",
        event_id="event-1",
        rule_id="rule-1",
        input_state_hash="abc123",
        result="accepted",
        reason="fixture",
        decision_tick=0,
    )
    MetricRecord(
        metric_id="metric-1",
        formula_id="raw_power_concentration",
        window_start_tick=0,
        window_end_tick=1,
        value=0.0,
        unit="share",
    )
