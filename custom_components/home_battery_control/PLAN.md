# Implementation Plan — Orchestrator-Driven Control

Build steps derived from the `decisions-mk2` ADRs
([002](../../project/decisions-mk2/ADR-002-control-architecture.md) orchestrator ·
[004](../../project/decisions-mk2/ADR-004-planning-context.md) planning ·
[005](../../project/decisions-mk2/ADR-005-resource-abstraction.md) resources ·
[006](../../project/decisions-mk2/ADR-006-optimizer-technology.md) optimizer).

Each step ends at an **intermediate testable result**. Steps 1–7 deliver ADR-002
Phase 1 (orchestrator + battery, all three guards). Steps 8–11 add the later phases.
Tests run via `uv run pytest` (ADR-001 Option A); HA-level checks via the devcontainer
(ADR-001 Option B).

---

### 1. Scaffold the `/app` directory
Create the package skeleton from ADR-002/005: `control/core/ports/` (with `inbound.py`
and `outbound.py` port modules), `resources/`, `strategy/`, `planning/`, `market/`, each
package with `__init__.py`. No logic yet.
**Test:** `import` of every package succeeds; pytest collects an empty suite green.

### Todo — refine Plan and HouseState
Before step 2 nails down the schemas, resolve the open questions in the ADRs so the
value-object shapes don't get versioned twice:
- **`plan` shape — RESOLVED: current slot only.** `HouseState` is a snapshot of the
  *current* state of the house, so `HouseState.plan` carries only the current slot (resolved
  setpoints for now), never the whole horizon. The full horizon lives in the planning
  context (`sensor.hbc_plan`); gather projects the current slot into `HouseState`. This drops
  the ADR-005 `plan.slots[*]` array form. Keep the slot keyed by resource name (not flat
  `battery_power_w` fields) so it matches `HouseState.resources` / `Solution`.
- **Meter/prices placement.** Decide whether observable-only resources live under
  `resources` (read like any resource) or are promoted to top-level fields (`grid_power_w`,
  `prices`), as ADR-004's JSON shows. Settles whether `resources` is controllable-only.
- **`resources` value type.** `dict[str, ResourceState]` (typed) vs `dict[str, dict]` (raw,
  as in the JSON example).
- **`settings`** appears in the ADR-004 schema but is defined nowhere — what feeds it, and
  is it in scope for Phase 1?
- **`HouseState` vs `GridContext`.** The ADRs pair them; decide whether one composes the
  other or they stay independent, since step 2 defines both.
- **Representation.** Frozen dataclass vs pydantic, given "pure Python, no HA imports".

### 2. Core value objects & port protocols
Define the cross-context payloads — `HouseState` (incl. `plan=None`), `Solution`,
`ResourceState`, `GridContext` — and the port `Protocol`s: `ForGatheringState`,
`ForProducingSolution`, `ForApplyingSolution`, `ForReadingResourceState`,
`ForCommandingResource`, `ForRunningControlCycle`. Pure Python, no HA imports.
**Test:** construct each value object; assert protocol method signatures.

### 3. `ControlCycle` orchestrator against fake phases
Implement the thin orchestrator: sequencing + single-flight/trailing-coalesce +
timeout→fallback + monotonic `cycle_id` correlation. No phase logic inside.
**Test:** unit tests with fake gather/decide/apply prove each guard — concurrent triggers
collapse to one trailing re-run; a slow `produce` yields the fallback solution; a stale
`cycle_id` is dropped.

### 4. Resource model: registry + battery + meter
`RESOURCE_REGISTRY`, `ResourceConfig`, the `battery` slice (model + read/command adapter,
e.g. a fake/Huawei) and the observable-only `meter` slice (read only). Read against a fake
HA state, command against a fake service registry.
**Test:** battery `read()` maps fake SoC → `ResourceState`; `command()` calls the right
service; meter exposes read only.

### 5. Gather & Apply phase implementations
`gather.py` fans in all registered resources (+ meter, `plan=None`) into `HouseState`;
`apply.py` fans out a `Solution` to `ForCommandingResource` per named controllable resource.
**Test:** gather assembles a `HouseState` from fake resources; apply commands exactly the
resources named in the solution.

### 6. First Python strategy (self-consumption)
A synchronous `ForProducingSolution` implementation: given `HouseState`, produce a
battery `Solution` (e.g. hold grid exchange toward zero / self-consumption default), which
also serves as the orchestrator fallback.
**Test:** representative `HouseState` → expected per-resource setpoints.

### 7. Wire into Home Assistant (Phase 1 complete)
`__init__.py` setup builds the wiring; inbound adapters (P1 meter listener + cycle timer)
trigger `ControlCycle`; config flow gains the battery sub-entry; publish the
`hbc_last_decision` diagnostic entity.
**Test (devcontainer):** a `sensor.fake_p1` change drives one cycle and commands the
battery; `hbc_last_decision` shows the `cycle_id`, state digest and whether fallback fired.

### 8. PID control-primitive + strategy selection
Add the stateful PID primitive in `strategy/core/` (integral/prev-error persisted across
cycles by the orchestrator-owned instance) and a HA `select` to pick the active strategy.
**Test:** PID converges to setpoint over successive cycles; switching the select swaps the
active `ForProducingSolution`.

### 9. Node-RED bridge (second strategy implementation)
A `ForProducingSolution` that publishes `hbc_state_ready` (state + `cycle_id`) and awaits
`hbc_solution_ready`, behind the same uniform port. The Step-3 guards harden the seam.
**Test:** matching `cycle_id` resolves to a `Solution`; timeout and stale/mismatched replies
fall back without wedging the loop.

### 10. Additional resources + market context
New vertical slices `ev_charger` and `heat_pump` via one registry line each; a `market`
inbound adapter publishing `sensor.hbc_prices`, folded into `HouseState` by gather.
**Test:** registering a slice makes its state appear in `HouseState` and its setpoints
applied, with zero orchestrator changes; gather includes current price.

### 11. Planning context (MILP)
`planning/` builds a Pyomo/HiGHS MILP from the controllable resources' `Resource` facet on
its own cadence, offloaded via `async_add_executor_job`, publishing `sensor.hbc_plan` (+
`sensor.hbc_plan_current`). A plan-following strategy reads `HouseState.plan` with the
freshness/fallback policy.
**Test:** solver emits a horizon to `sensor.hbc_plan`; gather surfaces the current slot;
plan-following strategy tracks it and falls back when the plan is stale/infeasible.
