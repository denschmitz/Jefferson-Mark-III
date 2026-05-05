import pytest

from jefferson_sim.engine import (
    ApprovalRecord,
    AuthorityCharterRecord,
    AuthorityRecord,
    DelegationRecord,
    DelegationStatus,
    RepresentativeRecord,
    ScopeRecord,
    ScopeConflictClassification,
    ScopeConflictRecord,
    SimulationState,
    StateValidationError,
    SubscriberRecord,
    ThresholdResult,
)


def approval_record() -> ApprovalRecord:
    return ApprovalRecord(
        approval_record_id="approval-1",
        decision_type="authority_formation",
        subject_id="authority-1",
        electorate_basis="all_subscribers",
        eligible_count=100,
        approval_count=75,
        rejection_count=25,
        abstention_count=0,
        approval_ratio=0.75,
        threshold_required=0.75,
        threshold_result=ThresholdResult.PASS,
        snapshot_tick=0,
        assumptions_used=["fixed_eligible_snapshot"],
    )


def scope_record() -> ScopeRecord:
    return ScopeRecord(
        scope_id="scope-1",
        function="public_safety",
        permitted_powers=["patrol"],
        enforcement_authority=["citation"],
    )


def charter_record() -> AuthorityCharterRecord:
    return AuthorityCharterRecord(
        charter_id="charter-1",
        scope_id="scope-1",
        funding_sources=["authority_surtax"],
        renewal_process="five_year_review",
        oversight_structures=["public_audit"],
        formation_threshold=0.75,
        approval_record_id="approval-1",
    )


def test_state_rejects_duplicate_ids() -> None:
    state = SimulationState()
    state.add_subscriber(SubscriberRecord("sub-1", "token-1"))

    with pytest.raises(StateValidationError):
        state.add_subscriber(SubscriberRecord("sub-1", "token-2"))


def test_state_rejects_authority_without_charter() -> None:
    state = SimulationState()
    state.add_scope(scope_record())

    with pytest.raises(StateValidationError):
        state.add_authority(
            AuthorityRecord(
                authority_id="authority-1",
                charter_id="charter-1",
                authority_type="public_safety",
                coercive_status=True,
                scope_id="scope-1",
            )
        )


def test_state_accepts_linked_authority_records() -> None:
    state = SimulationState()
    state.add_approval_record(approval_record())
    state.add_scope(scope_record())
    state.add_authority_charter(charter_record())
    state.add_authority(
        AuthorityRecord(
            authority_id="authority-1",
            charter_id="charter-1",
            authority_type="public_safety",
            coercive_status=True,
            scope_id="scope-1",
        )
    )

    assert "authority-1" in state.authorities


def test_state_serialization_and_hash_are_deterministic() -> None:
    first = SimulationState()
    second = SimulationState()

    for state in (first, second):
        state.add_subscriber(SubscriberRecord("sub-1", "token-1"))
        state.add_approval_record(approval_record())
        state.add_scope(scope_record())
        state.add_authority_charter(charter_record())

    assert first.to_dict() == second.to_dict()
    assert first.state_hash() == second.state_hash()
    assert len(first.state_hash()) == 64


def test_state_stores_scope_conflicts_in_serialized_state() -> None:
    state = SimulationState()

    state.add_scope_conflict(
        ScopeConflictRecord(
            conflict_id="scope-conflict-1",
            authority_ids=["authority-1"],
            scope_ids=["scope-1"],
            conflict_basis=[ScopeConflictClassification.PROHIBITED_POWER],
            detected_tick=0,
            trigger_event_id="event-1",
        )
    )

    assert state.to_dict()["scope_conflicts"]["scope-conflict-1"]["conflict_basis"] == [
        "prohibited_power"
    ]


def test_state_recalculates_raw_delegation_totals_from_active_delegations() -> None:
    state = SimulationState()
    state.add_subscriber(SubscriberRecord("sub-1", "token-1"))
    state.add_representative(
        RepresentativeRecord("rep-1", "sub-1", raw_delegation_total=99.0)
    )

    state.add_delegation(
        DelegationRecord(
            delegation_id="delegation-1",
            source_subscriber_id="sub-1",
            target_representative_id="rep-1",
            token_share=0.5,
            submitted_tick=0,
            activation_tick=0,
            status=DelegationStatus.ACTIVE,
        )
    )

    assert state.representatives["rep-1"].raw_delegation_total == 0.5


def test_state_rejects_active_delegation_share_total_above_one() -> None:
    state = SimulationState()
    state.add_subscriber(SubscriberRecord("sub-1", "token-1"))
    state.add_representative(RepresentativeRecord("rep-1", "sub-1"))
    state.add_representative(RepresentativeRecord("rep-2", "sub-1"))
    state.add_delegation(
        DelegationRecord(
            delegation_id="delegation-1",
            source_subscriber_id="sub-1",
            target_representative_id="rep-1",
            token_share=0.75,
            submitted_tick=0,
            activation_tick=0,
            status=DelegationStatus.ACTIVE,
        )
    )

    with pytest.raises(StateValidationError):
        state.add_delegation(
            DelegationRecord(
                delegation_id="delegation-2",
                source_subscriber_id="sub-1",
                target_representative_id="rep-2",
                token_share=0.5,
                submitted_tick=0,
                activation_tick=0,
                status=DelegationStatus.ACTIVE,
            )
        )
