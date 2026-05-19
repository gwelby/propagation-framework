# G3-OP-MAP Spectral Contract Audit
*Date: 2026-05-13*
*Auditor: Codex*
*Target: `/mnt/d/DeepSeek/sandbox/g3_op_map_contract.py`*
*Status: conditional negative; v3 script patched and rerun with corrected codomains*

## 1. Verdict

DeepSeek's spectral-map contract points in the right direction:

```text
No bridge was found in the tested spectral-map regimes.
G3 remains CONDITIONAL 0.88.
```

The original v1 script was not a clean sign-off artifact because it compared objects in different bases. That defect is now patched in `/mnt/d/DeepSeek/sandbox/g3_op_map_contract.py` v3.

The corrected v3 result is still negative for the tested spectral/DFT map. It is a valid subroute negative, not a full negative closure of every possible `G3-OP-MAP` route.

## 2. What Reproduced From v1

Command:

```bash
python3.12 /mnt/d/DeepSeek/sandbox/g3_op_map_contract.py
```

Output reproduced:

| Regime | min KL | Bridge? |
|--------|-------:|:-------:|
| null `(kappa=0, gamma=0)` | 0.1897 | NO |
| coupled `(kappa=0.5, gamma=0)` | 0.2489 | NO |
| damped `(kappa=0.5, gamma=0.1)` | 0.2213 | NO |
| heavy damp `(kappa=0.5, gamma=0.5)` | 0.2834 | NO |

So the operational result is reproducible: the tested spectral map does not drive KL near zero.

## 3. Main Audit Issue

`F_spectral(chi)` returns a probability vector over Fourier-mode powers:

```python
chi_f = F.conj().T @ chi
p_j = |chi_f[j]|^2 / sum_k |chi_f[k]|^2
```

But the verification gate then applies `T_sym^3` directly to that vector:

```python
T3 @ p_t
```

`T_sym^3` is written as a channel-basis operator. Its spectral form is:

```text
T_sym^3 = P0 - (1/8) Q
```

So applying the channel-basis matrix to a Fourier-mode power distribution mixes codomains. There are two coherent options:

1. **Channel probability map**: return probabilities in the channel basis, then `T3 @ p_t` is typed correctly.
2. **Spectral power map**: stay in Fourier mode space, but compare against a spectral-power contraction rule such as:

   ```text
   p0 -> p0
   p1 -> p1 / 64
   p2 -> p2 / 64
   renormalize
   ```

   because amplitudes in the Q-sector contract by `-1/8`, so powers contract by `1/64`.

The v1 script mixed option 1 and option 2.

## 4. Basis-Corrected Spot Check

I ran a quick basis-corrected spectral-power comparison using:

```text
expected(p) = normalize([p0, p1/64, p2/64])
```

Result:

| Regime | KL(h=3) | KL(h=10) | KL(h=50) | min KL |
|--------|-------:|--------:|--------:|-------:|
| null | 1.3949 | 2.1485 | 1.6881 | 1.3949 |
| coupled | 1.0858 | 1.2852 | 1.3250 | 1.0858 |
| damped | 1.2284 | 1.5389 | 1.5956 | 1.2284 |
| heavy damp | 1.1935 | 1.7159 | 1.6814 | 1.1935 |

This makes the gap larger, not smaller.

So the basis bug did not rescue the spectral map. It weakened v1's formal cleanliness, but the negative direction survived.

## 5. v3 Patched Gate Result

I patched `/mnt/d/DeepSeek/sandbox/g3_op_map_contract.py` so it now tests two separately typed comparisons:

1. `spectral_power_corrected`: Fourier-mode powers compared against `normalize([p0, p1/64, p2/64])`.
2. `channel_power_diagnostic`: channel powers compared against `T_sym^3 @ p` as a basis-dependent diagnostic.

Command:

```bash
python3.12 /mnt/d/DeepSeek/sandbox/g3_op_map_contract.py
```

The script now runs five seeds, horizons `3`, `10`, `50`, `noise=0` and `noise=0.05` controls, and damping values `gamma = 0.1, 0.5, 1.0`.

Corrected spectral-power result:

| Regime | min mean KL | Bridge? |
|--------|------------:|:-------:|
| null/no-noise | 1.2895 | NO |
| null/noisy | 1.4410 | NO |
| coupled/no-noise | 1.1866 | NO |
| coupled/noisy | 1.1543 | NO |
| damped `gamma=0.1` noisy | 1.1951 | NO |
| damped `gamma=0.5` noisy | 1.1684 | NO |
| damped `gamma=1.0` noisy | 1.1747 | NO |

Best corrected spectral result: `coupled/noisy`, min mean KL `1.1543`.

Channel-power diagnostic result:

| Best diagnostic regime | min mean KL | Bridge? |
|------------------------|------------:|:-------:|
| damped `gamma=0.1` noisy | 0.3985 | NO |

The diagnostic also does not cross the bridge threshold (`min mean KL < 0.05`).

## 6. Scope Limits

Do not overstate this as:

```text
all damping regimes fail
all coarse-graining maps fail
all measurement maps fail
G3-OP-MAP is fully closed negatively
```

The patched script only tests:

- one spectral map,
- one channel-power diagnostic,
- seven `(kappa, gamma, noise)` regimes,
- horizons `3`, `10`, and `50`,
- five random seeds,
- a linearized stochastic oscillator.

The supported statement is narrower:

```text
The tested spectral/DFT map does not bridge the linearized oscillator to T_sym^3.
When the comparison is made basis-consistent, the gap persists and grows.
```

## 7. Applied Fix

This fix has been applied in v3:

```text
D = linearized Z3 phase-space states
F = spectral-power map into Fourier-mode probability simplex
R = bridge if spectral-power evolution matches normalize([p0, p1/64, p2/64])
V = KL sweep across horizons, damping, seeds
X = positive KL floor under the corrected spectral-power target
```

The remaining work is not to fix this script. The remaining work is to try a different candidate class:

- coarse-graining / RG map,
- damping or environment mechanism derived from PF rather than inserted,
- nonlinear completion,
- or an explicit measurement theory.

## 8. Board Impact

No confidence score change.

`G3-OP-MAP` remains the active bounded strike.

The spectral-map subroute now has a stronger conditional negative:

```text
Spectral/DFT map is PF-native and horizon-stable, but it does not reproduce the discrete closure operator in the tested linearized regimes. Corrected codomain comparison gives min mean KL >= 1.1543 for the spectral map, far above the 0.05 bridge threshold.
```
