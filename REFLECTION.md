# Understanding the Dependency Graph and Reflection — Make vs run_all.sh

1. If `code/preprocess.py` is edited:
   - Make rebuilds:
     - `output/figures/figure_5_2.png`
     - `output/figures/figure_5_3.png`
     - `paper/paper.pdf` (because it depends on the figures)
   - Make skips:
     - `output/tables/did_table.tex` (since `did_analysis.py` did not change)

2. If `code/did_analysis.py` is edited:
   - Make rebuilds:
     - `output/tables/did_table.tex`
     - `paper/paper.pdf` (because it depends on the DID table)
   - Make skips:
     - `output/figures/figure_5_2.png`
     - `output/figures/figure_5_3.png` (since `preprocess.py` did not change)

3. If `paper/paper.tex` is edited:
   - Make rebuilds:
     - `paper/paper.pdf` only
   - Make skips:
     - All Python scripts and intermediate outputs

---

## Reflection

The Makefile makes the project’s dependency structure explicit by clearly listing which outputs depend on which inputs and scripts. In contrast, `run_all.sh` encodes the workflow as a simple sequence of commands, leaving the dependency relationships implicit. By declaring targets and their dependencies, Make automatically determines what needs to be rebuilt and avoids unnecessary computation. This not only improves efficiency but also documents the logical structure of the project for collaborators. Reading the Makefile reveals the full dependency graph of the replication workflow.