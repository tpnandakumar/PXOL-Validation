# v0.3 Real-Engine Validation Status

## Development repository

Real-engine implementation is being developed in:

- Repository: `tpnandakumar/LLM-DEV`
- Pull request: #4
- Branch: `feature/p5d-vcg-dvd`

## Implemented on the feature branch

- explicit P5D[zD] dimensional controller
- explicit Dynamic Vectoring Decision
- explicit Vector Cognitive Guidance
- opt-in integration switches in `PXOLModelConfig`
- per-turn P5D, DvD and VCG telemetry
- higher dimensional compute-budget modulation
- DvD-triggered guidance escalation
- VCG-triggered higher-to-lower guidance requests
- real-engine vectoring ablation benchmark
- FULL / NO_P5D / NO_DVD / NO_VCG / LEGACY configurations

## Scientific status

No performance claim is made from this stage yet.

The original CI failure was traced to an existing dependency mismatch: matched GRU/LSTM/Transformer cold-start tests require PyTorch, while the workflow installed only the development extra. The feature branch now installs PyTorch in CI.

The branch should be merged only after the complete test suite and G0 benchmark pass.

## Real ablation outputs to publish next

For each configuration:

- externally scored task accuracy
- mean confidence
- guidance interventions
- pump-prime utilisation
- mean active dimensionality
- zD expansions
- VCG vector events
- mean resolver iterations

The objective is to retain a component only when its removal causes a reproducible loss in resolution quality, efficiency, adaptation, transfer or robustness.
