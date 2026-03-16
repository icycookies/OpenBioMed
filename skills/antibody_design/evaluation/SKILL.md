```
name: claw-antibody-structure-evaluation
version: 0.1.0
description: Structural evaluation of antibody–antigen complexes using UniMoMo DockQ and Rosetta binding energy
author: Jiashuo Wang
license: MIT

tags:
  - antibody-design
  - antibody-evaluation
  - structural-biology
  - docking
  - rosetta
  - dockq

inputs:
  - name: predicted_complex
    type: file
    format: [pdb]
    description: Predicted antibody–antigen complex structure

  - name: reference_complex
    type: file
    format: [pdb]
    optional: true
    description: Reference antibody–antigen complex used for DockQ evaluation

outputs:
  - name: evaluation_report
    type: file
    format: markdown
    description: Structural evaluation report

metadata:
  openclaw:
    category: bioinformatics
    homepage: https://github.com/kxz18/UniMoMo
    min_python: "3.9"

    dependencies:
      - numpy
      - pandas
      - biopython

    system_dependencies:
      - pyrosetta
```

# 🧬 Antibody Complex Evaluation

Evaluate the structural quality of **predicted antibody–antigen complexes** using metrics implemented in the **UniMoMo evaluation toolkit**.

This skill computes:

- **DockQ** (optional, requires reference complex)
- **Rosetta binding energy (ΔG)**

------

# What it does

1. Takes a predicted antibody–antigen complex structure
2. Computes **Rosetta binding energy**
3. Optionally compares the prediction to a reference structure
4. Computes **DockQ docking quality score**
5. Produces a standardized evaluation report

# Environment Setup

All commands below must be executed from the UniMoMo repository directory:

```
cd skills/antibody_design/unimomo/repo
```

Create the environment:

```
conda env create -f env_cuda117.yaml
conda activate UniMoMo
```

Alternatively:

```
env_cuda121.yaml
```

for CUDA 12 + PyTorch 2.1.

# Evaluation Pipeline

## 1. Rosetta Binding Energy

Binding energy is computed using:

```
UniMoMo/evaluation/energy.py
```

Example command:

```
python evaluation/energy.py \
'{"pdb_path":"sample.pdb","receptor_chains":["A"],"ligand_chains":["B"],"relax":true}'
```

Example output:

```
-27.6
```

Lower values indicate stronger predicted binding.

------

# 2. DockQ Evaluation (optional)

DockQ measures similarity between the predicted complex and a **reference antibody–antigen complex**.

Script:

```
UniMoMo/evaluation/dockq.py
```

Example command:

```
python evaluation/dockq.py sample.pdb reference.pdb A B
```

Example output:

```
0.74
```

------

# Automatic Report Generation

The evaluation results can be written to a Markdown report using the following workflow:

```
ENERGY=$(python evaluation/energy.py \
'{"pdb_path":"sample.pdb","receptor_chains":["A"],"ligand_chains":["B"],"relax":true}')

echo "# Antibody Complex Evaluation" > evaluation_report.md
echo "" >> evaluation_report.md

echo "## Input" >> evaluation_report.md
echo "Predicted complex: sample.pdb" >> evaluation_report.md

echo "" >> evaluation_report.md
echo "## Rosetta Binding Energy" >> evaluation_report.md
echo "$ENERGY" >> evaluation_report.md

if [ -f reference.pdb ]; then
    DOCKQ=$(python evaluation/dockq.py sample.pdb reference.pdb A B)

    echo "" >> evaluation_report.md
    echo "## DockQ Score" >> evaluation_report.md
    echo "$DOCKQ" >> evaluation_report.md
fi
```

This generates:

```
evaluation_report.md
```

Example report:

```
Antibody Complex Evaluation
===========================

Predicted complex: sample.pdb

Rosetta binding energy (dG): -27.6

DockQ score: 0.74
```

# Interpretation Guide

- **DockQ** measures the structural similarity between the predicted antibody–antigen complex and a reference complex. It summarizes multiple interface metrics including interface RMSD, ligand RMSD, and native contact recovery.
- Higher **DockQ** scores indicate that the predicted binding interface more closely matches the reference complex geometry.
- **Rosetta binding energy (ΔG)** estimates the interaction energy between the antibody and antigen using the Rosetta scoring function.
- Lower (more negative) **ΔG** values generally indicate stronger predicted binding interactions between the antibody and antigen.

# Citation

If you use this evaluation pipeline, please cite:

```
Kong et al. (2025)
UniMoMo: Unified Generative Modeling of 3D Molecules
for De Novo Binder Design
ICML 2025
```