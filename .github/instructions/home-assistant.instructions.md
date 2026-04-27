---
applyTo: "**/*.yaml"
---

Always use modern Home Assistant YAML syntax (post-2024.10). Use the `trigger:` key with inline type notation (e.g., `trigger: state`) instead of the legacy `platform:` style. Apply this consistently across automations and trigger-based template sensors.
