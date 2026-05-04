"""Validation reports for configuration, state, and rule metadata."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .records import to_primitive


class ValidationSeverity(StrEnum):
    ERROR = "error"
    WARNING = "warning"
    NOTICE = "notice"


class ValidationFailedError(ValueError):
    """Raised when blocking validation errors are present."""


@dataclass(slots=True)
class ValidationIssue:
    severity: ValidationSeverity
    code: str
    message: str
    path: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return to_primitive(self)


@dataclass(slots=True)
class ValidationReport:
    issues: list[ValidationIssue] = field(default_factory=list)

    def add(
        self,
        severity: ValidationSeverity,
        code: str,
        message: str,
        path: str | None = None,
    ) -> None:
        self.issues.append(
            ValidationIssue(
                severity=severity,
                code=code,
                message=message,
                path=path,
            )
        )

    def error(self, code: str, message: str, path: str | None = None) -> None:
        self.add(ValidationSeverity.ERROR, code, message, path)

    def warning(self, code: str, message: str, path: str | None = None) -> None:
        self.add(ValidationSeverity.WARNING, code, message, path)

    def notice(self, code: str, message: str, path: str | None = None) -> None:
        self.add(ValidationSeverity.NOTICE, code, message, path)

    @property
    def has_errors(self) -> bool:
        return any(issue.severity == ValidationSeverity.ERROR for issue in self.issues)

    def extend(self, other: "ValidationReport") -> None:
        self.issues.extend(other.issues)

    def assert_valid(self) -> None:
        if self.has_errors:
            messages = "; ".join(issue.message for issue in self.issues if issue.severity == ValidationSeverity.ERROR)
            raise ValidationFailedError(messages)

    def to_dict(self) -> dict[str, Any]:
        return {"issues": [issue.to_dict() for issue in self.issues]}
