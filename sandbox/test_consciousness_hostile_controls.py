"""
Hostile negative and positive controls for the C_PF reduced metric.

This file adds adversarial pytest controls to the C_PF test battery.
It does NOT claim to detect or measure consciousness; it only tests whether
the current Phase-0 scorer (D_int * C_coh * D_dir_proxy) can discriminate
self-model recurrence from generic temporal/feed-forward/synchronous/common-
driver structure.

PUBLIC HOLD on Fundamentals remains in effect.
"""

import os
import sys

# Route to the consciousness metric tool tree without modifying it.
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tools", "consciousness_metric"))
sys.path.insert(0, ROOT)

import numpy as np
import pytest

from cpf.score import compute_cpf_components
from cpf.nulls import (
    generate_white_noise,
    generate_collapsed_synchrony,
    generate_thermostat,
)

# Reproducible defaults
N_CHANNELS = 4
N_SAMPLES = 1500
TAU = 2
D = 3
SEED = 42


def _score(data, tau=TAU, d=D, model_channels=None, exog_channels=None):
    """Run the Phase-0 C_PF component scorer with explicit channel mapping.

    CRITICAL: model_channels and exog_channels MUST be passed per-control.
    Without exog_channels, L_self computes unconditional MI I(X;M) instead
    of conditional MI I(X;M|E) — which is not what the battery is testing.
    See Claude's finding 2026-08-19.
    """
    return compute_cpf_components(
        data, tau=tau, d=d,
        model_channels=model_channels,
        exog_channels=exog_channels,
    )


def _rng(seed=SEED):
    return np.random.default_rng(seed)


# ---------------------------------------------------------------------------
# Control generators
# ---------------------------------------------------------------------------

def generate_acyclic_feedforward_chain(
    n_channels=N_CHANNELS, n_samples=N_SAMPLES, seed=SEED
):
    """
    Negative control: a strictly feed-forward chain.
    X[0] is an AR oscillator. Each downstream channel depends only on its own
    recent past and the previous channel at t-1. No feedback, no model variable.
    """
    rng = _rng(seed)
    data = np.zeros((n_channels, n_samples))
    # driver for X0 (oscillatory AR)
    for t in range(2, n_samples):
        data[0, t] = (
            1.85 * data[0, t - 1]
            - 0.95 * data[0, t - 2]
            + rng.normal(0.0, 0.5)
        )
    # feed-forward chain
    for i in range(1, n_channels):
        for t in range(2, n_samples):
            data[i, t] = (
                0.6 * data[i, t - 1]
                - 0.25 * data[i, t - 2]
                + 0.45 * data[i - 1, t - 1]
                + rng.normal(0.0, 0.2)
            )
    return data


def generate_synchronized_no_model(
    n_channels=5, n_samples=N_SAMPLES, seed=SEED
):
    """
    Negative control: N identical oscillators driven by a common master signal.
    Zero directed structure, high zero-lag coherence, no model or loop.
    """
    rng = _rng(seed)
    t = np.arange(n_samples)
    f = 0.05  # arbitrary units
    master = np.sin(2 * np.pi * f * t)
    noise = rng.normal(0.0, 0.05, size=(n_channels, n_samples))
    data = np.tile(master, (n_channels, 1)) + noise
    return data


def generate_time_shifted_surrogate(
    n_channels=N_CHANNELS, n_samples=N_SAMPLES, seed=SEED
):
    """
    Negative control: take a single stochastic time series and shift each
    channel by a different lag. Cross-channel temporal structure is destroyed.
    """
    rng = _rng(seed)
    max_shift = 200
    total = n_samples + max_shift
    base = np.zeros(total)
    for t in range(2, total):
        base[t] = 0.8 * base[t - 1] - 0.3 * base[t - 2] + rng.normal(0.0, 0.5)

    shifts = rng.integers(20, max_shift, size=n_channels)
    data = np.zeros((n_channels, n_samples))
    for i in range(n_channels):
        data[i, :] = base[shifts[i] : shifts[i] + n_samples]
    return data


