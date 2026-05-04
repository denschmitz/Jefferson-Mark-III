"""Approval threshold helpers for first-pass Charter mechanics."""

from __future__ import annotations

from .records import ApprovalRecord, ThresholdResult


COERCIVE_AUTHORITY_THRESHOLD = 0.75
NON_COERCIVE_AUTHORITY_THRESHOLD = 0.60


def authority_formation_threshold(coercive_status: bool) -> float:
    return COERCIVE_AUTHORITY_THRESHOLD if coercive_status else NON_COERCIVE_AUTHORITY_THRESHOLD


def approval_passes_threshold(record: ApprovalRecord, threshold: float | None = None) -> bool:
    required = record.threshold_required if threshold is None else threshold
    return record.approval_ratio >= required


def evaluate_approval_record(record: ApprovalRecord, threshold: float | None = None) -> ThresholdResult:
    return ThresholdResult.PASS if approval_passes_threshold(record, threshold) else ThresholdResult.FAIL
