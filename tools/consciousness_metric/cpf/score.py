import warnings
import numpy as np
from cpf.embedding import delay_embed
from cpf.differentiation import compute_pca_entropy
from cpf.coherence import compute_plv, compute_wpli
from cpf.directed import compute_prediction_gain
from cpf.self_model import compute_l_self


def compute_cpf_components(
    data: np.ndarray,
    tau: int = 1,
    d: int = 3,
    model_channels=None,
    exog_channels=None,
) -> dict:
    """
    Calculates all components required by the Phase 0 consciousness metric.

    Args:
        data: 2D array (n_channels, n_samples)
        tau: embedding delay
        d: embedding dimension
        model_channels: optional channel(s) to treat as the internal model M for
            the new L_self CMI estimator. If None, defaults to the last channel.
        exog_channels: optional channel(s) to treat as exogenous E for L_self.
            If None, E is empty and L_self computes UNCONDITIONAL MI, not
            conditional MI. This is rarely what you want — pass explicit
            exog_channels when the exogenous input channels are known.

    Returns:
        Dictionary containing D_int, C_coh_plv, C_coh_wpli, D_dir_proxy, L_self,
        and the final composite scores.
    """
    # 1. Differentiation (D_int) via PCA Entropy on Delay Embeddings
    try:
        embedded_data = delay_embed(data, tau=tau, d=d)
        D_int = compute_pca_entropy(embedded_data)
    except ValueError:
        D_int = 0.0

    # 2. Coherence (C_coh)
    C_coh_plv = compute_plv(data)
    C_coh_wpli = compute_wpli(data)

    # 3. Directed Information / Prediction Gain (D_dir_proxy) — legacy
    D_dir_proxy = compute_prediction_gain(data)

    # 4. Self-model CMI gate L_self — new canonical estimator
    # If no model_channels specified, default to the last channel for the new
    # estimator. This is an operational default; the caller should override it
    # when the model channel is known. CMI lags are tested in sample units
    # (tau_cmi=1) up to the embedding dimension d; the embedding tau is used
    # only for D_int and C_coh.
    #
    # WARNING: If exog_channels is None, E is empty and L_self computes
    # unconditional MI I(X;M) instead of conditional MI I(X;M|E).
    # This is almost never the intended use — pass explicit exog_channels.
    if exog_channels is None:
        warnings.warn(
            "compute_cpf_components: exog_channels is None — E is empty. "
            "L_self will compute UNCONDITIONAL MI I(X;M), not conditional "
            "MI I(X;M|E). This is rarely what you want. Pass explicit "
            "exog_channels when the exogenous input channels are known.",
            stacklevel=2,
        )

    if model_channels is None:
        L_self = compute_l_self(data, tau=1, d=d)
    else:
        L_self = compute_l_self(
            data,
            tau=1,
            d=d,
            model_channels=model_channels,
            exog_channels=exog_channels,
        )

    # 5. Composite Scores
    C_PF_reduced_plv = D_int * C_coh_plv * D_dir_proxy
    C_PF_reduced_wpli = D_int * C_coh_wpli * D_dir_proxy
    C_PF_lself_wpli = D_int * C_coh_wpli * L_self

    return {
        "D_int": float(D_int),
        "C_coh_plv": float(C_coh_plv),
        "C_coh_wpli": float(C_coh_wpli),
        "D_dir_proxy": float(D_dir_proxy),
        "L_self": float(L_self),
        "C_PF_reduced_plv": float(C_PF_reduced_plv),
        "C_PF_reduced_wpli": float(C_PF_reduced_wpli),
        "C_PF_lself_wpli": float(C_PF_lself_wpli),
    }
