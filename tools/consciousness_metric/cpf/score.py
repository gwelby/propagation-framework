import numpy as np
from cpf.embedding import delay_embed
from cpf.differentiation import compute_pca_entropy
from cpf.coherence import compute_plv, compute_wpli
from cpf.directed import compute_prediction_gain

def compute_cpf_components(data: np.ndarray, tau: int=1, d: int=3) -> dict:
    """
    Calculates all components required by the Phase 0 consciousness metric.
    
    Args:
        data: 2D array (n_channels, n_samples)
        tau: embedding delay
        d: embedding dimension
        
    Returns:
        Dictionary containing D_int, C_coh_plv, C_coh_wpli, D_dir_proxy, 
        and the final composite scores.
    """
    # 1. Differentiation (D_int) via PCA Entropy on Delay Embeddings
    try:
        embedded_data = delay_embed(data, tau=tau, d=d)
        D_int = compute_pca_entropy(embedded_data)
    except ValueError:
        D_int = 0.0
        
    # 2. Coherence (C_coh)
    C_coh_plv = compute_plv(data)
    C_coh_wpli = compute_wpli(data)
    
    # 3. Directed Information / Prediction Gain (D_dir_proxy)
    D_dir_proxy = compute_prediction_gain(data)
    
    # 4. Composite Scores
    C_PF_reduced_plv = D_int * C_coh_plv * D_dir_proxy
    C_PF_reduced_wpli = D_int * C_coh_wpli * D_dir_proxy
    
    return {
        "D_int": float(D_int),
        "C_coh_plv": float(C_coh_plv),
        "C_coh_wpli": float(C_coh_wpli),
        "D_dir_proxy": float(D_dir_proxy),
        "C_PF_reduced_plv": float(C_PF_reduced_plv),
        "C_PF_reduced_wpli": float(C_PF_reduced_wpli)
    }
