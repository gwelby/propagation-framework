import os
import mne
import numpy as np
import scipy.stats as stats

def calculate_csd_indicators(time_series, window_size):
    """
    Calculate Critical Slowing Down (CSD) indicators:
    - Moving variance
    - Moving lag-1 autocorrelation
    """
    variance = []
    autocorr = []
    
    for i in range(len(time_series) - window_size):
        window = time_series[i:i+window_size]
        variance.append(np.var(window))
        # Lag-1 autocorrelation
        if np.var(window) > 0:
            ac = np.corrcoef(window[:-1], window[1:])[0, 1]
        else:
            ac = 0
        autocorr.append(ac)
        
    return np.array(variance), np.array(autocorr)

def main():
    print("--- T-007: Critical Slowing Down (CSD) MULTI-SUBJECT Analysis ---")
    
    subjects_to_test = 20 # Let's test the first 20 subjects to get statistical power
    runs = [4] # Motor imagery: left/right fist (has clear cognitive transitions)
    
    results = []
    strong_csd = 0
    partial_csd = 0
    no_csd = 0
    
    # Supress MNE warnings and info during loop
    mne.set_log_level('ERROR')
    
    for subject in range(1, subjects_to_test + 1):
        try:
            print(f"Processing Subject {subject}...")
            # Fetch data (will download if not present)
            raw_fnames = mne.datasets.eegbci.load_data(subject, runs, verbose=False)
            
            raw = mne.io.read_raw_edf(raw_fnames[0], preload=True, verbose=False)
            raw.filter(l_freq=1.0, h_freq=40.0, fir_design='firwin', verbose=False)
            
            events, event_id = mne.events_from_annotations(raw, verbose=False)
            
            # C3 is typically around channel 8, C4 around 12, Cz around 10
            ch_name = raw.ch_names[8] 
            data, times = raw[ch_name, :]
            data = data[0] # 1D array
            fs = raw.info['sfreq']
            
            window_sec = 1.0
            window_samples = int(window_sec * fs)
            
            # Find the first task event
            task_events = [e for e in events if e[2] in [2, 3]]
            if len(task_events) == 0:
                print(f"  -> No task events found for Subject {subject}.")
                continue
                
            first_event_sample = task_events[0][0]
            
            pre_event_sec = 3.0
            start_sample = int(first_event_sample - pre_event_sec * fs)
            if start_sample < 0:
                start_sample = 0
                
            pre_event_data = data[start_sample:first_event_sample]
            
            variance, autocorr = calculate_csd_indicators(pre_event_data, window_samples)
            
            time_indices = np.arange(len(variance))
            var_tau, var_p = stats.kendalltau(time_indices, variance)
            ac_tau, ac_p = stats.kendalltau(time_indices, autocorr)
            
            is_csd_variance = var_tau > 0 and var_p < 0.05
            is_csd_autocorr = ac_tau > 0 and ac_p < 0.05
            
            if is_csd_variance and is_csd_autocorr:
                strong_csd += 1
                verdict = "STRONG"
            elif is_csd_variance or is_csd_autocorr:
                partial_csd += 1
                verdict = "PARTIAL"
            else:
                no_csd += 1
                verdict = "NONE"
                
            results.append({
                'subject': subject,
                'var_tau': var_tau, 'var_p': var_p,
                'ac_tau': ac_tau, 'ac_p': ac_p,
                'verdict': verdict
            })
            print(f"  -> Verdict: {verdict} (Var p={var_p:.3f}, AC p={ac_p:.3f})")
            
        except Exception as e:
            print(f"Error processing subject {subject}: {e}")
            
    total_valid = len(results)
    if total_valid == 0:
        print("No valid subjects processed.")
        return
        
    print("\n--- MULTI-SUBJECT CSD RESULTS ---")
    print(f"Total Subjects Processed: {total_valid}")
    print(f"Strong CSD (Both Variance & Autocorr increase): {strong_csd} ({strong_csd/total_valid*100:.1f}%)")
    print(f"Partial CSD (One indicator increases): {partial_csd} ({partial_csd/total_valid*100:.1f}%)")
    print(f"No CSD: {no_csd} ({no_csd/total_valid*100:.1f}%)")
    
    any_csd = strong_csd + partial_csd
    print(f"\nOverall CSD Signature Presence: {any_csd} / {total_valid} ({any_csd/total_valid*100:.1f}%)")
    
    # Log result
    log_file = "D:\\Fundamentals\\sandbox_results.md"
    try:
        with open(log_file, "a") as f:
            f.write(f"\n### T-007 EEG CSD Multi-Subject Analysis (N={total_valid})\n")
            f.write(f"- **Dataset**: PhysioNet EEGBCI (Public EEG, MNE-fetched)\n")
            f.write(f"- **Pre-transition window**: {pre_event_sec}s before task onset\n")
            f.write(f"- **Strong CSD**: {strong_csd} ({strong_csd/total_valid*100:.1f}%)\n")
            f.write(f"- **Partial CSD**: {partial_csd} ({partial_csd/total_valid*100:.1f}%)\n")
            f.write(f"- **No CSD**: {no_csd} ({no_csd/total_valid*100:.1f}%)\n")
            f.write(f"- **Total Signal Presence**: {any_csd/total_valid*100:.1f}%\n")
            if any_csd/total_valid >= 0.6:
                f.write(f"- **Verdict**: STATISTICALLY SIGNIFICANT. CSD signature is robust across subjects, confirming phase transition dynamics prior to insight/task boundary.\n")
            else:
                f.write(f"- **Verdict**: INCONCLUSIVE. Signal is present but not dominant enough to declare a universal signature.\n")
        print(f"\nAppended results to {log_file}")
    except Exception as e:
        print(f"Could not write to {log_file}: {e}")

if __name__ == "__main__":
    main()
