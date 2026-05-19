import numpy as np
from sklearn.linear_model import LinearRegression

def compute_prediction_gain(data: np.ndarray) -> float:
    """
    VAR / Linear Granger prediction gain proxy (D_dir_proxy).
    Estimates how much the prediction of channel X improves when incorporating
    the past of ALL channels vs just the past of channel X.
    
    Args:
        data: 2D array of shape (n_channels, n_samples)
        
    Returns:
        Normalized prediction gain across all channels [0, 1].
    """
    n_channels, n_samples = data.shape
    if n_channels < 2 or n_samples < 3:
        return 0.0
        
    gains = []
    
    # We predict X[t] using data from t-1
    # Y is the target shape (n_samples-1, )
    # X_self is (n_samples-1, 1)
    # X_all is (n_samples-1, n_channels)
    
    for target_ch in range(n_channels):
        Y = data[target_ch, 1:]
        
        # Self history
        X_self = data[target_ch, :-1].reshape(-1, 1)
        
        # All history
        X_all = data[:, :-1].T # shape (n_samples-1, n_channels)
        
        # Fit self-only model
        model_self = LinearRegression().fit(X_self, Y)
        pred_self = model_self.predict(X_self)
        var_self = np.var(Y - pred_self)
        
        # Fit all-channel model
        model_all = LinearRegression().fit(X_all, Y)
        pred_all = model_all.predict(X_all)
        var_all = np.var(Y - pred_all)
        
        if var_self == 0:
            gains.append(0.0)
        else:
            # How much did variance decrease?
            # Gain = (var_self - var_all) / var_self
            # If var_all < var_self, it's > 0. Bounded [0, 1] ideally.
            gain = max(0.0, (var_self - var_all) / var_self)
            gains.append(gain)
            
    return float(np.mean(gains))
