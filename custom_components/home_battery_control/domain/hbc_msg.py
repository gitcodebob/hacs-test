"""HbcMsg — the central data contract.

See ADR-002 §"The HbcMsg — Central Data Contract" for the full schema.
Phase 1 scaffold: only the fields the current proof-of-concept needs.
Expand as the architecture lights up.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class HbcMsg:
    """Central data contract passed through the pipeline."""

    version: int = 1
    timestamp: datetime | None = None
    grid_power_w: float | None = None
    devices: dict[str, dict[str, Any]] = field(default_factory=dict)
    settings: dict[str, dict[str, Any]] = field(default_factory=dict)
    plan: dict[str, Any] | None = None
    solution: dict[str, Any] | None = None
