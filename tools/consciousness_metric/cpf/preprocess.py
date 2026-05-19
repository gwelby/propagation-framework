import numpy as np
from scipy.signal import butter, filtfilt

def bandpass_filter(data: np.ndarray, fs: float, lowcut: float, highcut: float, order: int = 4) -> np.ndarray:
    """
    Applies a zero-phase Butterworth bandpass filter.
    
    Args:
        data: 2D array of shape (n_channels, n_samples)
        fs: Sampling frequency in Hz
        lowcut: Lower cutoff frequency in Hz
        highcut: Upper cutoff frequency in Hz
        order: Filter order
        
    Returns:
        Filtered 2D array of shape (n_channels, n_samples)
    """
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    
    # Apply filter along the sample axis (axis=1)
    filtered_data = filtfilt(b, a, data, axis=1)
    return filtered_data

def reject_artifacts(data: np.ndarray, fs: float, window_sec: float = 2.0, threshold: float = 100.0) -> list:
    """
    Chunks data into epochs and drops any epoch where absolute amplitude exceeds the threshold.
    
    Args:
        data: 2D array of shape (n_channels, n_samples)
        fs: Sampling frequency
        window_sec: Length of each epoch in seconds
        threshold: Maximum allowed absolute amplitude (in uV)
        
    Returns:
        List of clean epochs, where each epoch is a 2D array (n_channels, n_window_samples)
    """
    n_channels, n_samples = data.shape
    window_samples = int(fs * window_sec)
    
    if window_samples > n_samples:
        raise ValueError("Data is shorter than a single window.")
        
    clean_epochs = []
    
    # Non-overlapping windows
    for start in range(0, n_samples - window_samples + 1, window_samples):
        end = start + window_samples
        epoch = data[:, start:end]
        
        # Check artifact threshold
        if np.max(np.abs(epoch)) <= threshold:
            clean_epochs.append(epoch)
            
    return clean_epochs
