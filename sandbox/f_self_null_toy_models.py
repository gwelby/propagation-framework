"""
Toy checks for the F_self v2 lane.

Purpose:
  - Show that breaking either loop leg drives the estimated loop gate to ~0
  - Provide named toy classes aligned with the theorem notes
  - Provide a positive-control recurrent model where both loop legs are > 0
  - Add first differentiation and coherence proxies
  - Compare PLV against a lag-aware proxy (wPLI)
  - Report bounded C_PF proxy panels instead of a single hidden coherence choice

Important honesty boundary:
  This harness still uses the abstract toy model variable `m_t` plus an
  observable channel-stack proxy. It is not yet the full delay-embedded
  `M_obs_t` estimator from the derivation notes.

This is not a proof. It is a sanity-check harness for:
  derivations/consciousness_f_self_null_theorem_target_2026-04-15.md
  derivations/consciousness_f_self_null_class_exogenous_only_2026-04-16.md
  derivations/consciousness_f_self_null_class_passive_tracker_2026-04-16.md
  derivations/consciousness_f_self_mt_operationalization_audit_2026-04-16.md
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy.signal import hilbert


def _ols_residual_var(y: np.ndarray, X: np.ndarray) -> float:
    y = np.asarray(y, dtype=float).reshape(-1, 1)
    if X.size == 0:
        resid = y - y.mean()
        return float(((resid.T @ resid) / len(y)).item())

    X = np.asarray(X, dtype=float)
    X = np.column_stack([np.ones(len(X)), X])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    return float(((resid.T @ resid) / len(y)).item())


def gaussian_cmi_scalar(target: np.ndarray, source: np.ndarray, cond: np.ndarray) -> float:
    """
    Estimate I(target ; source | cond) for a linear-Gaussian toy model using
    regression residual variances:
      0.5 * log Var(target | cond) / Var(target | source, cond)
    """
    target = np.asarray(target, dtype=float)
    source = np.asarray(source, dtype=float).reshape(-1, 1)
    cond = np.asarray(cond, dtype=float)
    if cond.ndim == 1:
        cond = cond.reshape(-1, 1)

    var_without = _ols_residual_var(target, cond)
    var_with = _ols_residual_var(target, np.column_stack([source, cond]))
    ratio = max(var_without / max(var_with, 1e-12), 1.0)
    return 0.5 * math.log(ratio)


def effective_rank_from_cov(features: np.ndarray, eps: float = 1e-12) -> float:
    """
    Cheap differentiation proxy in [0, 1] based on the effective rank of the
    feature covariance.

    Important calibration:
      erank itself lives in [1, n_features]. A pure rank-1 collapse should map
      to 0, not 1/n_features. So the proxy uses the zero-based normalization

        (erank - 1) / (n_features - 1)

      instead of erank / n_features.
    """
    features = np.asarray(features, dtype=float)
    if features.ndim == 1:
        features = features.reshape(-1, 1)

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
    erank = math.exp(entropy)
    return float(np.clip((erank - 1.0) / (n_features - 1.0), 0.0, 1.0))


def plv_coherence(phase_a: np.ndarray, phase_b: np.ndarray) -> float:
    phase_a = np.asarray(phase_a, dtype=float)
    phase_b = np.asarray(phase_b, dtype=float)
    if phase_a.shape != phase_b.shape:
        raise ValueError('phase_a and phase_b must have the same shape')

    delta = phase_a - phase_b
    return float(np.abs(np.mean(np.exp(1j * delta))))


def hilbert_plv(data: np.ndarray, pair_idx: tuple[int, int]) -> float:
    data = np.asarray(data, dtype=float)
    if data.ndim == 1:
        data = data.reshape(-1, 1)

    analytic_i = hilbert(data[:, pair_idx[0]])
    analytic_j = hilbert(data[:, pair_idx[1]])
    phase_i = np.angle(analytic_i)
    phase_j = np.angle(analytic_j)
    return plv_coherence(phase_i, phase_j)


def wpli_pair(data: np.ndarray, pair_idx: tuple[int, int], eps: float = 1e-12) -> float:
    data = np.asarray(data, dtype=float)
    if data.ndim == 1:
        data = data.reshape(-1, 1)

    analytic_i = hilbert(data[:, pair_idx[0]])
    analytic_j = hilbert(data[:, pair_idx[1]])
    cross_spec = analytic_i * np.conj(analytic_j)
    imag = np.imag(cross_spec)

    num = np.abs(np.mean(np.abs(imag) * np.sign(imag)))
    den = np.mean(np.abs(imag))
    return float(num / max(den, eps))


def coherence_proxy_panel_from_channels(data: np.ndarray) -> tuple[float, float]:
    """
    Return a two-proxy coherence panel:
      - mean PLV across channel pairs
      - mean wPLI across channel pairs

    Codex read:
      PLV is the broad synchrony proxy.
      wPLI is the lag-aware hostile comparison that suppresses zero-lag collapse.
    """
    data = np.asarray(data, dtype=float)
    if data.ndim == 1 or data.shape[1] == 1:
        return 1.0, 1.0

    pairs = [(i, j) for i in range(data.shape[1]) for j in range(i + 1, data.shape[1])]
    plvs = [hilbert_plv(data, pair) for pair in pairs]
    wplis = [wpli_pair(data, pair) for pair in pairs]
    return float(np.mean(plvs)), float(np.mean(wplis))


@dataclass
class ToyResult:
    name: str
    rin: float
    rout: float
    l_self: float
    d_proxy: float
    c_coh_plv_proxy: float
    c_coh_wpli_proxy: float
    c_pf_plv_proxy: float
    c_pf_wpli_proxy: float


def simulate_model(kind: str, n: int = 50000, seed: int = 7) -> ToyResult:
    rng = np.random.default_rng(seed)

    e = rng.normal(size=n)
    x_prev = rng.normal(size=n)
    x_t = 0.7 * x_prev + 0.4 * e + 0.3 * rng.normal(size=n)

    if kind in {'no_inbound', 'exogenous_only_controller'}:
        m_t = 0.9 * e + 0.3 * rng.normal(size=n)
        x_next = 0.6 * x_t + 0.5 * m_t + 0.2 * e + 0.3 * rng.normal(size=n)
    elif kind in {'no_outbound', 'passive_state_tracker'}:
        m_t = 0.7 * x_prev + 0.4 * e + 0.3 * rng.normal(size=n)
        x_next = 0.8 * x_t + 0.2 * e + 0.3 * rng.normal(size=n)
    elif kind == 'positive_loop':
        m_t = 0.7 * x_prev + 0.4 * e + 0.3 * rng.normal(size=n)
        x_next = 0.55 * x_t + 0.55 * m_t + 0.2 * e + 0.3 * rng.normal(size=n)
    elif kind == 'collapsed_sync':
        # Strongly collapsed recurrent loop: both legs exist, but almost every
        # variable rides the same latent mode, so differentiation should drop.
        z = rng.normal(size=n)
        x_prev = z + 0.02 * rng.normal(size=n)
        x_t = 0.98 * x_prev + 0.02 * e + 0.02 * rng.normal(size=n)
        m_t = 0.99 * x_t + 0.02 * rng.normal(size=n)
        x_next = 0.99 * m_t + 0.01 * x_t + 0.02 * e + 0.02 * rng.normal(size=n)
    elif kind == 'lagged_loop':
        # Genuine lagged coupling toy: weaker raw PLV, stronger lag-aware coupling.
        base = rng.normal(size=n)
        x_prev = 0.8 * np.roll(base, 3) + 0.2 * base + 0.1 * rng.normal(size=n)
        x_t = 0.8 * np.roll(x_prev, 2) + 0.15 * e + 0.1 * rng.normal(size=n)
        m_t = 0.75 * np.roll(x_t, 2) + 0.1 * np.roll(x_prev, 1) + 0.1 * rng.normal(size=n)
        x_next = 0.7 * np.roll(m_t, 2) + 0.2 * x_t + 0.1 * rng.normal(size=n)
    else:
        raise ValueError(f'Unknown model kind: {kind}')

    rin = gaussian_cmi_scalar(target=m_t, source=x_prev, cond=e)
    rout = gaussian_cmi_scalar(target=x_next, source=m_t, cond=np.column_stack([x_t, e]))

    nrin = 1.0 - math.exp(-rin)
    nrout = 1.0 - math.exp(-rout)
    l_self = min(nrin, nrout)

    observable_channels = np.column_stack([x_prev, x_t, m_t, x_next])
    d_proxy = effective_rank_from_cov(observable_channels)
    c_coh_plv_proxy, c_coh_wpli_proxy = coherence_proxy_panel_from_channels(observable_channels)
    c_pf_plv_proxy = l_self * d_proxy * c_coh_plv_proxy
    c_pf_wpli_proxy = l_self * d_proxy * c_coh_wpli_proxy

    return ToyResult(
        kind,
        rin,
        rout,
        l_self,
        d_proxy,
        c_coh_plv_proxy,
        c_coh_wpli_proxy,
        c_pf_plv_proxy,
        c_pf_wpli_proxy,
    )


def main() -> None:
    models = [
        'exogenous_only_controller',
        'passive_state_tracker',
        'positive_loop',
        'collapsed_sync',
        'lagged_loop',
    ]
    results = [simulate_model(name) for name in models]

    print('F_self v2 toy checks (proxy panel)')
    print('=' * 148)
    print(
        f"{'model':<22} {'R_in':>10} {'R_out':>10} {'L_self':>10} {'D_proxy':>10} "
        f"{'PLV':>10} {'wPLI':>10} {'C_PF_PLV':>12} {'C_PF_wPLI':>12}"
    )
    print('-' * 148)
    for r in results:
        print(
            f"{r.name:<22} {r.rin:10.6f} {r.rout:10.6f} {r.l_self:10.6f} {r.d_proxy:10.6f} "
            f"{r.c_coh_plv_proxy:10.6f} {r.c_coh_wpli_proxy:10.6f} "
            f"{r.c_pf_plv_proxy:12.6f} {r.c_pf_wpli_proxy:12.6f}"
        )

    print('\nExpected pattern:')
    print('- exogenous_only_controller -> both C_PF panels ~ 0 because loop gate is broken')
    print('- passive_state_tracker     -> both C_PF panels ~ 0 because loop gate is broken')
    print('- positive_loop            -> PLV panel high, wPLI panel low if coherence is mostly zero-lag')
    print('- collapsed_sync           -> PLV very high but wPLI near zero; this is the hostile comparison')
    print('- lagged_loop              -> wPLI should rise relative to PLV when lagged coupling is real')


if __name__ == '__main__':
    main()
