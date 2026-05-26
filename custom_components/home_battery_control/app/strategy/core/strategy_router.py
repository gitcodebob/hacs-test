"""StrategyRouter — selects which strategy implementation is active.

Phase 1 scaffold: holds a single active strategy. Becomes meaningful in
Phase 2 when multiple Python strategy implementations land
(self-consumption, dynamic tariff, …).

See ADR-002 §"Phased Delivery".
"""

from __future__ import annotations

from .ports import ForProducingSolution


class StrategyRouter:
    """Phase-1 stub: exposes the single configured strategy."""

    def __init__(self, strategy: ForProducingSolution) -> None:
        self._strategy = strategy

    @property
    def active(self) -> ForProducingSolution:
        return self._strategy
