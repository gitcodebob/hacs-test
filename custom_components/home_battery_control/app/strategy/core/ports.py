"""Ports for the Strategy bounded context.

See ADR-002 §"Hexagonal Architecture (Ports & Adapters)" and
research/07-folder-structures.md.
"""

from __future__ import annotations

from typing import Protocol

from ...domain.hbc_msg import HbcMsg
from ...domain.solution import Solution

# ---------------------------------------------------------------------------
# Inbound — use cases the core OFFERS (called by inbound adapters)
# ---------------------------------------------------------------------------


class ForProducingSolution(Protocol):
    """Produce a Solution.

    Long-term shape (Phase 2+): `produce(msg: HbcMsg) -> Solution`.
    Phase 1 uses a transitional `on_grid_power(power_w)` until the
    Aggregator publishes proper HbcMsg objects through the event bus.
    """

    def on_grid_power(self, power_w: float) -> None: ...


# ---------------------------------------------------------------------------
# Outbound — use cases the core DELEGATES TO (implemented by outbound adapters)
# ---------------------------------------------------------------------------


class ForPublishingSolution(Protocol):
    """Publish a Solution.

    Phase 2 (ADR-002): implemented by an HA event-bus adapter that fires
    `hbc_solution_ready`. The Distribution context's inbound listener
    subscribes to that event.
    """

    def publish(self, solution: Solution) -> None: ...
