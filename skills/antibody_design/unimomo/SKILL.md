```
name: claw-unimomo-antibody-design
version: 0.1.0
description: Antibody CDR design using the UniMoMo 3D generative model
author: Jiashuo Wang
license: MIT

tags:
  - antibody-design
  - protein-design
  - structural-biology
  - generative-model
  - unimomo
  - cdr-design

inputs:
  - name: antigen_antibody_complex
    type: file
    format: [pdb]
    description: Antigen–antibody complex structure with antibody renumbered in Chothia scheme

  - name: config
    type: file
    format: [yaml]
    description: UniMoMo antibody generation configuration

outputs:
  - name: antibody_candidates
    type: directory
    description: Generated antibody CDR candidate structures

  - name: evaluation_report
    type: file
    format: markdown
    description: Antibody design evaluation report including structural metrics

metadata:
  openclaw:
    category: bioinformatics
    homepage: https://github.com/kxz18/UniMoMo
    min_python: "3.9"

    dependencies:
      - pytorch
      - numpy
      - pandas
      - biopython
      - pyyaml

    system_dependencies:
      - cuda
      - conda
```
---

# 🧬 UniMoMo Antibody CDR Design

Design **antibody CDR loops** against a target protein using the **UniMoMo unified 3D generative model**.

UniMoMo is a generative diffusion model trained to design molecular binders by modeling **all-atom interactions in protein binding sites**.

# What it does

1. Takes a **target protein–antibody complex structure** as input
2. Uses the **UniMoMo generative model** to redesign antibody CDR loops
3. Generates candidate CDR structures conditioned on the antigen binding site
4. Evaluates generated antibody structures using structural and docking metrics
5. Produces a report summarizing design quality

------

# Why this exists

If a general AI system is asked to redesign antibody CDRs, it may:

- ignore antibody structural constraints
- generate unrealistic loop conformations
- fail to evaluate docking compatibility with the antigen

This skill encodes a **reproducible antibody design workflow**:

- uses a **trained 3D generative model**
- conditions generation on the **antigen–antibody interface**
- evaluates designs using **standard structural metrics**
- produces interpretable evaluation statistics

------

# Model Checkpoint

All commands below must be executed from the UniMoMo repository directory:

```
cd skills/antibody_design/unimomo/repo
```

Before running the pipeline, download the pretrained model:

```
mkdir checkpoints
cd checkpoints

wget https://github.com/kxz18/UniMoMo/releases/download/v1.0/model.ckpt
```

The checkpoint must be located at:

```
./checkpoints/model.ckpt
```

------

# Environment Setup

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

------

# Antibody Design Pipeline

### 1. Input preparation

Provide a **reference antigen–antibody complex**.

The antibody must be **renumbered using the Chothia numbering system** so that UniMoMo can identify CDR regions.

Example renumbering:

```
cd api

python renumber.py \
    demo/reference_complex.pdb \
    demo/reference_chothia.pdb \
    chothia
```

------

### 2. Configuration

Define a config file specifying:

- target chain
- antibody chain
- CDR region to redesign

Example:

```
dataset:
  pdb_paths:
    - ./reference_chothia.pdb

  tgt_chains:
    - A

  lig_chains:
    - H

templates:

  - class: Antibody
    cdr_type: HCDR3

batch_size: 8
n_samples: 20
```

------

### 3. Antibody Generation (single PDB)

Run UniMoMo on the specific structure:

```
python -m api.generate \
    --config config.yaml \
    --ckpt checkpoints/model.ckpt \
    --save_dir generations \
    --gpu 0
```

This command generates **candidate antibody CDR designs for the given PDB structure**.

The results will be stored in:

```
generations/
```

------

# Evaluation

Evaluation scripts provided in UniMoMo evaluate generated antibodies using structural metrics.

Run evaluation:

```
python -m scripts.metrics.peptide \
    --results generations/results.jsonl \
    --antibody \
    --log_suffix HCDR3 \
    --num_workers 96 \
> evaluation_report.md
```

------

# Example Evaluation Output

Evaluation results typically appear in the following format:

```
Point-wise evaluation results:

AAR (mean): 0.5195516666666666
        lowest: 0.3, id: 4xnq_D_B_A/HCDR3
        highest: 0.8571, id: 5d93_A_C_B/HCDR3
        correlation with flow matching likelihood: -0.0565

C_RMSD(CA) (median): 0.885
        lowest: 0.2, id: 2dd8_S_H_L/HCDR3
        highest: 3.02, id: 3h3b_A_c_C/HCDR3

L_RMSD(CA) (median): 0.59
        lowest: 0.09, id: 4cmh_A_B_C/HCDR3
        highest: 2.57, id: 3h3b_A_c_C/HCDR3

DockQ (mean): 0.9569499999999999
        lowest: 0.772, id: 3h3b_A_c_C/HCDR3
        highest: 0.999, id: 4cmh_A_B_C/HCDR3

Clash_inner (mean): 0.0015806500000000003
Clash_outer (mean): 0.0003739333333333336

dG (mean): 9.009833333333331
```

------

# Interpretation Guide

Important metrics:

| Metric     | Meaning                       |
| ---------- | ----------------------------- |
| **AAR**    | Amino-acid recovery rate      |
| **C_RMSD** | Backbone structural deviation |
| **L_RMSD** | Loop structural deviation     |
| **DockQ**  | Docking interface quality     |
| **Clash**  | Atomic steric clashes         |
| **dG**     | Binding free energy estimate  |

# Citation

If you use this skill in a publication, please cite:

```
Kong et al. (2025)
UniMoMo: Unified Generative Modeling of 3D Molecules
for De Novo Binder Design
ICML 2025
```