from jefferson_sim.engine import (
    EventInput,
    EventProcessor,
    EventStatus,
    NO_OP_RULE_ID,
    SimulationState,
)


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
