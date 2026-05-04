import pytest

from jefferson_sim.engine import (
    ApprovalRecord,
    AuthorityCharterRecord,
    AuthorityRecord,
    ScopeRecord,
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
