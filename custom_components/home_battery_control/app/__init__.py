"""Application code for the Home Battery Control integration.

Everything under this package is *inside* the integration's hex-arch
boundary: bounded contexts (aggregation, strategy, distribution, planning)
and the shared domain types they speak. The integration root above this
folder holds only the files Home Assistant requires (manifest.json,
config_flow.py, __init__.py, platform files, …).

See ADR-002 and research/07-folder-structures.md.
"""
