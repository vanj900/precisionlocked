# Trauma as a Precision-Weighting Disorder
## A Computational Formulation of Therapeutic Change via Active Inference

This repository contains the theoretical manuscript, mathematical specification, and executable simulation kernel for the paper **"Trauma as a Precision-Weighting Disorder."** This project unifies the Free Energy Principle (FEP), Polyvagal Theory, and Memory Reconsolidation into a single, falsifiable computational framework. It models psychological trauma not as a vague energetic block, but as a specific breakdown in the precision-weighting dynamics of an Active Inference agent.

## 📂 Repository Structure

* **src/trauma_agent.py**: The executable Python kernel simulating the trauma trap (rigid prior) and therapeutic annealing.
* **docs/paper.md**: The full academic manuscript (submission ready).
* **docs/computational_spec.md**: The explicit mathematical derivation of the generative model and update equations.

## ⚡ The Core Theory

Trauma is defined as a pathologically high-precision prior (Π → ∞) regarding threat, which renders the agent immune to sensory prediction errors (safety signals).

The update logic follows the gradient descent on Variational Free Energy:

```
dμ/dt = -∂F/∂μ = 2(o - μ)Π_likelihood - 2(μ - μ_prior)Π_prior
```

In a trauma state, **Π_prior** dominates, forcing `dμ/dt ≈ 0` (stasis) despite contradictory sensory evidence `o`.

## 🚀 Quick Start

To run the simulation kernel and observe the **"Trauma Trap"** vs. **"Therapeutic Annealing"**:

1. **Clone the repo:**
   ```bash
   git clone https://github.com/vanj900/precisionlocked.git
   cd precisionlocked
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the agent:**
   ```bash
   python src/trauma_agent.py
   ```

## Output Example

The script demonstrates the difference in belief updating (μ) between a traumatized agent (Stiff Gradient) and an annealed agent (Labile Gradient):

```
--- INDUCING TRAUMA (Pi_Prior -> 10,000) ---
Step 1: Belief(μ)=0.8999 (Trauma Locked)

--- THERAPY (ANNEALING) ---
Step 1: Belief(μ)=0.4500 (Updating...)
```

## 🛠️ Computational Constraints

The simulation implements an adaptive integration time step (dt).

* **Normal State:** `dt = 0.01`
* **Trauma State:** `dt = 0.00005` (To handle the stiff gradient of high-precision priors).

This computationally demonstrates the **Allostatic Load theory**: the traumatized agent requires significantly more computational cycles to process the same temporal window.

## 📄 Citation

If you use this code or framework in your research, please link back to this repository.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
