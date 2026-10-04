# Portable execution directory

This directory is a self-contained convenience copy of the principal late-stage Paper-IV execution path.

It combines:

- the `ORIGINAL` base reactor (`reactor_v012.py`);
- the three `REFERENCE_RECONSTRUCTION` dependencies;
- path-only `PORTABLE_ADAPTATION` copies of the six `TRANSCRIPT_RECOVERED` late-stage runners.

The exact transcript-recovered files remain unchanged under `../transcript_recovered/`. The only intended change in the portable copies is replacement of the transient `/mnt/data` dependency path with the current directory so the scripts can be run from a normal clone.

Examples:

```bash
cd code/portable
python reactor_relational_rotation.py
python reactor_full_loop_operator_gain_diagnostic.py
python reactor_loop_half_operator_factorization_diagnostic.py
```

The full confirmatory runs can be invoked by importing each runner and passing its frozen seed cohort; the direct `__main__` blocks of the reconstructed operator runners execute the documented eight-seed validation subsets.