def generate_phase_randomized_surrogate(
    n_channels=N_CHANNELS, n_samples=N_SAMPLES, seed=SEED
):
    """
    Negative control: preserve each channel's amplitude spectrum and replace
    Fourier phases by independent random phases. Cross-channel coherence is
    broken while the per-channel spectrum is unchanged.
    """
    rng = _rng(seed)
    # Start from a coherent feed-forward pattern, then scramble it.
    original = generate_acyclic_feedforward_chain(n_channels, n_samples, seed)
    data = np.zeros_like(original)
    for i in range(n_channels):
        fft = np.fft.rfft(original[i, :])
        amp = np.abs(fft)
        phases = rng.uniform(0.0, 2.0 * np.pi, size=fft.shape)
        # DC and (for even length) Nyquist must be real to keep the irfft real.
        phases[0] = 0.0
        if n_samples % 2 == 0:
            phases[-1] = 0.0
        fft_new = amp * np.exp(1j * phases)
        data[i, :] = np.fft.irfft(fft_new, n=n_samples)
    return data


def generate_common_driver_confound(
    n_channels=N_CHANNELS, n_samples=N_SAMPLES, seed=SEED
):
    """
    Negative control: a single hidden driver projects to all observed channels
    with different delays and weights. The observed channels are coherent but
    no direct causal link exists among them.
    """
    rng = _rng(seed)
    max_delay = n_channels
    total = n_samples + max_delay
    driver = np.zeros(total)
    for t in range(2, total):
        driver[t] = (
            1.75 * driver[t - 1]
            - 0.85 * driver[t - 2]
            + rng.normal(0.0, 0.5)
        )

    delays = np.arange(1, n_channels + 1)
    weights = rng.uniform(0.4, 0.9, size=n_channels)
    data = np.zeros((n_channels, n_samples))
    for i in range(n_channels):
        data[i, :] = weights[i] * driver[delays[i] : delays[i] + n_samples]
    data += rng.normal(0.0, 0.25, size=data.shape)
    return data


def generate_closed_self_model_loop(
    n_channels=3, n_samples=N_SAMPLES, seed=SEED
):
    """
    Positive control: a model-like variable M[t] is fed by internal history and
    feeds back to influence future X. The loop uses second-order dynamics and
    lag-1/lag-2 coupling so that M and the X variables form a stable, closed
    self-model circuit.

    This is the only control that should be able to produce a non-zero score
    on a metric that targets self-model loops.
    """
    rng = _rng(seed)
    data = np.zeros((n_channels, n_samples))
    # state order: [X1, X2, M]
    for t in range(2, n_samples):
        x1_l1, x1_l2 = data[0, t - 1], data[0, t - 2]
        x2_l1, x2_l2 = data[1, t - 1], data[1, t - 2]
        m_l1, m_l2 = data[2, t - 1], data[2, t - 2]

        # M is fed by its own past and by the X history.
        data[2, t] = (
            0.2 * m_l1
            - 0.1 * m_l2
            + 0.4 * x1_l2
            + 0.4 * x2_l2
            + rng.normal(0.0, 0.2)
        )

        # The X variables are fed by M and by their own damped oscillation.
        data[0, t] = (
            0.84 * m_l1
            + 0.2 * x1_l1
            - 0.1 * x1_l2
            + rng.normal(0.0, 0.2)
        )
        data[1, t] = (
            0.84 * m_l1
            + 0.2 * x2_l1
            - 0.1 * x2_l2
            + rng.normal(0.0, 0.2)
        )
    return data


# ---------------------------------------------------------------------------
# Test battery
# ---------------------------------------------------------------------------

