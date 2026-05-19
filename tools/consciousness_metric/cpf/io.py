import numpy as np
import pandas as pd

def load_muse_csv(filepath: str) -> np.ndarray:
    """
    Loads raw EEG data from a standard Muse CSV (e.g., Mind Monitor output).
    Expects columns like 'RAW_TP9' or 'TP9'.
    
    Args:
        filepath: path to the CSV file
        
    Returns:
        2D numpy array of shape (n_channels, n_samples)
    """
    df = pd.read_csv(filepath)
    
    # Common Mind Monitor column names
    raw_cols = ['RAW_TP9', 'RAW_AF7', 'RAW_AF8', 'RAW_TP10']
    
    # Fallback to standard 10-20 names if RAW_ prefix isn't there
    alt_cols = ['TP9', 'AF7', 'AF8', 'TP10']
    
    if all(col in df.columns for col in raw_cols):
        eeg_data = df[raw_cols].values
    elif all(col in df.columns for col in alt_cols):
        eeg_data = df[alt_cols].values
    else:
        # Just grab the first 4 numeric columns that aren't timestamps if we can't find standard names
        numeric_df = df.select_dtypes(include=[np.number])
        # Drop known non-EEG columns
        drop_cols = [c for c in numeric_df.columns if 'Time' in c or 'Battery' in c or 'Gyro' in c or 'Accelerometer' in c or 'HSI' in c]
        numeric_df = numeric_df.drop(columns=drop_cols, errors='ignore')
        
        if numeric_df.shape[1] < 4:
            raise ValueError(f"Could not find 4 EEG channels in CSV. Found columns: {df.columns}")
            
        eeg_data = numeric_df.iloc[:, :4].values
        
    # Shape should be (n_channels, n_samples) for our pipeline
    return eeg_data.T
