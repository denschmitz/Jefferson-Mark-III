# Simulation Code

This folder is reserved for executable simulation code.

The intended architecture is:

- `src/jefferson_sim/engine/`: pure Python Charter rules engine.
- `src/jefferson_sim/mesa_adapter/`: Mesa model, agent, scenario, and metric integration.
- `tests/`: rules-engine and Mesa-adapter tests.

The engine should be implemented before Mesa-specific behavior so charter compliance can be tested independently from the simulator runtime.