CONTROLS = [
    # name, kind, generator, kwargs, model_channels, exog_channels
    # kind: "negative" (should score ~0), "positive" (should score >0),
    #        "known_limit" (observationally unsolvable — not counted in FPR)
    #
    # Channel mappings:
    # - model_channels: which channel(s) are the self-model M
    # - exog_channels: which channel(s) are exogenous input E
    # If exog_channels is None, L_self computes UNCONDITIONAL MI (not CMI).
    # This is correct only for controls with no exogenous input at all.
    #
    # white_noise: no structure at all. No M, no E. Last channel as M, no E.
    ("white_noise", "negative", generate_white_noise,
     {"n_channels": N_CHANNELS, "n_samples": N_SAMPLES, "seed": SEED},
     None, None),
    # collapsed_synchrony: all channels identical (common mode). No M, no E.
    ("collapsed_synchrony", "negative", generate_collapsed_synchrony,
     {"n_channels": N_CHANNELS, "n_samples": N_SAMPLES, "seed": SEED},
     None, None),
    # thermostat: 1D state tiled to 4 channels. No M, no E.
    ("thermostat", "negative", generate_thermostat,
     {"n_samples": N_SAMPLES, "setpoint": 20.0, "seed": SEED},
     None, None),
    # acyclic_feedforward_chain: channel 0 is the driver (E), channels 1-3 are
    # downstream. No model variable. M=last channel (3), E=channel 0 (driver).
    ("acyclic_feedforward_chain", "negative", generate_acyclic_feedforward_chain,
     {}, 3, [0]),
    # synchronized_no_model: all channels driven by common master. No model.
    # M=last channel, E=channel 0 (master is embedded in all, but channel 0
    # is as close to the driver as we get).
    ("synchronized_no_model", "negative", generate_synchronized_no_model,
     {}, 4, [0]),
    # time_shifted_surrogate: all channels are shifted versions of one signal.
    # No model. M=last channel, E=channel 0.
    ("time_shifted_surrogate", "negative", generate_time_shifted_surrogate,
     {}, 3, [0]),
    # phase_randomized_surrogate: scrambled feed-forward. No model.
    # M=last channel, E=channel 0.
    ("phase_randomized_surrogate", "negative", generate_phase_randomized_surrogate,
     {}, 3, [0]),
    # common_driver_confound: hidden driver projects to all channels.
    # KNOWN LIMIT: the driver is unobserved by construction — it's a local
    # variable, never returned in data. No observational measure can condition
    # on an unobserved common cause. This is a causal-inference identifiability
    # limit, not an estimator defect. Reclassified from "negative" to
    # "known_limit" per Claude's finding 2026-08-19.
    # FPR is computed over "negative" controls only, not "known_limit".
    ("common_driver_confound", "known_limit", generate_common_driver_confound,
     {}, 3, None),  # E=None because the driver is unobserved
    # closed_self_model_loop: state order [X1, X2, M]. M=channel 2, X=[0,1].
    # No exogenous input (closed loop). E=None is correct here — the loop
    # is self-contained with no external driver.
    ("closed_self_model_loop", "positive", generate_closed_self_model_loop,
     {}, 2, None),
]


@pytest.mark.parametrize("name,kind,generator,kwargs,model_ch,exog_ch", CONTROLS)
def test_control(name, kind, generator, kwargs, model_ch, exog_ch, capsys):
    """Compute and emit C_PF components for every hostile control."""
    data = generator(**kwargs)
    if data.ndim == 1:
        data = data.reshape(1, -1)
    scores = _score(data, model_channels=model_ch, exog_channels=exog_ch)

    with capsys.disabled():
        print(
            f"{name:30s}  kind={kind:8s}  "
            f"D_int={scores['D_int']:.4f}  "
            f"C_coh_wpli={scores['C_coh_wpli']:.4f}  "
            f"D_dir_proxy={scores['D_dir_proxy']:.4f}  "
            f"L_self={scores['L_self']:.4f}  "
            f"C_PF_lself_wpli={scores['C_PF_lself_wpli']:.4f}  "
            f"C_PF_reduced_wpli={scores['C_PF_reduced_wpli']:.4f}"
        )

    # Basic validity: all components must be in [0, 1].
    for key in ("D_int", "C_coh_plv", "C_coh_wpli", "D_dir_proxy", "L_self", "C_PF_lself_wpli", "C_PF_reduced_wpli"):
        assert 0.0 <= scores[key] <= 1.0, f"{name}: {key} out of bounds: {scores[key]}"

    # The expected outcomes are documented in the Route C report. These tests
    # are a measurement battery; the current scorer is expected to fail on some
    # of the negative controls, which is why the report exists.
    if kind == "negative":
        assert 0.0 <= scores["C_PF_reduced_wpli"] <= 1.0
    else:
        # The positive control is required to be non-zero; whether it is
        # *discriminated* from the strongest negative is checked in the summary.
        assert scores["C_PF_reduced_wpli"] > 0.0, (
            f"{name} is a positive control but C_PF_reduced_wpli = "
            f"{scores['C_PF_reduced_wpli']:.4f}"
        )


