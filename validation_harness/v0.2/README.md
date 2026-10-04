# PXOL/PFLOX VCG-P5D[zD] Validation Harness v0.2

Version 0.2 strengthens the first harness by adding **30-seed replicated paired ablation testing**.

## Why this matters

A single run can make a component look better or worse because of stochastic variation.
v0.2 therefore:

- gives every architecture configuration the same task set for each seed
- repeats the experiment across 30 seeds
- calculates mean effect, standard deviation and 95% confidence intervals
- labels effects as PASS, WATCH or FAIL against prespecified practical thresholds

## Interpretation

**PASS** means the observed synthetic effect is positive and its 95% confidence interval clears the practical threshold.

**WATCH** means the result is uncertain or mixed.

**FAIL** means the component is associated with a reproducible adverse effect in this synthetic implementation.

None of these synthetic results validates the real architecture. The purpose is to prove that the harness can detect positive, neutral and adverse component effects rather than automatically favouring the proposed model.

## Next integration step

Replace `SyntheticPXOLAgent` with the real PXOL/PFLOX engine while keeping:

- identical task sets
- paired ablations
- repeated seeds
- prespecified metrics
- the same reporting pipeline

Only those real-engine results can support architectural claims.
