#!/usr/bin/env python3
"""
Trauma as a Precision-Weighting Disorder
Active Inference Simulation Kernel

This module implements the core computational model of trauma as a pathologically 
high-precision prior that prevents belief updating in response to safety signals.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple


class ActiveInferenceAgent:
    """
    An Active Inference agent that updates beliefs via gradient descent on 
    Variational Free Energy (VFE).
    
    Key Dynamics:
    - Belief update: dμ/dt ∝ -∂F/∂μ
    - Free Energy: F = (o - μ)² Π_likelihood + (μ - μ_prior)² Π_prior
    - Trauma: Π_prior → ∞, forcing μ ≈ μ_prior (frozen belief)
    """
    
    def __init__(
        self, 
        mu_prior: float = 0.9,
        pi_prior: float = 1.0,
        pi_likelihood: float = 1.0,
        dt_normal: float = 0.01,
        dt_trauma: float = 0.00005
    ):
        """
        Initialize the Active Inference agent.
        
        Args:
            mu_prior: Prior belief (default: 0.9 = high threat expectation)
            pi_prior: Precision of the prior (trauma: ~10,000, normal: ~1.0)
            pi_likelihood: Precision of sensory observations
            dt_normal: Time step for normal belief updating
            dt_trauma: Time step for trauma state (stiff gradient)
        """
        self.mu = mu_prior  # Current belief state
        self.mu_prior = mu_prior
        self.pi_prior = pi_prior
        self.pi_likelihood = pi_likelihood
        self.dt_normal = dt_normal
        self.dt_trauma = dt_trauma
        
    def free_energy_gradient(self, observation: float) -> float:
        """
        Compute the gradient of Variational Free Energy with respect to belief μ.
        
        ∂F/∂μ = -2(o - μ)Π_likelihood + 2(μ - μ_prior)Π_prior
        
        Args:
            observation: Sensory observation (0 = safe, 1 = threat)
            
        Returns:
            Gradient of free energy
        """
        prediction_error = observation - self.mu
        prior_divergence = self.mu - self.mu_prior
        
        gradient = (
            -2 * prediction_error * self.pi_likelihood +
            2 * prior_divergence * self.pi_prior
        )
        
        return gradient
    
    def update_belief(self, observation: float, steps: int = 1) -> None:
        """
        Update belief via gradient descent on Free Energy.
        
        Args:
            observation: Sensory observation
            steps: Number of integration steps
        """
        # Select adaptive time step based on trauma state
        dt = self.dt_trauma if self.pi_prior > 100 else self.dt_normal
        
        for _ in range(steps):
            gradient = self.free_energy_gradient(observation)
            # Gradient descent: μ_new = μ - dt * ∂F/∂μ
            self.mu = self.mu - dt * gradient
            
            # Bound belief to [0, 1]
            self.mu = np.clip(self.mu, 0.0, 1.0)
    
    def induce_trauma(self, pi_trauma: float = 10000.0) -> None:
        """
        Induce trauma by setting pathologically high prior precision.
        
        Args:
            pi_trauma: Trauma-level precision (default: 10,000)
        """
        self.pi_prior = pi_trauma
        print(f"\n--- INDUCING TRAUMA (Pi_Prior -> {pi_trauma}) ---")
    
    def therapeutic_annealing(self, pi_target: float = 1.0) -> None:
        """
        Simulate therapeutic intervention by annealing prior precision.
        
        Args:
            pi_target: Target precision after therapy (default: 1.0)
        """
        self.pi_prior = pi_target
        print(f"\n--- THERAPY (ANNEALING) Pi_Prior -> {pi_target} ---")


def demonstrate_trauma_trap():
    """
    Demonstrate the 'Trauma Trap' phenomenon:
    - High-precision priors prevent belief updating despite contradictory evidence
    - Therapeutic annealing restores adaptive inference
    """
    print("=" * 60)
    print("TRAUMA AS A PRECISION-WEIGHTING DISORDER")
    print("Active Inference Simulation")
    print("=" * 60)
    
    # ========== TRAUMA CONDITION ==========
    print("\n[1] TRAUMATIZED AGENT")
    print("-" * 60)
    
    # Create agent with trauma-level prior precision
    trauma_agent = ActiveInferenceAgent(
        mu_prior=0.9,           # Prior: "The world is dangerous"
        pi_prior=10000.0,       # Pathologically high precision
        pi_likelihood=1.0
    )
    
    print(f"Initial Belief (μ): {trauma_agent.mu:.4f}")
    print(f"Prior Precision (Π_prior): {trauma_agent.pi_prior}")
    
    # Present safety signals (observation = 0.0)
    observation_safe = 0.0
    trauma_agent.induce_trauma(10000.0)
    
    for step in range(1, 6):
        trauma_agent.update_belief(observation_safe, steps=1000)
        print(f"Step {step}: Belief(μ)={trauma_agent.mu:.4f} (Trauma Locked)")
    
    # ========== THERAPEUTIC ANNEALING ==========
    print("\n[2] THERAPEUTIC INTERVENTION")
    print("-" * 60)
    
    # Reset agent and apply annealing
    annealed_agent = ActiveInferenceAgent(
        mu_prior=0.9,
        pi_prior=1.0,           # Normal precision (annealed)
        pi_likelihood=1.0
    )
    
    annealed_agent.therapeutic_annealing(1.0)
    
    for step in range(1, 6):
        annealed_agent.update_belief(observation_safe, steps=1000)
        print(f"Step {step}: Belief(μ)={annealed_agent.mu:.4f} (Updating...)")
    
    print("\n" + "=" * 60)
    print("CONCLUSION:")
    print("- Trauma: μ remains locked near prior (0.9) despite safety")
    print("- Therapy: μ updates toward observation (0.0)")
    print("=" * 60)


def plot_belief_trajectories():
    """
    Generate visualization of belief trajectories for trauma vs. therapy.
    """
    steps = 100
    observations = np.zeros(steps)  # Safety signals
    
    # Trauma condition
    trauma_agent = ActiveInferenceAgent(mu_prior=0.9, pi_prior=10000.0)
    trauma_trajectory = []
    
    for obs in observations:
        trauma_agent.update_belief(obs, steps=100)
        trauma_trajectory.append(trauma_agent.mu)
    
    # Annealed (therapy) condition
    annealed_agent = ActiveInferenceAgent(mu_prior=0.9, pi_prior=1.0)
    annealed_trajectory = []
    
    for obs in observations:
        annealed_agent.update_belief(obs, steps=100)
        annealed_trajectory.append(annealed_agent.mu)
    
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(trauma_trajectory, 'r-', linewidth=2, label='Trauma (Π=10,000)')
    plt.plot(annealed_trajectory, 'g-', linewidth=2, label='Therapy (Π=1.0)')
    plt.axhline(y=0.0, color='b', linestyle='--', alpha=0.5, label='Safety Signal (o=0)')
    plt.axhline(y=0.9, color='gray', linestyle='--', alpha=0.5, label='Prior (μ₀=0.9)')
    
    plt.xlabel('Time Steps', fontsize=12)
    plt.ylabel('Belief (μ)', fontsize=12)
    plt.title('Trauma Trap vs. Therapeutic Annealing', fontsize=14, fontweight='bold')
    plt.legend(loc='best', fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.ylim(-0.05, 1.05)
    
    plt.tight_layout()
    plt.savefig('trauma_belief_trajectory.png', dpi=300, bbox_inches='tight')
    print("\n📊 Plot saved: trauma_belief_trajectory.png")
    plt.close()


if __name__ == "__main__":
    # Run the core demonstration
    demonstrate_trauma_trap()
    
    # Generate visualization
    try:
        plot_belief_trajectories()
    except Exception as e:
        print(f"\nNote: Plotting skipped ({e})")
        print("Install matplotlib to generate visualizations: pip install matplotlib")