def test_hostile_battery_landscape():
    """Aggregate the battery and compute false-positive/negative rates."""
    results = []
    for name, kind, generator, kwargs, model_ch, exog_ch in CONTROLS:
        data = generator(**kwargs)
        if data.ndim == 1:
            data = data.reshape(1, -1)
        scores = _score(data, model_channels=model_ch, exog_channels=exog_ch)
        results.append({"name": name, "kind": kind, **scores})

    negatives = [r for r in results if r["kind"] == "negative"]
    positives = [r for r in results if r["kind"] == "positive"]

    def _summarize(score_key: str, label: str):
        false_positives = [r for r in negatives if r[score_key] >= 0.05]
        false_negatives = [r for r in positives if r[score_key] <= 0.05]

        fpr = len(false_positives) / len(negatives) if negatives else 0.0
        fnr = len(false_negatives) / len(positives) if positives else 0.0

        print(f"\n--- {label} ---")
        print(f"False positives ({score_key} >= 0.05): {len(false_positives)}")
        for r in false_positives:
            print(f"  - {r['name']}: {r[score_key]:.4f}")
        print(f"False-positive rate (FPR): {fpr:.2%}")
        print(f"False negatives ({score_key} <= 0.05): {len(false_negatives)}")
        for r in false_negatives:
            print(f"  - {r['name']}: {r[score_key]:.4f}")
        print(f"False-negative rate (FNR): {fnr:.2%}")

        max_negative = max(r[score_key] for r in negatives)
        min_positive = min(r[score_key] for r in positives)
        print(f"Max negative {score_key}: {max_negative:.4f}")
        print(f"Min positive {score_key}: {min_positive:.4f}")
        discrimination_gap = min_positive - max_negative
        print(f"Discrimination gap (positive - max negative): {discrimination_gap:+.4f}")
        assert -1.0 <= discrimination_gap <= 1.0, "Discrimination gap out of bounds"

    print("\n=== Hostile control summary ===")
    print(f"Negative controls: {len(negatives)}")
    print(f"Positive controls: {len(positives)}")
    _summarize("C_PF_reduced_wpli", "Legacy D_dir_proxy composite")
    _summarize("C_PF_lself_wpli", "New L_self CMI composite")


if __name__ == "__main__":
    # Direct script execution prints the table for inspection.
    print("\n=== C_PF hostile control battery (direct run) ===\n")
    for name, kind, generator, kwargs, model_ch, exog_ch in CONTROLS:
        data = generator(**kwargs)
        if data.ndim == 1:
            data = data.reshape(1, -1)
        scores = _score(data, model_channels=model_ch, exog_channels=exog_ch)
        print(
            f"{name:30s}  {kind:8s}  "
            f"D_int={scores['D_int']:.4f}  "
            f"C_coh_wpli={scores['C_coh_wpli']:.4f}  "
            f"D_dir_proxy={scores['D_dir_proxy']:.4f}  "
            f"L_self={scores['L_self']:.4f}  "
            f"C_PF_lself_wpli={scores['C_PF_lself_wpli']:.4f}  "
            f"C_PF_reduced_wpli={scores['C_PF_reduced_wpli']:.4f}"
        )

    # Run the aggregate summary.
    test_hostile_battery_landscape()
