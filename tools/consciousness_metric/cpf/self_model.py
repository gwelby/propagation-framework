import numpy as np
from sklearn.covariance import LedoitWolf


def _fit_joint_cov(joint: np.ndarray) -> np.ndarray:
    """Single Ledoit-Wolf covariance for the full joint vector."""
    return LedoitWolf().fit(joint).covariance_


def _ensure_pd_logdet(cov: np.ndarray) -> float:
    """Return logdet, adding a small ridge if the matrix is singular/indefinite."""
    sign, logdet = np.linalg.slogdet(cov)
    if sign > 0 and np.isfinite(logdet):
        return float(logdet)
    n = cov.shape[0]
    scale = np.trace(cov) / max(n, 1)
    for ridge in (1e-10, 1e-8, 1e-6, 1e-4):
        cov_r = cov + ridge * scale * np.eye(n)
        sign, logdet = np.linalg.slogdet(cov_r)
        if sign > 0 and np.isfinite(logdet):
            return float(logdet)
    return 0.0


def _sub_cov(cov: np.ndarray, *groups: list[int]) -> np.ndarray:
    """Extract sub-covariance for the given groups of variable indices."""
    idx = []
    for g in groups:
        idx.extend(list(g))
    return cov[np.ix_(idx, idx)]


def _gaussian_cmi_from_cov(
    cov: np.ndarray,
    a_idx: list[int],
    b_idx: list[int],
    c_idx: list[int] | None = None,
) -> float:
    """
    I(A;B|C) for jointly Gaussian (A,B,C) from a single covariance matrix.
    Uses the entropy identity:
        I(A;B|C) = 0.5 * log( det(Σ_AC) * det(Σ_BC) / (det(Σ_C) * det(Σ_ABC)) )
    """
    c_idx = list(c_idx) if c_idx else []

    if not c_idx:
        log_a = _ensure_pd_logdet(_sub_cov(cov, a_idx))
        log_b = _ensure_pd_logdet(_sub_cov(cov, b_idx))
        log_ab = _ensure_pd_logdet(_sub_cov(cov, a_idx, b_idx))
        mi = 0.5 * (log_a + log_b - log_ab)
    else:
        log_ac = _ensure_pd_logdet(_sub_cov(cov, a_idx, c_idx))
        log_bc = _ensure_pd_logdet(_sub_cov(cov, b_idx, c_idx))
        log_c = _ensure_pd_logdet(_sub_cov(cov, c_idx))
        log_abc = _ensure_pd_logdet(_sub_cov(cov, a_idx, b_idx, c_idx))
        mi = 0.5 * (log_ac + log_bc - log_c - log_abc)

    return float(max(0.0, mi))


def _normalize_cmi(cmi_nats: float) -> float:
    """Monotonic [0,1) map: R_norm = 1 - exp(-R_nats)."""
    if not np.isfinite(cmi_nats) or cmi_nats <= 0:
        return 0.0
    return float(1.0 - np.exp(-cmi_nats))


def _channel_indices(total: int, channels):
    """Normalize channels arg to a list of non-negative indices."""
    if channels is None:
        return []
    if isinstance(channels, int):
        channels = [channels]
    return [c % total for c in channels]


def _single_cov_cmi(a: np.ndarray, b: np.ndarray, c: np.ndarray | None) -> float:
    """Compute I(A;B|C) with a single joint covariance."""
    if a.shape[0] < 4:
        return 0.0

    if c is None or c.shape[1] == 0:
        joint = np.concatenate([a, b], axis=1)
        cov = _fit_joint_cov(joint)
        a_idx = list(range(a.shape[1]))
        b_idx = list(range(a.shape[1], a.shape[1] + b.shape[1]))
        return _gaussian_cmi_from_cov(cov, a_idx, b_idx)

    joint = np.concatenate([a, b, c], axis=1)
    cov = _fit_joint_cov(joint)
    a_idx = list(range(a.shape[1]))
    b_idx = list(range(a.shape[1], a.shape[1] + b.shape[1]))
    c_idx = list(range(a.shape[1] + b.shape[1], a.shape[1] + b.shape[1] + c.shape[1]))
    return _gaussian_cmi_from_cov(cov, a_idx, b_idx, c_idx)


def compute_l_self(
    data: np.ndarray,
    tau: int = 2,
    d: int = 3,
    model_channels=-1,
    exog_channels=None,
    max_lag: int | None = None,
) -> float:
    """
    Estimate the self-model loop gate L_self = min(R_in_norm, R_out_norm) using
    a single-joint-covariance Ledoit-Wolf CMI estimator over multiple candidate lags.

    Args:
        data: 2D array of shape (n_channels, n_samples).
        tau: embedding delay (samples). Used as the lag step for the CMI legs.
        d: embedding dimension. Also used as the maximum number of candidate lags
            if max_lag is not provided.
        model_channels: int or list of int. Channel(s) treated as the internal
            model M. Default -1 (last channel). This is an operational choice;
            the theorem-grade M_t is not observable in EEG.
        exog_channels: int or list of int. Channel(s) treated as exogenous E.
            Default None (no conditioning on E). This is a known limitation:
            if a common driver is unobserved, no purely observational measure can
            separate common-cause from genuine feedback without an observed E
            proxy (causal-inference identifiability limit).
        max_lag: int. Maximum lag (in multiples of tau) to test. Default d.

    Returns:
        float: L_self in [0, 1). For each leg we take the maximum CMI over the
        candidate lags, then L_self = min(R_in_norm, R_out_norm).
    """
    n_channels, n_samples = data.shape
    if n_channels < 2 or n_samples < 8:
        return 0.0

    model_ch = _channel_indices(n_channels, model_channels)
    exog_ch = _channel_indices(n_channels, exog_channels)
    sensor_ch = [c for c in range(n_channels) if c not in model_ch and c not in exog_ch]

    if not sensor_ch:
        return 0.0

    if max_lag is None:
        max_lag = max(1, d)

    r_in_max = 0.0
    r_out_max = 0.0

    for k in range(1, max_lag + 1):
        lag = k * tau
        if n_samples <= 2 * lag + 2:
            break

        # R_in(k) = I( X_{t-k*tau} ; M_t | E_t )
        a_in = data[sensor_ch, :-lag].T
        b_in = data[model_ch, lag:].T
        c_in = data[exog_ch, lag:].T if exog_ch else None
        r_in = _single_cov_cmi(a_in, b_in, c_in)
        r_in_max = max(r_in_max, r_in)

        # R_out(k) = I( M_t ; X_{t+k*tau} | X_t, E_t )
        # Align t so that t + k*tau is in range.
        a_out = data[model_ch, lag:n_samples - lag].T
        b_out = data[sensor_ch, 2 * lag:].T
        x_cond = data[sensor_ch, lag:n_samples - lag].T
        if exog_ch:
            e_cond = data[exog_ch, lag:n_samples - lag].T
            c_out = np.concatenate([x_cond, e_cond], axis=1)
        else:
            c_out = x_cond
        r_out = _single_cov_cmi(a_out, b_out, c_out)
        r_out_max = max(r_out_max, r_out)

    r_in_norm = _normalize_cmi(r_in_max)
    r_out_norm = _normalize_cmi(r_out_max)
    return float(min(r_in_norm, r_out_norm))
