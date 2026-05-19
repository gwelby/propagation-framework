import pytest
import numpy as np
import sys
import os

# Add parent directory to path to allow absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from cpf.nulls import generate_white_noise, generate_collapsed_synchrony, generate_thermostat
from cpf.score import compute_cpf_components

def test_white_noise_null():
    """Null 1: White noise should have near-zero coherence and directed score."""
    data = generate_white_noise(n_channels=4, n_samples=1000, seed=42)
    scores = compute_cpf_components(data, tau=2, d=3)
    
    assert scores["C_coh_plv"] < 0.1, f"PLV too high: {scores['C_coh_plv']}"
    assert scores["C_coh_wpli"] < 0.1, f"wPLI too high: {scores['C_coh_wpli']}"
    assert scores["D_dir_proxy"] < 0.1, f"Directed score too high: {scores['D_dir_proxy']}"
    
    assert scores["C_PF_reduced_wpli"] < 0.05, "Composite score failed Null 1"

def test_collapsed_synchrony_null():
    """Null 2: Collapsed synchrony should have high PLV, but ZERO wPLI and low D_int."""
    data = generate_collapsed_synchrony(n_channels=4, n_samples=1000, seed=42)
    scores = compute_cpf_components(data, tau=2, d=3)
    
    # Common mode signal -> high PLV
    assert scores["C_coh_plv"] > 0.8, f"PLV should be high: {scores['C_coh_plv']}"
    # Common mode signal -> zero phase lag -> low wPLI
    assert scores["C_coh_wpli"] < 0.1, f"wPLI must penalize zero-lag: {scores['C_coh_wpli']}"
    
    # Differentiation should be relatively low compared to full rank noise
    assert scores["D_int"] < 0.5, f"D_int should be lower for collapsed state: {scores['D_int']}"
    
    assert scores["C_PF_reduced_wpli"] < 0.05, "Composite score failed Null 2"

def test_thermostat_null():
    """Null 5: 1D Thermostat should have zero D_int (trivial manifold)."""
    data = generate_thermostat(n_samples=1000, setpoint=20.0, seed=42)
    scores = compute_cpf_components(data, tau=2, d=3)
    
    # The thermostat is a strict 1D process duplicated 4 times.
    # The PCA entropy of its embedding should be 0 because it has rank 1 effectively.
    assert scores["D_int"] < 0.25, f"Thermostat D_int must be low: {scores['D_int']}"
    
    assert scores["C_PF_reduced_wpli"] < 0.05, "Composite score failed Null 5"
