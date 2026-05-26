"""Ports for the State Aggregation bounded context.

Ports are interfaces (Protocols) owned by the core. Inbound ports are what
the core OFFERS to be called from outside; outbound ports are what the core
NEEDS from outside and delegates to.

See ADR-002 §"Hexagonal Architecture (Ports & Adapters)" and
research/07-folder-structures.md.
"""

from __future__ import annotations

from typing import Protocol

from ...domain.hbc_msg import HbcMsg
from .house_state_snapshot import HouseStateSnapshot

# ---------------------------------------------------------------------------
# Inbound — use cases the core OFFERS (called by inbound adapters)
# ---------------------------------------------------------------------------


class ForBuildingHbcMsg(Protocol):
    """Called when a relevant entity changes.

    Phase 1 uses a single-value entry point (`on_grid_power`) for the
    proof-of-concept. The eventual shape is "the core reads all relevant
    HA entities and publishes a full HbcMsg" — see the Aggregator.
    """

    def on_grid_power(self, power_w: float) -> None: ...


# ---------------------------------------------------------------------------
# Outbound — use cases the core DELEGATES TO (implemented by outbound adapters)
# ---------------------------------------------------------------------------


class ForReadingHouseState(Protocol):
    """Pull a snapshot of all relevant HA entity states.

    The Aggregator calls this after a trigger fires (e.g. `on_grid_power`)
    to gather the rest of the data it needs to build an HbcMsg. The trigger
    value itself is *not* part of the snapshot — it arrived via the inbound
    port and the core already has it in hand.

    Phase 2 (ADR-002): implemented by an HA adapter that reads entity states
    via `hass.states.get(...)`. Not used in Phase 1 — the Aggregator still
    forwards the raw P1 reading so the existing POC keeps working.
    """

    def read(self) -> HouseStateSnapshot: ...


class ForPublishingHbcMsg(Protocol):
    """Publish a freshly built HbcMsg.

    Phase 2 (ADR-002): implemented by an HA event-bus adapter that fires
    `hbc_msg_ready`. Not used in Phase 1 — the Aggregator scaffolds a
    callback instead so the existing POC keeps working.
    """

    def publish(self, msg: HbcMsg) -> None: ...
