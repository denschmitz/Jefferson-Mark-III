from jefferson_sim.engine import (
    ApprovalRecord,
    AuthorityCharterRecord,
    AuthorityLifecycleState,
    AuthorityRecord,
    EventInput,
    EventProcessor,
    EventStatus,
    NO_OP_RULE_ID,
    RepresentativeRecord,
    ScopeRecord,
    ScopeConflictClassification,
    SimulationState,
    SubscriberRecord,
    ThresholdResult,
)


def authority_action_state() -> SimulationState:
    state = SimulationState()
    state.add_approval_record(
        ApprovalRecord(
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
    )
    for suffix, function in (("1", "public_safety"), ("2", "public_safety")):
        state.add_scope(
            ScopeRecord(
                scope_id=f"scope-{suffix}",
                function=function,
                territory=["district-1"],
                population_affected=["residents"],
                permitted_powers=["patrol", "close_road"],
                prohibited_powers=["curfew"] if suffix == "1" else [],
                resource_authority=["vehicle-fleet"],
                enforcement_authority=["citation"],
            )
        )
        state.add_authority_charter(
            AuthorityCharterRecord(
                charter_id=f"charter-{suffix}",
                scope_id=f"scope-{suffix}",
                funding_sources=["authority_surtax"],
                renewal_process="five_year_review",
                oversight_structures=["public_audit"],
                formation_threshold=0.75,
                approval_record_id="approval-1",
            )
        )
        state.add_authority(
            AuthorityRecord(
                authority_id=f"authority-{suffix}",
                charter_id=f"charter-{suffix}",
                authority_type="public_safety",
                coercive_status=True,
                scope_id=f"scope-{suffix}",
                lifecycle_status=AuthorityLifecycleState.ACTIVE,
            )
        )
    return state


def test_event_processor_assigns_stable_event_ids() -> None:
    processor = EventProcessor()

    result = processor.submit_events(
        0,
        [
            EventInput(
                event_type="noop",
                submitted_tick=0,
                effective_tick=0,
                actor_id="system",
            )
        ],
    )

    assert result.accepted_event_ids == ["event-000001"]
    assert processor.state.events["event-000001"].event_id == "event-000001"


def test_event_processor_rejects_unknown_event_type_and_preserves_event() -> None:
    processor = EventProcessor()

    result = processor.submit_events(
        0,
        [
            EventInput(
                event_type="unknown_event",
                submitted_tick=0,
                effective_tick=0,
                actor_id="system",
            )
        ],
    )

    event = processor.state.events["event-000001"]
    assert result.rejected_event_ids == ["event-000001"]
    assert event.status == EventStatus.REJECTED
    assert processor.validation_report.has_errors
    assert any(
        issue.code == "event.type.unknown"
        for issue in processor.validation_report.issues
    )


def test_event_processor_orders_same_tick_events_deterministically() -> None:
    processor = EventProcessor()

    processor.submit_events(
        0,
        [
            EventInput(
                event_type="delegation_create",
                submitted_tick=0,
                effective_tick=0,
                actor_id="sub-1",
            ),
            EventInput(
                event_type="authority_formation",
                submitted_tick=0,
                effective_tick=0,
                actor_id="sub-2",
            ),
        ],
    )

    assert [decision.event_id for decision in processor.state.rule_decisions] == [
        "event-000002",
        "event-000001",
    ]


def test_event_processor_records_no_op_rule_decisions() -> None:
    processor = EventProcessor()

    result = processor.submit_events(
        0,
        [
            EventInput(
                event_type="noop",
                submitted_tick=0,
                effective_tick=0,
                actor_id="system",
            )
        ],
    )

    decision = processor.state.rule_decisions[0]
    assert result.decision_ids == ["decision-000001"]
    assert decision.rule_id == NO_OP_RULE_ID
    assert decision.event_id == "event-000001"
    assert decision.result == EventStatus.NO_OP.value
    assert len(decision.input_state_hash) == 64
    assert len(decision.output_state_hash) == 64


def test_state_changing_rule_decision_records_pre_and_post_state_hashes() -> None:
    state = SimulationState()
    state.add_subscriber(SubscriberRecord("sub-1", "token-1"))
    state.add_representative(RepresentativeRecord("rep-1", "sub-1"))
    processor = EventProcessor(state)

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
                },
            )
        ],
    )

    decision = processor.state.rule_decisions[0]
    assert decision.result == EventStatus.ACCEPTED.value
    assert len(decision.input_state_hash) == 64
    assert len(decision.output_state_hash) == 64
    assert decision.input_state_hash != decision.output_state_hash


def test_event_processor_processes_future_effective_events_on_later_tick() -> None:
    processor = EventProcessor()

    first = processor.submit_events(
        0,
        [
            EventInput(
                event_type="noop",
                submitted_tick=0,
                effective_tick=1,
                actor_id="system",
            )
        ],
    )
    second = processor.submit_events(1, [])

    assert first.decision_ids == []
    assert second.decision_ids == ["decision-000001"]
    assert processor.state.events["event-000001"].status == EventStatus.NO_OP


