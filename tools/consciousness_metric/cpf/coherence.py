import numpy as np
from scipy.signal import hilbert

def compute_plv(data: np.ndarray) -> float:
    """
    Computes Phase Locking Value (PLV) across all unique pairs of channels.
    
    Args:
        data: 2D array of shape (n_channels, n_samples)
        
    Returns:
        Mean PLV across all pairs [0, 1].
    """
    n_channels, _ = data.shape
    if n_channels < 2:
        return 0.0
        
    # Extract instantaneous phase via Hilbert transform
    analytic_signal = hilbert(data, axis=1)
    phase = np.angle(analytic_signal)
    
    plvs = []
    for i in range(n_channels):
        for j in range(i + 1, n_channels):
            phase_diff = phase[i] - phase[j]
            # PLV = |<exp(i * delta_phi)>|
            plv = np.abs(np.mean(np.exp(1j * phase_diff)))
            plvs.append(plv)
            
    return float(np.mean(plvs))

def compute_wpli(data: np.ndarray) -> float:
    """
    Computes Weighted Phase Lag Index (wPLI) across all unique pairs of channels.
    wPLI penalizes zero/pi phase lag (often caused by volume conduction).
    
    Args:
        data: 2D array of shape (n_channels, n_samples)
        
    Returns:
        Mean wPLI across all pairs [0, 1].
    """
    n_channels, _ = data.shape
    if n_channels < 2:
        return 0.0
        
    analytic_signal = hilbert(data, axis=1)
    
    wplis = []
    for i in range(n_channels):
        for j in range(i + 1, n_channels):
            # Cross-spectral density proxy (using analytic signal product)
            # True CSD involves tapering/epochs, but for continuous proxy we use instantaneous:
            cross_spec = analytic_signal[i] * np.conj(analytic_signal[j])
            imag_cross = np.imag(cross_spec)
            
            # wPLI = |<Im(X)>| / <|Im(X)|>
            num = np.abs(np.mean(imag_cross))
            den = np.mean(np.abs(imag_cross))
            
            wpli = num / den if den > 0 else 0.0
            wplis.append(wpli)
            
    return float(np.mean(wplis))
