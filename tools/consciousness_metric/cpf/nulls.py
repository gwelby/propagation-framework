import numpy as np

def generate_white_noise(n_channels: int, n_samples: int, seed: int = None) -> np.ndarray:
    """
    Generates independent white noise across channels.
    Null 1: Expect low PLV, low wPLI, low directed score.
    """
    if seed is not None:
        np.random.seed(seed)
    return np.random.randn(n_channels, n_samples)

def generate_collapsed_synchrony(n_channels: int, n_samples: int, seed: int = None) -> np.ndarray:
    """
    Generates a common-mode signal with slight noise added to each channel.
    Null 2: Expect high PLV, low wPLI, low D_int.
    """
    if seed is not None:
        np.random.seed(seed)
    
    # The "shouting" master signal
    t = np.linspace(0, 10, n_samples)
    master_signal = np.sin(2 * np.pi * 5 * t)  # 5Hz theta/alpha boundary oscillation
    
    # Broadcast to all channels with minimal noise
    data = np.tile(master_signal, (n_channels, 1))
    noise = np.random.randn(n_channels, n_samples) * 0.1
    
    return data + noise

def generate_thermostat(n_samples: int, setpoint: float = 0.0, seed: int = None) -> np.ndarray:
    """
    Generates a simple 1D recurrent controller (temperature reading -> heat on/off).
    Null 5: Expect low D_int (trivial manifold), low composite.
    Returns 4 identical channels of the 1D state to match pipeline shape.
    """
    if seed is not None:
        np.random.seed(seed)
        
    state = np.zeros(n_samples)
    temp = setpoint - 5.0 # Start cold
    
    for i in range(1, n_samples):
        # Heating element logic
        if temp < setpoint:
            heat = 0.5
        else:
            heat = -0.1 # Cooling down
            
        temp = temp + heat + np.random.randn() * 0.05
        state[i] = temp
        
    # Tile it to mimic a 4-channel input so it runs through the same pipeline
    return np.tile(state, (4, 1))