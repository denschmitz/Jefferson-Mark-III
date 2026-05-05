"""Authority lifecycle state machine helpers."""

from __future__ import annotations

from .records import AuthorityLifecycleState, AuthorityRecord


class LifecycleTransitionError(ValueError):
    """Raised when an Authority lifecycle transition is not permitted."""


ALLOWED_AUTHORITY_TRANSITIONS = {
    AuthorityLifecycleState.PROPOSED: {
        AuthorityLifecycleState.CHARTERED,
        AuthorityLifecycleState.REJECTED,
    },
    AuthorityLifecycleState.CHARTERED: {AuthorityLifecycleState.ACTIVE},
    AuthorityLifecycleState.ACTIVE: {
        AuthorityLifecycleState.UNDER_REVIEW,
        AuthorityLifecycleState.SUSPENDED,
        AuthorityLifecycleState.DISSOLVING,
    },
    AuthorityLifecycleState.UNDER_REVIEW: {
        AuthorityLifecycleState.ACTIVE,
        AuthorityLifecycleState.REAUTHORIZATION_REQUIRED,
        AuthorityLifecycleState.SUSPENDED,
        AuthorityLifecycleState.DISSOLVING,
    },
    AuthorityLifecycleState.REAUTHORIZATION_REQUIRED: {
        AuthorityLifecycleState.ACTIVE,
        AuthorityLifecycleState.DISSOLVING,
    },
    AuthorityLifecycleState.SUSPENDED: {
        AuthorityLifecycleState.ACTIVE,
        AuthorityLifecycleState.DISSOLVING,
    },
    AuthorityLifecycleState.DISSOLVING: {AuthorityLifecycleState.DISSOLVED},
    AuthorityLifecycleState.REJECTED: set(),
    AuthorityLifecycleState.DISSOLVED: set(),
    AuthorityLifecycleState.MERGED: set(),
    AuthorityLifecycleState.SEPARATED: set(),
}


ORDINARY_ACTION_STATES = {AuthorityLifecycleState.ACTIVE}


def can_transition_authority(
    from_state: AuthorityLifecycleState, to_state: AuthorityLifecycleState
) -> bool:
    return to_state in ALLOWED_AUTHORITY_TRANSITIONS[from_state]


def transition_authority(
    authority: AuthorityRecord, to_state: AuthorityLifecycleState
) -> None:
    if not can_transition_authority(authority.lifecycle_status, to_state):
        raise LifecycleTransitionError(
            f"invalid Authority lifecycle transition: {authority.lifecycle_status} -> {to_state}"
        )
    authority.lifecycle_status = to_state


def can_execute_ordinary_action(
    authority: AuthorityRecord, review_continuation_allowed: bool = False
) -> bool:
    if authority.lifecycle_status in ORDINARY_ACTION_STATES:
        return True
    return (
        review_continuation_allowed
        and authority.lifecycle_status == AuthorityLifecycleState.UNDER_REVIEW
    )
