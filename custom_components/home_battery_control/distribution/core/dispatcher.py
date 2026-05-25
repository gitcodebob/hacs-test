"""Dispatcher — use-case implementation for ForDispatchingSolution.

Phase 2 stub. Iterates Solution.setpoints (keyed by asset name) and
delegates each to its registered ForCommandingAsset implementation.

See ADR-002 §"Distribution".
"""

from __future__ import annotations

import logging

from ...domain.solution import Solution
from .ports import ForCommandingAsset

_LOGGER = logging.getLogger(__name__)


class Dispatcher:
    """Routes per-asset setpoints to the right commanders."""

    def __init__(self, commanders: dict[str, ForCommandingAsset]) -> None:
        self._commanders = commanders

    def dispatch(self, solution: Solution) -> None:
        # TODO Phase 2: for each (asset_name, setpoints) pair, look up the
        #               commander and call commander.command(setpoints).
        raise NotImplementedError("Phase 2 — distribution pipeline not yet wired")
