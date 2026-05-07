"""Command-line entry point for running simulation scenarios."""

from __future__ import annotations

from .engine.runner import main


if __name__ == "__main__":
    raise SystemExit(main())
