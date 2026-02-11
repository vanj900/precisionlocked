import numpy as np

class ActiveInferenceAgent:
    def __init__(self, prior_mean, prior_precision_val, sensory_precision_val, time_step=0.001):
        """
        Initializes the Active Inference agent.
        
        Args:
            prior_mean (float): The expectation of the prior (eta). E.g., 1.0 = Threat, 0.0 = Safe.
            prior_precision_val (float): Initial precision of the prior (Pi_prior).
            sensory_precision_val (float): Initial precision of sensory input (Pi_sensory).
            time_step (float): 'dt' for Euler integration. 
                               Note: High precision priors require extremely small dt to avoid divergence.
        """
        # Internal Model State (mu) - Initialized to prior expectation
        self.mu = prior_mean
        
        # Generative Model Parameters
        self.eta = prior_mean
        self.pi_prior_base = prior_precision_val
        self.pi_sensory_base = sensory_precision_val
        
        # Current Precision State (Dynamic)
        self.pi_prior = prior_precision_val
        self.pi_sensory = sensory_precision_val
        
        # Integration step size
        self.dt = time_step 
        
        self.history = []

    def observe(self, sensory_input):
        """Receives sensory input (o)."""
        self.observation = sensory_input

    def update_belief(self):
        """
        Performs gradient descent on Variational Free Energy (VFE).
        The update equation: mu_dot = Pi_sensory * (o - mu) - Pi_prior * (mu - eta)
        """
        # 1. Calculate Prediction Errors
        sensory_pe = self.observation - self.mu
        prior_pe = self.mu - self.eta
        
        # 2. Weight Errors by Precision (Gradients)
        # dF/dmu = -Pi_sensory * (o - mu) + Pi_prior * (mu - eta)
        # We move opposite to the gradient to minimize Free Energy.
        weighted_sensory = self.pi_sensory * sensory_pe
        weighted_prior = self.pi_prior * prior_pe
        
        mu_dot = weighted_sensory - weighted_prior
        
        # 3. Euler Integration Step
        self.mu += self.dt * mu_dot
        
        # Logging
        self.history.append({
            'mu': self.mu,
            'pi_prior': self.pi_prior,
            'mu_dot': mu_dot
        })
        
        return self.mu

    def induce_trauma(self):
        """
        Simulates the onset of Trauma.
        Sets Prior Precision to a pathologically high value.
        Reduces integration time step (dt) to model metabolic cost/time dilation.
        """
        self.pi_prior = 10000.0
        # CRITICAL: We reduce dt to prevent numerical explosion due to the stiff gradient.
        # This models the high computational cost of suppressing large errors.
        self.dt = 0.00005 

    def apply_annealing(self, beta):
        """
        Simulates Therapeutic Annealing (Reconsolidation).
        Args:
            beta (float): The annealing factor. Reduces Prior Precision (Pi_prior / beta).
        """
        # 1. De-weight the Prior (Induce Uncertainty)
        self.pi_prior = self.pi_prior_base / beta
        
        # 2. Increase Sensory Gain (Grounding/Mindfulness)
        self.pi_sensory = self.pi_sensory_base * 5.0 
        
        # 3. Relax time step (Metabolic efficiency returns)
        self.dt = 0.01

if __name__ == "__main__":
    # --- SIMULATION CONFIGURATION ---
    # Scenario: Agent believes world is Dangerous (1.0), but World is actually Safe (0.0)
    
    print("--- INITIALIZING AGENT ---")
    # Start with a standard timestep
    agent = ActiveInferenceAgent(prior_mean=1.0, prior_precision_val=10.0, sensory_precision_val=2.0, time_step=0.01)
    
    # 1. TRAUMA STATE
    print("\n--- INDUCING TRAUMA (Pi_Prior -> 10,000) ---")
    agent.induce_trauma()
    
    print("\n--- PHASE 1: EXPOSURE WITHOUT ANNEALING ---")
    # Sensory input is 0.0 (Safety)
    safe_input = 0.0
    for i in range(5):
        agent.observe(safe_input)
        mu = agent.update_belief()
        print(f"Step {i+1}: Obs={safe_input:.1f}, Belief(mu)={mu:.6f} (Stasis/Trauma Locked)")

    # 2. THERAPEUTIC STATE
    print("\n--- PHASE 2: THERAPY (BAYESIAN ANNEALING) ---")
    # Beta=500 divides prior precision by 500 (10000 -> 20)
    agent.apply_annealing(beta=500.0)
    
    for i in range(10):
        agent.observe(safe_input)
        mu = agent.update_belief()
        print(f"Step {i+1}: Obs={safe_input:.1f}, Belief(mu)={mu:.6f} (Updating...)")
        
    print(f"\nFINAL BELIEF STATE: {agent.mu:.6f} (Successfully Updated to Safety)")
