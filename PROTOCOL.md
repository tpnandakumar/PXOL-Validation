# PXOL 1.0 Fixed External Validation Protocol

## Objective

Independently test PXOL 1.0 for reproducibility, functional correctness, state continuity, learning behaviour, ablation sensitivity and comparative performance.

## Rules

1. Record OS, Python version, hardware and PXOL commit or package checksum.
2. Do not alter PXOL source before completing the fixed protocol.
3. Use the supplied dataset and seven supplied configurations first.
4. Run each stochastic condition with at least five seeds where the benchmark exposes a seed.
5. Preserve all raw console output and machine-readable result files.
6. Report negative, null and positive outcomes.
7. Separate confirmatory runs from later exploratory runs.
8. State any protocol deviation explicitly.

## Required sequence

- V1 Installation and product acceptance: `pxol-product-check`
- V2 Baseline comparison: `pxol-baseline-comparison`
- V3 Stage ablation: `pxol-stage-ablation`
- V4 Stage profile: `pxol-stage-profile`
- V5 Restart continuity: `pxol-restart-benchmark`
- V6 Self-memory behaviour: `pxol-self-memory-benchmark`
- V7 Longitudinal autonomy: `pxol-autonomy-benchmark`
- V8 Regulation and distributed behaviour: `pxol-regulation-benchmark`, `pxol-distributed-benchmark`
- V9 Native and EPP benchmarks: `pxol-benchmark`, `pxol-epp-benchmark`

## Interpretation

A positive result is evidence for that tested condition, not proof of universal superiority. A null result means no measurable advantage was demonstrated under that condition. A negative result must be retained and investigated rather than removed from the report.
