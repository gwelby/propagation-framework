import numpy as np
from sklearn.decomposition import PCA

def compute_pca_entropy(embedded_data: np.ndarray) -> float:
    """
    Computes the Shannon entropy of the normalized PCA eigenvalues.
    This serves as D_int_proxy: a measure of the effective rank 
    or dimensionality of the internal model manifold.
    
    Args:
        embedded_data: 2D array of shape (n_samples, n_features)
                       where n_features is n_channels * embedding_dimension.
                       
    Returns:
        float: Normalized entropy [0, 1]. High score means complex state space.
               Returns 0.0 if variance is zero.
    """
    # Handle edge case: empty or trivial data
    if embedded_data.shape[0] < 2 or embedded_data.shape[1] < 1:
        return 0.0
        
    # Handle zero variance
    if np.all(np.std(embedded_data, axis=0) == 0):
        return 0.0

    # Fit PCA (max components = min(n_samples, n_features))
    pca = PCA()
    pca.fit(embedded_data)
    
    # Get eigenvalues (explained variance)
    eigenvalues = pca.explained_variance_
    
    # Normalize to create a probability distribution (p_i)
    total_variance = np.sum(eigenvalues)
    if total_variance == 0:
        return 0.0
        
    p_i = eigenvalues / total_variance
    
    # Filter out exact zeros to avoid log(0)
    p_i = p_i[p_i > 0]
    
    # Shannon entropy: H = -sum(p_i * log2(p_i))
    entropy = -np.sum(p_i * np.log2(p_i))
    
    # Normalize by theoretical maximum entropy for this rank
    # max entropy occurs when all eigenvalues are equal: log2(N)
    max_rank = min(embedded_data.shape)
    if max_rank <= 1:
        return 0.0
        
    max_entropy = np.log2(max_rank)
    
    normalized_entropy = entropy / max_entropy
    return float(normalized_entropy)