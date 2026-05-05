import pytest

from jefferson_sim.engine import (
    ALLOWED_AUTHORITY_TRANSITIONS,
    ApprovalRecord,
    AuthorityCharterRecord,
    AuthorityLifecycleState,
    AuthorityRecord,
    DelegationStatus,
    EventInput,
    EventProcessor,
    LifecycleTransitionError,
    RepresentativeRecord,
    ScopeRecord,
    SimulationState,
    SubscriberRecord,
    ThresholdResult,
    authority_count,
    can_execute_ordinary_action,
    delegation_churn,
    evaluate_approval_record,
    raw_power_concentration,
    transition_authority,
)


def add_delegation_fixture_state() -> SimulationState:
    state = SimulationState()
    state.add_subscriber(SubscriberRecord("sub-1", "token-1"))
    state.add_subscriber(SubscriberRecord("sub-2", "token-2"))
    state.add_representative(RepresentativeRecord("rep-1", "sub-1"))
    state.add_representative(RepresentativeRecord("rep-2", "sub-2"))
    return state


def add_authority_fixture_state(approval_ratio: float = 0.75) -> SimulationState:
    state = SimulationState()
    state.add_approval_record(
        ApprovalRecord(
            approval_record_id="approval-1",
            decision_type="authority_formation",
            subject_id="authority-1",
            electorate_basis="all_subscribers",
            eligible_count=100,
            approval_count=int(approval_ratio * 100),
            rejection_count=100 - int(approval_ratio * 100),
            abstention_count=0,
            approval_ratio=approval_ratio,
            threshold_required=0.75,
            threshold_result=ThresholdResult.PASS
            if approval_ratio >= 0.75
            else ThresholdResult.FAIL,
            snapshot_tick=0,
            assumptions_used=["fixed_eligible_snapshot"],
        )
    )
    state.add_scope(
        ScopeRecord(
            scope_id="scope-1",
            function="public_safety",
            permitted_powers=["patrol"],
            enforcement_authority=["citation"],
        )
    )
    state.add_authority_charter(
        AuthorityCharterRecord(
            charter_id="charter-1",
            scope_id="scope-1",
            funding_sources=["authority_surtax"],
            renewal_process="five_year_review",
            oversight_structures=["public_audit"],
            formation_threshold=0.75,
            approval_record_id="approval-1",
        )
    )
    return state


def test_approval_threshold_helper_uses_approval_ratio() -> None:
    record = ApprovalRecord(
        approval_record_id="approval-1",
        decision_type="authority_formation",
        subject_id="authority-1",
        electorate_basis="all_subscribers",
        eligible_count=100,
        approval_count=60,
        rejection_count=40,
        abstention_count=0,
        approval_ratio=0.60,
        threshold_required=0.75,
        threshold_result=ThresholdResult.FAIL,
        snapshot_tick=0,
        assumptions_used=["fixed_eligible_snapshot"],
    )

    assert evaluate_approval_record(record) == ThresholdResult.FAIL
    assert evaluate_approval_record(record, threshold=0.60) == ThresholdResult.PASS


def test_delegation_create_schedules_activation_and_updates_raw_total() -> None:
    processor = EventProcessor(add_delegation_fixture_state())

    processor.submit_events(
        0,
        [
            EventInput(
                event_type="delegation_create",
                submitted_tick=0,
                effective_tick=0,
                actor_id="sub-1",
                target_id="rep-1",
                payload={
                    "source_subscriber_id": "sub-1",
                    "target_representative_id": "rep-1",
                    "token_share": 1.0,
                    "activation_delay_ticks": 1,
                },
            )
        ],
    )
    processor.submit_events(1, [])

    delegation = processor.state.delegations["delegation-event-000001"]
    assert delegation.status == DelegationStatus.ACTIVE
    assert processor.state.representatives["rep-1"].raw_delegation_total == 1.0


def test_delegation_revocation_preserves_history_and_recalculates_total() -> None:
    processor = EventProcessor(add_delegation_fixture_state())
    processor.submit_events(
        0,
        [
            EventInput(
                event_type="delegation_create",
                submitted_tick=0,
                effective_tick=0,
                actor_id="sub-1",
                payload={
                    "source_subscriber_id": "sub-1",
                    "target_representative_id": "rep-1",
                    "token_share": 1.0,
                    "activation_delay_ticks": 0,
                },
            )
        ],
    )

    processor.submit_events(
        1,
        [
            EventInput(
                event_type="delegation_revoke",
                submitted_tick=1,
                effective_tick=1,
                actor_id="sub-1",
                payload={"delegation_id": "delegation-event-000001"},
            )
        ],
    )

    assert processor.state.delegations["delegation-event-000001"].status == DelegationStatus.INACTIVE
    assert processor.state.representatives["rep-1"].raw_delegation_total == 0.0


