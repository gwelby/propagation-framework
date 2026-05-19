import argparse
import numpy as np
import sys
import os

from cpf.io import load_muse_csv
from cpf.preprocess import bandpass_filter, reject_artifacts
from cpf.score import compute_cpf_components

def main():
    parser = argparse.ArgumentParser(description="Compute Phase 0 C_PF_reduced_proxy for Muse EEG data.")
    parser.add_argument("csv_path", type=str, help="Path to the Muse CSV file.")
    parser.add_argument("--fs", type=float, default=256.0, help="Sampling frequency (default: 256 Hz)")
    parser.add_argument("--lowcut", type=float, default=1.0, help="Bandpass lowcut (default: 1.0 Hz)")
    parser.add_argument("--highcut", type=float, default=45.0, help="Bandpass highcut (default: 45.0 Hz)")
    parser.add_argument("--epoch_sec", type=float, default=2.0, help="Epoch length in seconds (default: 2.0s)")
    parser.add_argument("--threshold", type=float, default=100.0, help="Artifact rejection threshold in uV (default: 100.0 uV)")
    parser.add_argument("--tau", type=int, default=2, help="Embedding delay (default: 2)")
    parser.add_argument("--dim", type=int, default=3, help="Embedding dimension (default: 3)")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.csv_path):
        print(f"Error: File '{args.csv_path}' not found.")
        sys.exit(1)
        
    print(f"Loading {args.csv_path}...")
    try:
        raw_data = load_muse_csv(args.csv_path)
    except Exception as e:
        print(f"Error loading CSV: {e}")
        sys.exit(1)
        
    print(f"Loaded data shape: {raw_data.shape} (Channels x Samples)")
    
    # Preprocessing
    print(f"Applying bandpass filter: {args.lowcut}-{args.highcut} Hz...")
    filtered_data = bandpass_filter(raw_data, fs=args.fs, lowcut=args.lowcut, highcut=args.highcut)
    
    print(f"Epoching ({args.epoch_sec}s) and rejecting artifacts (> {args.threshold} uV)...")
    clean_epochs = reject_artifacts(filtered_data, fs=args.fs, window_sec=args.epoch_sec, threshold=args.threshold)
    
    if len(clean_epochs) == 0:
        print("Error: All epochs rejected due to artifacts. Data is too noisy.")
        sys.exit(1)
        
    print(f"Kept {len(clean_epochs)} clean epochs.")
    
    # Compute scores for each epoch
    print("Computing C_PF_reduced_proxy components...")
    all_scores = {
        "D_int": [], "C_coh_plv": [], "C_coh_wpli": [], 
        "D_dir_proxy": [], "C_PF_reduced_plv": [], "C_PF_reduced_wpli": []
    }
    
    for idx, epoch in enumerate(clean_epochs):
        try:
            scores = compute_cpf_components(epoch, tau=args.tau, d=args.dim)
            for k, v in scores.items():
                all_scores[k].append(v)
        except Exception as e:
            print(f"Warning: Failed to compute scores for epoch {idx}. Reason: {e}")
            continue
            
    if len(all_scores["C_PF_reduced_wpli"]) == 0:
        print("Error: Could not compute scores for any epoch.")
        sys.exit(1)
        
    # Aggregate and print
    print("\n--- FINAL AVERAGE SCORES ---")
    for k, v in all_scores.items():
        mean_val = np.mean(v)
        std_val = np.std(v)
        print(f"{k:>18}: {mean_val:.4f}  (± {std_val:.4f})")
        
if __name__ == "__main__":
    main()
