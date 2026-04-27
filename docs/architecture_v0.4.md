# Kairoseed Architecture v0.4

Kairoseed v0.4 introduces a more modular cognitive system design featuring an explicit evaluation layer and a decision compiler.

---

## System Layers

### Layer 1: Generation
Kairoseed creates hypothesis space H using the generator module.

### Layer 2: Evaluation
GSBS maps each hypothesis H → scalar utility score using structured vector scoring.

### Layer 3: Evolution
PEE transforms top hypotheses via:

- mutation
- recombination
- pruning

### Layer 4: Compiler
The new compiler layer translates selected hypotheses into structured decision artifacts.

### Layer 5: Safety (Optional)
AGT acts as an external constraint gate and validation layer.

### Layer 6: Execution
Selected hypothesis becomes action.

### Layer 7: Memory
System updates weights and stores outcomes based on feedback.

---

## v0.4 Design Principles

- explicit separation between evaluation and decision compilation
- modular cognitive layers for research clarity
- support for vector-based hypothesis scoring
- maintainable pipeline orchestration
- optional safety gating via AGT

---

## New v0.4 Components

- `core/compiler.py` — decision compilation layer
- `models/vector.py` — vector representation for GSBS scoring
- `evaluation/` — benchmarking and stability metrics
- `docs/architecture_v0.4.md` — upgraded architecture description
