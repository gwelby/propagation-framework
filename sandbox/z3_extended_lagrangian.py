import numpy as np

def compute_fisher_information(prob_func, theta, eps=1e-5):
    """Computes the Fisher Information Matrix for a given probability function using finite differences."""
    D = len(theta)
    G = np.zeros((D, D))
    prob = prob_func(theta)
    
    if prob <= 0 or prob >= 1:
        return G
        
    grad = np.zeros(D)
    for i in range(D):
        step = np.zeros(D)
        step[i] = eps
        grad[i] = (prob_func(theta + step) - prob_func(theta - step)) / (2.0 * eps)
        
    # Bernoulli Fisher Information: (grad p * grad p^T) / (p * (1-p))
    G = np.outer(grad, grad) / (prob * (1.0 - prob))
    return G

def z3_lagrangian_experiment():
    print("=======================================================")
    print("  EXPERIMENT 4: Z3 EXTENDED TOY LAGRANGIAN")
    print("  Testing C3-Equivariant Coupling & Fisher Isotropy")
    print("=======================================================\n")

    D = 3 # Spatial dimensions
    theta = np.array([0.5, 0.5, 0.5]) # Arbitrary spatial lock point

    # 1. Define the Z3 Coupling Matrix (Circulant)
    # A circulant matrix commutes with the cyclic shift operator \bar{S}, 
    # perfectly satisfying Axiom 4 / H_C3stat.
    c0, c1, c2 = 0.8, 0.1, 0.1
    M_circulant = np.array([
        [c0, c1, c2],
        [c2, c0, c1],
        [c1, c2, c0]
    ])
    
    print("--- 1. Circulant Coupling Matrix M (C3 Symmetry) ---")
    print(M_circulant)
    print("Notice: Each row is a cyclic shift of the one above it.\n")

    # 2. Define Closure Probabilities
    # The effective spatial field "felt" by channel 'a' is the M-coupled theta.
    beta = 1.0
    def p_channel(a, t):
        # The field specific to channel a
        chi_a = np.dot(M_circulant[a], t)
        # Heat kernel-like Gaussian closure probability
        return np.exp(-beta * chi_a**2)

    # 3. Compute Fisher Information per channel
    G_channels = []
    print("--- 2. Per-Channel Fisher Information G^(a) ---")
    for a in range(3):
        G_a = compute_fisher_information(lambda t: p_channel(a, t), theta)
        evals = np.linalg.eigvalsh(G_a)
        print(f"Channel {a} Eigenvalues: {evals}")
        G_channels.append(G_a)
        
    print("Codex was right: Each individual channel produces a rank-1 Fisher matrix (only one non-zero eigenvalue).\n")

    # 4. Total Fisher Information
    G_total = sum(G_channels)
    print("--- 3. Total Coupled Fisher Information G = Σ G^(a) ---")
    print(G_total)
    
    total_evals = np.linalg.eigvalsh(G_total)
    print(f"\nTotal Eigenvalues: {total_evals}")
    
    # Check if the total G is isotropic (all eigenvalues equal -> G = lambda * I)
    lam_min = np.min(total_evals)
    lam_max = np.max(total_evals)
    
    print(f"Min Eigenvalue: {lam_min:.6f}")
    print(f"Max Eigenvalue: {lam_max:.6f}")
    
    if np.isclose(lam_min, lam_max):
         print("\n[!] SUCCESS: The sum of the circulant-coupled channels creates a perfectly ISOTROPIC Fisher Information Matrix!")
         print("The cross-coupling naturally averages out the rank-1 degeneracy.")
    else:
         print("\n[!] WARNING: The total Fisher matrix is NOT isotropic without further SO(3) rotational averaging.")
         print("The Z3 internal coupling is not enough to guarantee spatial isotropy on its own.")

if __name__ == "__main__":
    z3_lagrangian_experiment()