def test_event_replay_is_deterministic_for_same_inputs() -> None:
    events_by_tick = {
        0: [
            EventInput(
                event_type="delegation_create",
                submitted_tick=0,
                effective_tick=0,
                actor_id="sub-1",
                target_id="rep-1",
                payload={"token_share": 1.0},
            )
        ],
        1: [
            EventInput(
                event_type="review_request",
                submitted_tick=1,
                effective_tick=1,
                actor_id="sub-2",
                target_id="authority-1",
            )
        ],
    }

    first_hash = EventProcessor(SimulationState()).replay(events_by_tick)
    second_hash = EventProcessor(SimulationState()).replay(events_by_tick)

    assert first_hash == second_hash


def test_state_hash_is_recorded_after_each_tick() -> None:
    processor = EventProcessor()

    result = processor.submit_events(0, [])

    assert processor.state_hashes_by_tick[0] == result.state_hash
    assert len(result.state_hash) == 64


def test_authority_action_with_benign_overlap_creates_no_scope_conflict() -> None:
    processor = EventProcessor(authority_action_state())

    processor.submit_events(
        0,
        [
            EventInput(
                event_type="authority_action",
                submitted_tick=0,
                effective_tick=0,
                actor_id="authority-1",
                payload={"authority_id": "authority-1", "directive_type": "patrol"},
            ),
            EventInput(
                event_type="authority_action",
                submitted_tick=0,
                effective_tick=0,
                actor_id="authority-2",
                payload={"authority_id": "authority-2", "directive_type": "patrol"},
            ),
        ],
    )

    assert processor.state.scope_conflicts == {}


def test_authority_action_detects_territorial_incompatible_directives() -> None:
    processor = EventProcessor(authority_action_state())
    matrix = {"close_road": ["open_road"], "open_road": ["close_road"]}

    processor.submit_events(
        0,
        [
            EventInput(
                event_type="authority_action",
                submitted_tick=0,
                effective_tick=0,
                actor_id="authority-1",
                payload={
                    "authority_id": "authority-1",
                    "directive_type": "close_road",
                    "incompatibility_matrix": matrix,
                },
            ),
            EventInput(
                event_type="authority_action",
                submitted_tick=0,
                effective_tick=0,
                actor_id="authority-2",
                payload={
                    "authority_id": "authority-2",
                    "directive_type": "open_road",
                    "incompatibility_matrix": matrix,
                },
            ),
        ],
    )

    conflict = next(iter(processor.state.scope_conflicts.values()))
    assert conflict.authority_ids == ["authority-1", "authority-2"]
    assert conflict.conflict_basis == [ScopeConflictClassification.MIXED]


def test_authority_action_detects_exclusive_resource_conflict() -> None:
    processor = EventProcessor(authority_action_state())

    processor.submit_events(
        0,
        [
            EventInput(
                event_type="authority_action",
                submitted_tick=0,
                effective_tick=0,
                actor_id="authority-1",
                payload={
                    "authority_id": "authority-1",
                    "exclusive_resource_claim": True,
                },
            ),
            EventInput(
                event_type="authority_action",
                submitted_tick=0,
                effective_tick=0,
                actor_id="authority-2",
                payload={
                    "authority_id": "authority-2",
                    "exclusive_resource_claim": True,
                },
            ),
        ],
    )

    conflict = next(iter(processor.state.scope_conflicts.values()))
    assert conflict.conflict_basis == [ScopeConflictClassification.RESOURCE]


def test_authority_action_detects_prohibited_power_conflict() -> None:
    processor = EventProcessor(authority_action_state())

    processor.submit_events(
        0,
        [
            EventInput(
                event_type="authority_action",
                submitted_tick=0,
                effective_tick=0,
                actor_id="authority-1",
                payload={
                    "authority_id": "authority-1",
                    "requested_power": "curfew",
                },
            )
        ],
    )

    conflict = next(iter(processor.state.scope_conflicts.values()))
    assert conflict.authority_ids == ["authority-1"]
    assert conflict.conflict_basis == [ScopeConflictClassification.PROHIBITED_POWER]


def test_authority_action_suppresses_duplicate_scope_conflicts_per_tick() -> None:
    processor = EventProcessor(authority_action_state())

    processor.submit_events(
        0,
        [
            EventInput(
                event_type="authority_action",
                submitted_tick=0,
                effective_tick=0,
                actor_id="authority-1",
                payload={
                    "authority_id": "authority-1",
                    "exclusive_resource_claim": True,
                },
            ),
            EventInput(
                event_type="authority_action",
                submitted_tick=0,
                effective_tick=0,
                actor_id="authority-2",
                payload={
                    "authority_id": "authority-2",
                    "exclusive_resource_claim": True,
                },
            ),
            EventInput(
                event_type="authority_action",
                submitted_tick=0,
                effective_tick=0,
                actor_id="authority-2",
                payload={
                    "authority_id": "authority-2",
                    "exclusive_resource_claim": True,
                },
            ),
        ],
    )

    assert len(processor.state.scope_conflicts) == 1
