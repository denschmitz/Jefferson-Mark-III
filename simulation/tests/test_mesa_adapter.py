from jefferson_sim.engine import (
    DelegationStatus,
    EventInput,
    RepresentativeRecord,
    SimulationState,
    SubscriberRecord,
)
from jefferson_sim.mesa_adapter import CharterMesaModel


def delegation_state() -> SimulationState:
    state = SimulationState()
    state.add_subscriber(SubscriberRecord("sub-1", "token-1"))
    state.add_representative(RepresentativeRecord("rep-1", "sub-1"))
    return state


def test_mesa_boundary_consumes_initialized_engine_state() -> None:
    state = delegation_state()

    model = CharterMesaModel(state=state, random_seed=123)

    assert model.processor.state is state
    assert model.random_seed == 123
    assert model.current_tick == 0


def test_mesa_boundary_queues_events_without_mutating_state() -> None:
    model = CharterMesaModel(state=delegation_state())
    before_hash = model.processor.state.state_hash()

    model.queue_event(
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
    )

    assert model.queued_event_count == 1
    assert model.processor.state.state_hash() == before_hash
    assert model.processor.state.events == {}


def test_mesa_boundary_step_submits_events_to_engine_for_decisions() -> None:
    model = CharterMesaModel(state=delegation_state())
    model.emit_event(
        event_type="delegation_create",
        actor_id="sub-1",
        payload={
            "source_subscriber_id": "sub-1",
            "target_representative_id": "rep-1",
            "token_share": 1.0,
            "activation_delay_ticks": 0,
        },
    )

    result = model.step()

    assert result.tick == 0
    assert model.current_tick == 1
    assert model.queued_event_count == 0
    assert [decision.rule_id for decision in result.decisions] == [
        "SIM-RULE-DELEGATION-CREATE",
        "SIM-RULE-DELEGATION-ACTIVATE",
    ]
    assert (
        model.processor.state.delegations["delegation-event-000001"].status
        == DelegationStatus.ACTIVE
    )


def test_mesa_boundary_state_snapshot_is_detached_from_engine_state() -> None:
    model = CharterMesaModel(state=delegation_state())

    snapshot = model.state_snapshot()
    snapshot["subscribers"].clear()

    assert "sub-1" in model.processor.state.subscribers


def test_mesa_boundary_does_not_duplicate_engine_rejection_logic() -> None:
    model = CharterMesaModel(state=delegation_state())
    model.emit_event(
        event_type="delegation_create",
        actor_id="sub-1",
        payload={
            "source_subscriber_id": "sub-1",
            "target_representative_id": "missing-rep",
            "token_share": 1.0,
        },
    )

    result = model.step()

    assert result.decisions[0].rule_id == "SIM-RULE-DELEGATION-CREATE"
    assert result.decisions[0].result == "rejected"
    assert "unknown target Representative" in result.decisions[0].reason
