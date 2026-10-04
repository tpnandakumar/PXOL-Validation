# PXOL Real-Engine Integration Map v0.3

This document maps the validation architecture onto the executable PXOL engine in `tpnandakumar/LLM-DEV`.

## Confirmed executable mechanisms

| Validation concept | Existing implementation | Status |
|---|---|---|
| PFLOX front-loading | `pxol/frontload.py`, `pxol/pump_priming.py`, `PXOLModel.pflox_backed()` | Implemented |
| Rear cognitive guidance | `pxol/rear_guided.py`, guidance packet path in `PXOLModel.respond()` | Implemented |
| Outcome-based local learning | `PXOLModel.feedback()`, `success()`, `failure()` | Implemented |
| Multi-guide arbitration | `pxol/multiguide.py` | Implemented |
| Adaptive strategy / complexity control | `pxol/strategy.py`, competence and self-model gating in `PXOLModel.respond()` | Implemented |
| Memory revision / utilisation | `pxol/revision.py`, persistence/utilisation paths | Implemented |
| Pump-prime verification | provisional prime records plus outcome verification/rejection | Implemented |

## New architecture still requiring explicit implementation

### P5D[zD] Tensor Polymatrix
No explicit P5D[zD] state, tensor-polymatrix representation, dimensional escalation/compression controller or dimensional telemetry has yet been identified in the current `pxol` package.

### VCG
Rear guidance is a strong precursor, but VCG requires explicit higher-to-lower dimensional vector guidance, guidance-vector telemetry and an ablation switch. It should not be declared equivalent merely by renaming rear guidance.

### DvD
The existing strategy, competence and self-model gates can contribute to DvD, but DvD requires an explicit decision object with actions such as NONE, LOCAL, UPWARD, DOWNWARD, CROSS, EXPAND and COMPRESS.

### Multidimensional memory
The engine has rich memory and revision behaviour, but the proposed multidimensional memory record requires explicit fields for dimension, context, ecology, trajectory, cause, action, outcome, confidence and vector history.

## Validation rule

The v0.2 synthetic results remain harness-validation results only.

Real-engine claims begin only after:
1. explicit instrumentation exists;
2. components can be independently disabled;
3. the same paired task set is used for full and ablated configurations;
4. outcome scoring is external to the engine;
5. repeated-seed results and confidence intervals are reported.

## Integration sequence

1. Add instrumentation/adapters without changing behaviour.
2. Add explicit VCG and DvD interfaces around existing guidance/strategy mechanisms.
3. Add P5D[zD] state and dimensional telemetry.
4. Extend memory schema for multidimensional linkage.
5. Run smoke tests.
6. Run single-component real ablations.
7. Run full replicated validation.
8. Compare against existing PXOL baseline and conventional sequence-model baselines where appropriate.