def test_authority_formation_passes_and_activates() -> None:
    processor = EventProcessor(add_authority_fixture_state(approval_ratio=0.75))

    processor.submit_events(
        0,
        [
            EventInput(
                event_type="authority_formation",
                submitted_tick=0,
                effective_tick=0,
                actor_id="sub-1",
                payload={
                    "proposed_authority_id": "authority-1",
                    "charter_id": "charter-1",
                    "coercive_status": True,
                    "authority_type": "public_safety",
                    "scope_id": "scope-1",
                },
            )
        ],
    )

    authority = processor.state.authorities["authority-1"]
    assert authority.lifecycle_status == AuthorityLifecycleState.ACTIVE
    assert authority.activation_tick == 0
    assert authority.review_due_tick == 1825


def test_authority_formation_fails_threshold() -> None:
    processor = EventProcessor(add_authority_fixture_state(approval_ratio=0.74))

    processor.submit_events(
        0,
        [
            EventInput(
                event_type="authority_formation",
                submitted_tick=0,
                effective_tick=0,
                actor_id="sub-1",
                payload={
                    "proposed_authority_id": "authority-1",
                    "charter_id": "charter-1",
                    "coercive_status": True,
                    "authority_type": "public_safety",
                    "scope_id": "scope-1",
                },
            )
        ],
    )

    assert (
        processor.state.authorities["authority-1"].lifecycle_status
        == AuthorityLifecycleState.REJECTED
    )
    assert processor.state.rule_decisions[-1].result == "rejected"


def test_lifecycle_rejects_invalid_transition_and_gates_actions() -> None:
    authority = AuthorityRecord(
        authority_id="authority-1",
        charter_id="charter-1",
        authority_type="public_safety",
        coercive_status=True,
        scope_id="scope-1",
    )

    with pytest.raises(LifecycleTransitionError):
        transition_authority(authority, AuthorityLifecycleState.ACTIVE)

    transition_authority(authority, AuthorityLifecycleState.CHARTERED)
    transition_authority(authority, AuthorityLifecycleState.ACTIVE)
    assert can_execute_ordinary_action(authority)


@pytest.mark.parametrize(
    ("from_state", "to_state"),
    [
        (AuthorityLifecycleState.PROPOSED, AuthorityLifecycleState.CHARTERED),
        (AuthorityLifecycleState.PROPOSED, AuthorityLifecycleState.REJECTED),
        (AuthorityLifecycleState.CHARTERED, AuthorityLifecycleState.ACTIVE),
        (AuthorityLifecycleState.ACTIVE, AuthorityLifecycleState.UNDER_REVIEW),
        (AuthorityLifecycleState.ACTIVE, AuthorityLifecycleState.SUSPENDED),
        (AuthorityLifecycleState.ACTIVE, AuthorityLifecycleState.DISSOLVING),
        (AuthorityLifecycleState.UNDER_REVIEW, AuthorityLifecycleState.ACTIVE),
        (
            AuthorityLifecycleState.UNDER_REVIEW,
            AuthorityLifecycleState.REAUTHORIZATION_REQUIRED,
        ),
        (AuthorityLifecycleState.UNDER_REVIEW, AuthorityLifecycleState.SUSPENDED),
        (AuthorityLifecycleState.UNDER_REVIEW, AuthorityLifecycleState.DISSOLVING),
        (
            AuthorityLifecycleState.REAUTHORIZATION_REQUIRED,
            AuthorityLifecycleState.ACTIVE,
        ),
        (
            AuthorityLifecycleState.REAUTHORIZATION_REQUIRED,
            AuthorityLifecycleState.DISSOLVING,
        ),
        (AuthorityLifecycleState.SUSPENDED, AuthorityLifecycleState.ACTIVE),
        (AuthorityLifecycleState.SUSPENDED, AuthorityLifecycleState.DISSOLVING),
        (AuthorityLifecycleState.DISSOLVING, AuthorityLifecycleState.DISSOLVED),
    ],
)
def test_first_pass_lifecycle_allows_supported_transitions(
    from_state: AuthorityLifecycleState, to_state: AuthorityLifecycleState
) -> None:
    authority = AuthorityRecord(
        authority_id="authority-1",
        charter_id="charter-1",
        authority_type="public_safety",
        coercive_status=True,
        scope_id="scope-1",
        lifecycle_status=from_state,
    )

    transition_authority(authority, to_state)

    assert authority.lifecycle_status == to_state


