import numpy as np

def delay_embed(data: np.ndarray, tau: int, d: int) -> np.ndarray:
    """
    Implements Takens' Theorem for delay embedding.
    
    Args:
        data: 2D array of shape (n_channels, n_samples)
        tau: integer, time delay in samples
        d: integer, embedding dimension
        
    Returns:
        2D array of shape (n_samples - (d-1)*tau, n_channels * d)
    """
    n_channels, n_samples = data.shape
    valid_samples = n_samples - (d - 1) * tau
    
    if valid_samples <= 0:
        raise ValueError("Data too short for given tau and d.")
        
    embedded = []
    # Build embedded state vector at each valid time step
    for i in range(valid_samples):
        state = []
        for ch in range(n_channels):
            # Extract delayed points for this channel
            points = [data[ch, i + k*tau] for k in range(d)]
            state.extend(points)
        embedded.append(state)
        
    return np.array(embedded)
