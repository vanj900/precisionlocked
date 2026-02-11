# Computational Specification: Trauma as Precision-Weighting Disorder

## Mathematical Formulation

### 1. Generative Model

The Active Inference agent maintains a generative model that factorizes as:

```
P(o, μ) = P(o | μ) · P(μ)
```

Where:
- `o` ∈ ℝ: Sensory observation (0 = safe, 1 = threat)
- `μ` ∈ [0,1]: Agent's belief about threat level
- `P(o | μ)`: Likelihood (sensory precision)
- `P(μ)`: Prior belief distribution

### 2. Gaussian Parameterization

Both distributions are Gaussian with fixed precision (inverse variance):

**Likelihood:**
```
P(o | μ) = 𝒩(o; μ, Π_likelihood⁻¹)
```

**Prior:**
```
P(μ) = 𝒩(μ; μ_prior, Π_prior⁻¹)
```

Where:
- `Π_likelihood`: Precision of sensory observations (trust in current signals)
- `Π_prior`: Precision of prior belief (rigidity of past learning)

### 3. Variational Free Energy

The agent's objective is to minimize Variational Free Energy (VFE), which upper-bounds surprise:

```
F = E_Q(μ)[log Q(μ) - log P(o, μ)]
```

For Gaussian distributions, this simplifies to the **precision-weighted prediction error**:

```
F = (o - μ)² · Π_likelihood + (μ - μ_prior)² · Π_prior
```

**Intuition:**
- First term: Sensory prediction error (discrepancy between observation and belief)
- Second term: Prior divergence (discrepancy between current belief and learned prior)

### 4. Belief Update Dynamics

The agent updates beliefs via **gradient descent** on Free Energy:

```
dμ/dt = -η · ∂F/∂μ
```

**Gradient Computation:**
```
∂F/∂μ = -2(o - μ) · Π_likelihood + 2(μ - μ_prior) · Π_prior
```

**Discrete-Time Update:**
```
μ_(t+1) = μ_t - dt · ∂F/∂μ
```

### 5. Trauma as Pathological Precision

**Normal State:**
```
Π_prior ≈ 1.0
```
- Balanced weighting of prior and sensory evidence
- Belief updates adaptively: μ → o

**Trauma State:**
```
Π_prior → ∞  (e.g., 10,000)
```
- Prior dominates sensory evidence
- Gradient becomes:
  ```
  ∂F/∂μ ≈ 2(μ - μ_prior) · Π_prior
  ```
- Belief frozen at prior: μ ≈ μ_prior (trauma lock)

### 6. Computational Stiffness

The trauma condition creates a **stiff differential equation**, requiring adaptive time stepping:

**Normal Integration:**
```
dt_normal = 0.01
```

**Trauma Integration:**
```
dt_trauma = 0.00005  (200× smaller)
```

This reflects **Allostatic Load Theory**: the traumatized agent requires ~200× more computational cycles to process the same time window.

### 7. Therapeutic Annealing

Therapy corresponds to **precision annealing**:

```
Π_prior: 10,000 → 1.0
```

**Mechanism:**
- Reduces the weight of the traumatic prior
- Restores sensitivity to sensory prediction errors
- Enables belief updating: μ can move toward o

**Biological Correlate:**
- Memory reconsolidation: weakening synaptic weights of trauma memory
- Vagal tone restoration: downregulating sympathetic rigidity

### 8. Implementation Notes

**Stability Constraint:**
For numerical stability with explicit Euler integration:

```
dt < 2 / (max eigenvalue of Hessian)
dt < 1 / Π_prior
```

Hence for Π_prior = 10,000:
```
dt < 0.0001  (we use 0.00005 for safety margin)
```

**Convergence Criterion:**
The annealed agent converges to the posterior mean:

```
μ_∞ = (μ_prior · Π_prior + o · Π_likelihood) / (Π_prior + Π_likelihood)
```

For Π_prior = 1, Π_likelihood = 1, μ_prior = 0.9, o = 0:
```
μ_∞ = (0.9 · 1 + 0 · 1) / (1 + 1) = 0.45
```

### 9. Falsifiable Predictions

This model makes testable predictions:

1. **Psychophysics**: Trauma survivors should show reduced sensory gain (effective Π_likelihood ↓) for safety signals
2. **Neuroimaging**: High amygdala precision (Π_prior) should correlate with insula-based prediction error suppression
3. **Therapy Outcome**: Successful therapy should show decreased resting-state connectivity in prior-encoding networks

### 10. Extensions

**Hierarchical Precision:**
```
μ_t^(i) ← μ_t^(i) - dt · (ε_t^(i) · Π^(i) - ε_t^(i+1) · Π^(i+1))
```

Where `ε_t^(i)` is prediction error at level `i`.

Trauma can lock any level of the hierarchy, creating:
- **Cognitive trauma**: frozen conceptual priors
- **Somatic trauma**: frozen autonomic setpoints
- **Social trauma**: frozen interpersonal expectations

---

## References

- Friston, K. (2010). The free-energy principle: a unified brain theory? *Nature Reviews Neuroscience*, 11(2), 127-138.
- Porges, S. W. (2011). The Polyvagal Theory. *W. W. Norton & Company*.
- Ecker, B., Ticic, R., & Hulley, L. (2012). *Unlocking the Emotional Brain*. Routledge.
