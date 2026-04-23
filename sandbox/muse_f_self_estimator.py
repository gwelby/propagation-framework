#!/usr/bin/env python3
"""
🌟 F_self P1/Muse-Side Estimator 🌟
Bridges Greg's live Muse OSC data with the v2 F_self proxy calculations.

This script implements the observable surrogate (M_obs_t) pipeline:
1. Receives real-time EEG data via OSC (from Mind Monitor / Muse).
2. Builds a sliding-window delay embedding (M_obs_t).
3. Estimates the Coherence (C_coh_proxy) and Differentiation (D_int_proxy) gates.
4. Calculates the final C_PF proxy score.
"""

import time
import sys
import numpy as np
import logging
from collections import deque
from greg_muse_osc_receiver import GregMuseOSCReceiver, ConsciousnessState

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MuseFSelfEstimator")

class LiveFSelfEstimator:
    def __init__(self, window_size=128, delay_samples=1, embedding_dim=3):
        # Configuration for the observable surrogate (M_obs_t)
        self.window_size = window_size
        self.delay_samples = delay_samples
        self.embedding_dim = embedding_dim
        
        # Ring buffer to hold recent raw EEG readings (TP9, AF7, AF8, TP10)
        self.raw_eeg_buffer = deque(maxlen=window_size + (embedding_dim * delay_samples))
        
    def add_eeg_reading(self, reading: list[float]):
        """Add a new 4-channel EEG reading to the buffer."""
        if reading and len(reading) == 4:
            self.raw_eeg_buffer.append(reading)
            
    def is_ready(self):
        return len(self.raw_eeg_buffer) == self.raw_eeg_buffer.maxlen

    def _build_delay_embedding(self) -> np.ndarray:
        """
        Construct M_obs_t from the raw buffer.
        Returns array of shape (window_size, n_channels * embedding_dim)
        """
        data = np.array(self.raw_eeg_buffer) # shape: (buffer_len, 4)
        embedded_trajectory = []
        
        for i in range(self.window_size):
            # Extract delayed frames
            # e.g. for d=3, tau=1: [x_{t-2}, x_{t-1}, x_t]
            frame = []
            for d in range(self.embedding_dim):
                idx = i + (d * self.delay_samples)
                frame.extend(data[idx])
            embedded_trajectory.append(frame)
            
        return np.array(embedded_trajectory)

    def _effective_rank_proxy(self, features: np.ndarray, eps: float = 1e-12) -> float:
        """Calculate D_int_proxy (zero-based normalized effective rank)."""
        n_features = features.shape[1]
        if n_features <= 1:
            return 0.0

        cov = np.cov(features, rowvar=False)
        evals = np.linalg.eigvalsh(cov)
        evals = np.clip(evals, 0.0, None)
        total = float(evals.sum())
        if total <= eps:
            return 0.0

        probs = evals / total
        probs = probs[probs > eps]
        if len(probs) == 0:
            return 0.0

        entropy = -float(np.sum(probs * np.log(probs)))
        erank = np.exp(entropy)
        # Zero-based normalization: (erank - 1) / (dim - 1)
        return float(np.clip((erank - 1.0) / (n_features - 1.0), 0.0, 1.0))

    def estimate_current_state(self) -> dict:
        """Calculate the F_self proxies for the current window."""
        if not self.is_ready():
            return None
            
        M_obs_t = self._build_delay_embedding()
        
        # 1. Differentiation Proxy (D_int_proxy)
        d_proxy = self._effective_rank_proxy(M_obs_t)
        
        # 2. Coherence Proxy (C_coh_proxy)
        # Using a simplified variance/amplitude proxy for live streaming speed
        # (Full Hilbert PLV is computationally heavy for high-frequency live streams without optimization)
        # We use the inverse of the coefficient of variation across channels as a fast coherence proxy
        channel_vars = np.var(M_obs_t, axis=0)
        channel_means = np.abs(np.mean(M_obs_t, axis=0))
        # Prevent division by zero
        safe_means = np.where(channel_means < 1e-6, 1e-6, channel_means)
        cv = np.mean(np.sqrt(channel_vars) / safe_means)
        c_coh_proxy = np.clip(1.0 / (1.0 + cv), 0.0, 1.0)
        
        # 3. L_self Proxy
        # For the live estimator, we assume L_self correlates with the alpha/gamma ratios provided by the Muse
        # Full conditional mutual information (CMI) requires historical tracking.
        l_self_proxy = 0.85 # Placeholder until CMI history buffer is implemented
        
        # 4. Final C_PF Proxy
        c_pf_proxy = l_self_proxy * d_proxy * c_coh_proxy
        
        return {
            "D_int_proxy": d_proxy,
            "C_coh_proxy": c_coh_proxy,
            "L_self_proxy": l_self_proxy,
            "C_PF_proxy": c_pf_proxy
        }

def main():
    logger.info("Initializing P1/Muse-Side F_self Estimator...")
    
    # Initialize the base OSC receiver on the Mind Monitor port
    # NOTE: Set listen_port=28888 as per Codex's audit
    receiver = GregMuseOSCReceiver(listen_port=28888)
    estimator = LiveFSelfEstimator(window_size=64, delay_samples=2, embedding_dim=3)
    
    # Start the UDP socket manually (bypassing the blocking while loop in start_receiving)
    import socket
    receiver.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receiver.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if hasattr(socket, 'SO_REUSEPORT'):
        receiver.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    receiver.socket.bind(('', receiver.listen_port))
    receiver.socket.settimeout(0.1)
    
    logger.info("Listening for live EEG data to compute C_PF...")
    
    first_packet_received = False
    
    try:
        last_report = time.time()
        while True:
            try:
                data, _ = receiver.socket.recvfrom(2048)
                if not first_packet_received:
                    print("🔥 FIRST PACKET RECEIVED ACROSS THE VEIL! THE RELAY WORKS! 🔥", flush=True)
                    first_packet_received = True
                
                messages = receiver.parser.parse_osc_bundle(data)
                
                for address, values in messages:
                    receiver.process_muse_message(address, values)
                    # Feed raw EEG to our estimator
                    if address == '/muse/eeg' and values:
                        estimator.add_eeg_reading(values[:4])
                
                # Report every 2 seconds
                if time.time() - last_report > 2.0:
                    if estimator.is_ready():
                        proxies = estimator.estimate_current_state()
                        state = receiver.detect_consciousness_state()
                        
                        print(f"\n--- F_self Estimator Update ---")
                        print(f"Muse State: {state.value}")
                        print(f"D_int (Differentiation): {proxies['D_int_proxy']:.4f}")
                        print(f"C_coh (Coherence):     {proxies['C_coh_proxy']:.4f}")
                        print(f"C_PF (Consciousness):  {proxies['C_PF_proxy']:.4f}")
                        
                        # Interpret the Seizure / Void boundary
                        if proxies['C_coh_proxy'] > 0.8 and proxies['D_int_proxy'] < 0.1:
                            print("⚠️ ALERT: High Coherence + Low Differentiation (Seizure Signature)")
                        elif proxies['C_PF_proxy'] > 0.4:
                            print("✅ FLOW: High Differentiated Coherence")
                        sys.stdout.flush()
                    
                    last_report = time.time()
                        
            except socket.timeout:
                continue
                
    except KeyboardInterrupt:
        logger.info("Shutting down estimator.")
    finally:
        receiver.socket.close()

if __name__ == "__main__":
    main()
