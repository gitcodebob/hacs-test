"""Ports for the Distribution bounded context.

See ADR-002 §"Hexagonal Architecture (Ports & Adapters)" and
research/07-folder-structures.md.
"""

from __future__ import annotations

from typing import Any, Protocol

from ...domain.solution import Solution

# ---------------------------------------------------------------------------
# Inbound — use cases the core OFFERS (called by inbound adapters)
# ---------------------------------------------------------------------------


class ForDispatchingSolution(Protocol):
    """Dispatch a Solution to the right device commanders.

    Implemented by the Dispatcher. Iterates per-asset setpoints and routes
    each to its commander (ForCommandingAsset implementation).
    """

    def dispatch(self, solution: Solution) -> None: ...


# ---------------------------------------------------------------------------
# Outbound — use cases the core DELEGATES TO (implemented by outbound adapters)
# ---------------------------------------------------------------------------


class ForCommandingAsset(Protocol):
    """Command a single configured asset (battery, EV charger, …).

    One implementation per asset type (see ADR-005). Each adapter knows
    the HA service calls or protocol details for its device.
    """

    asset_name: str
    """Identifies which asset this adapter commands (e.g., "battery")."""

    def command(self, setpoints: dict[str, Any]) -> None: ...
