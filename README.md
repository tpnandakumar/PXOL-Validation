# PXOL Validation

Public external-validation and contribution area for PXOL.

The PXOL core development repository remains private. This repository contains only material intentionally released for independent testing, reproducibility work, validator feedback, suggested improvements and formal sign-off.

## Validator portal

The public site is served from the `docs/` directory.

Validators can:
- follow the fixed PXOL validation protocol
- preserve and submit evidence
- submit suggested improvements and example code
- formally sign off their validation

## Suggested improvements

Create one folder inside `suggested_improvements/`:

```
suggested_improvements/
  surname_topic_001/
    README.md
    proposed_code.py
    evidence.md
    results.csv
```

Submit the folder by pull request.

All code in `suggested_improvements/` is **PROPOSED CODE, NOT PXOL CORE** until separately reviewed, tested and incorporated by the PXOL maintainers.

## Validation sign-off

Each completed validation should use a unique record such as `PXOL-EV-2026-0001`.

See `validation_results/README.md`.
