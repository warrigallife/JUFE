# JUFE / ABTM Specification Engine

This package turns the supplied manuscript and current code into a machine-readable requirements register.

## Files

- `requirements_register.json` — formal requirements extracted from the manuscript and original code
- `specification_engine.py` — coverage, status, category and unresolved-item reports
- `validate_requirements.py` — integrity checker for the register
- `SPECIFICATION_REPORT.txt` — current generated report

## Run

```bash
python3 validate_requirements.py
python3 specification_engine.py
```

## Rule

Every future core module should declare which requirement ID it implements.