def test_lifecycle_all_supported_transitions_are_covered_by_tests() -> None:
    expected = {
        (AuthorityLifecycleState.PROPOSED, AuthorityLifecycleState.CHARTERED),
        (AuthorityLifecycleState.PROPOSED, AuthorityLifecycleState.REJECTED),
        (AuthorityLifecycleState.CHARTERED, AuthorityLifecycleState.ACTIVE),
        (AuthorityLifecycleState.ACTIVE, AuthorityLifecycleState.UNDER_REVIEW),
        (AuthorityLifecycleState.ACTIVE, AuthorityLifecycleState.SUSPENDED),
        (AuthorityLifecycleState.ACTIVE, AuthorityLifecycleState.DISSOLVING),
        (AuthorityLifecycleState.UNDER_REVIEW, AuthorityLifecycleState.ACTIVE),
        (
            AuthorityLifecycleState.UNDER_REVIEW,
            AuthorityLifecycleState.REAUTHORIZATION_REQUIRED,
        ),
        (AuthorityLifecycleState.UNDER_REVIEW, AuthorityLifecycleState.SUSPENDED),
        (AuthorityLifecycleState.UNDER_REVIEW, AuthorityLifecycleState.DISSOLVING),
        (
            AuthorityLifecycleState.REAUTHORIZATION_REQUIRED,
            AuthorityLifecycleState.ACTIVE,
        ),
        (
            AuthorityLifecycleState.REAUTHORIZATION_REQUIRED,
            AuthorityLifecycleState.DISSOLVING,
        ),
        (AuthorityLifecycleState.SUSPENDED, AuthorityLifecycleState.ACTIVE),
        (AuthorityLifecycleState.SUSPENDED, AuthorityLifecycleState.DISSOLVING),
        (AuthorityLifecycleState.DISSOLVING, AuthorityLifecycleState.DISSOLVED),
    }
    actual = {
        (from_state, to_state)
        for from_state, to_states in ALLOWED_AUTHORITY_TRANSITIONS.items()
        for to_state in to_states
    }

    assert actual == expected


@pytest.mark.parametrize(
    ("from_state", "to_state"),
    [
        (AuthorityLifecycleState.PROPOSED, AuthorityLifecycleState.ACTIVE),
        (AuthorityLifecycleState.CHARTERED, AuthorityLifecycleState.UNDER_REVIEW),
        (AuthorityLifecycleState.REJECTED, AuthorityLifecycleState.ACTIVE),
        (AuthorityLifecycleState.DISSOLVED, AuthorityLifecycleState.ACTIVE),
        (AuthorityLifecycleState.ACTIVE, AuthorityLifecycleState.MERGED),
        (AuthorityLifecycleState.ACTIVE, AuthorityLifecycleState.SEPARATED),
        (AuthorityLifecycleState.DISSOLVING, AuthorityLifecycleState.ACTIVE),
    ],
)
def test_first_pass_lifecycle_rejects_unsupported_transitions(
    from_state: AuthorityLifecycleState, to_state: AuthorityLifecycleState
) -> None:
    authority = AuthorityRecord(
        authority_id="authority-1",
        charter_id="charter-1",
        authority_type="public_safety",
        coercive_status=True,
        scope_id="scope-1",
        lifecycle_status=from_state,
    )

    with pytest.raises(LifecycleTransitionError):
        transition_authority(authority, to_state)


@pytest.mark.parametrize(
    "state",
    [
        AuthorityLifecycleState.PROPOSED,
        AuthorityLifecycleState.REJECTED,
        AuthorityLifecycleState.CHARTERED,
        AuthorityLifecycleState.SUSPENDED,
        AuthorityLifecycleState.DISSOLVING,
        AuthorityLifecycleState.DISSOLVED,
        AuthorityLifecycleState.MERGED,
        AuthorityLifecycleState.SEPARATED,
        AuthorityLifecycleState.REAUTHORIZATION_REQUIRED,
    ],
)
def test_lifecycle_blocks_ordinary_actions_for_inactive_states(
    state: AuthorityLifecycleState,
) -> None:
    authority = AuthorityRecord(
        authority_id="authority-1",
        charter_id="charter-1",
        authority_type="public_safety",
        coercive_status=True,
        scope_id="scope-1",
        lifecycle_status=state,
    )

    assert not can_execute_ordinary_action(authority)


def test_lifecycle_under_review_actions_require_explicit_continuation() -> None:
    authority = AuthorityRecord(
        authority_id="authority-1",
        charter_id="charter-1",
        authority_type="public_safety",
        coercive_status=True,
        scope_id="scope-1",
        lifecycle_status=AuthorityLifecycleState.UNDER_REVIEW,
    )

    assert not can_execute_ordinary_action(authority)
    assert can_execute_ordinary_action(authority, review_continuation_allowed=True)


def test_narrow_metric_formulas() -> None:
    processor = EventProcessor(add_delegation_fixture_state())
    processor.submit_events(
        0,
        [
            EventInput(
                event_type="delegation_create",
                submitted_tick=0,
                effective_tick=0,
                actor_id="sub-1",
                payload={
                    "source_subscriber_id": "sub-1",
                    "target_representative_id": "rep-1",
                    "token_share": 1.0,
                    "activation_delay_ticks": 0,
                },
            )
        ],
    )
    authority_state = add_authority_fixture_state()
    authority_state.add_authority(
        AuthorityRecord(
            authority_id="authority-1",
            charter_id="charter-1",
            authority_type="public_safety",
            coercive_status=True,
            scope_id="scope-1",
            lifecycle_status=AuthorityLifecycleState.ACTIVE,
        )
    )

    assert raw_power_concentration(processor.state, 0, 0).value == 0.5
    assert delegation_churn(processor.state, 0, 0).value == 0.5
    assert authority_count(authority_state, 0, 0).value == 1
