# V_cross Part (d) Audit - 2026-04-23

**Agent:** Codex  
**Target:** Rivero `cos9delta_derivation.py` Part (d), the `V_cross` vs pure `W3^2` harmonic comparison  
**Status:** reconstructed from local audited formulas, not a direct run of Rivero's script

## Source Status

Attempted direct source fetch:

```bash
set -o pipefail; curl -fsSL --connect-timeout 5 http://lxbifi11.bifi.unizar.es:8080/3/calculations/cos9delta_derivation.py >/tmp/rivero_cos9delta_derivation.py
```

Result:

```text
curl: (7) Failed to connect to lxbifi11.bifi.unizar.es port 8080 after 140 ms: Couldn't connect to server
```

So this audit reconstructs Part (d) from formulas already preserved in
`derivations/koide_phase_existing_observable_audit_2026-04-20.md`.

## Inputs

Let

```text
x = cos(3*delta)
f(delta) = -1/2 + x/sqrt(2)
```

The preserved exact reductions are:

```text
V_cross = f^6 * sum_k 1/g_k^2
        = -6 f^5 + (9/4) f^4

V_pure  = f^12 * sum_k 1/g_k^4
        = 24 f^10 - 27 f^9 + (81/16) f^8
```

Both were expanded as:

```text
V(delta) = sum_m a_m cos(3*m*delta)
```

Repro script:

```bash
python3.12 /mnt/d/Fundamentals/sandbox/v_cross_part_d_audit_2026_04_23.py
```

## Harmonic Coefficients

| m | harmonic | V_cross | V_cross float | V_pure | V_pure float |
|---:|---:|---:|---:|---:|---:|
| 0 | 0 | `597/128` | `4.664062500` | `1794171/32768` | `54.753753662` |
| 1 | 3 | `-45*sqrt(2)/8` | `-7.954951288` | `-72807*sqrt(2)/1024` | `-100.551412925` |
| 2 | 6 | `39/8` | `4.875000000` | `79569/1024` | `77.704101562` |
| 3 | 9 | `-93*sqrt(2)/64` | `-2.055029083` | `-145557*sqrt(2)/4096` | `-50.256026245` |
| 4 | 12 | `69/128` | `0.539062500` | `220617/8192` | `26.930786133` |
| 5 | 15 | `-3*sqrt(2)/64` | `-0.066291261` | `-34083*sqrt(2)/4096` | `-11.767734582` |
| 6 | 18 | `0` | `0.000000000` | `8379/2048` | `4.091308594` |
| 7 | 21 | `0` | `0.000000000` | `-6309*sqrt(2)/8192` | `-1.089144698` |
| 8 | 24 | `0` | `0.000000000` | `6825/32768` | `0.208282471` |
| 9 | 27 | `0` | `0.000000000` | `-147*sqrt(2)/8192` | `-0.025377123` |
| 10 | 30 | `0` | `0.000000000` | `3/2048` | `0.001464844` |

Raw ratios:

| Term | cos(3d) / cos(9d) | cos(6d) / cos(9d) |
|---|---:|---:|
| `V_cross` | `3.87096774194` | `-2.37222920140` |
| `V_pure` | `2.00078319833` | `-1.54616485562` |

Important sign result: raw `V_cross` and raw `V_pure` both have the same signs for `cos(3d)`, `cos(6d)`, and `cos(9d)`: negative, positive, negative. Same-sign addition therefore does not cancel `cos(3d)`.

## Cancellation Test

Use one relative coupling:

```text
V_total = V_cross + rho * V_pure
```

Exact cancellation ratios:

```text
rho to cancel cos(3*delta) = -1920/24269 = -0.079113272075
rho to cancel cos(6*delta) = -1664/26523 = -0.062738000980
```

These are not equal. One free relative coupling cannot exactly cancel both lower harmonics.

### Case A: cancel cos(3*delta)

At `rho = -1920/24269`, `cos(3*delta)` is exactly zero.

| harmonic | total coeff float | relative to abs cos9 |
|---:|---:|---:|
| 3 | `0.000000000` | `0.000000000` |
| 6 | `-1.272425728` | `0.662414816` |
| 9 | `1.920889595` | `1.000000000` |
| 12 | `-1.591520111` | `0.828532840` |
| 15 | `0.864692727` | `0.450152226` |
| 18 | `-0.323676810` | `0.168503599` |

This is the interesting result: with a negative relative sign and a tuned magnitude, `cos(9*delta)` becomes the largest oscillating harmonic.

### Case B: cancel cos(6*delta)

At `rho = -1664/26523`, `cos(6*delta)` is exactly zero, but `cos(3*delta)` remains larger than `cos(9*delta)`.

| harmonic | total coeff float | relative to abs cos9 |
|---:|---:|---:|
| 3 | `-1.646556646` | `1.499686989` |
| 6 | `0.000000000` | `0.000000000` |
| 9 | `1.097933541` | `1.000000000` |
| 12 | `-1.150521187` | `1.047896930` |

This does not produce clean `cos(9*delta)` dominance.

### Case C: least-squares lower-harmonic suppression

Least-squares suppression of the pair `(cos3, cos6)` gives:

```text
rho = -0.0729905602414
```

| harmonic | total coeff float | relative to abs cos9 |
|---:|---:|---:|
| 3 | `-0.615647326` | `0.381634333` |
| 6 | `-0.796665906` | `0.493846150` |
| 9 | `1.613186428` | `1.000000000` |
| 12 | `-1.426630668` | `0.884355734` |
| 15 | `0.792642279` | `0.491351939` |

Numerical scan over `rho in [-0.2, 0.1]` found:

```text
cos(9*delta) is the largest oscillating harmonic for rho in [-0.102738, -0.066376]
```

## Verdict

This is not a clean no-go, but it is not a derivation either.

What survives:

- The cross-term lane is a real structural lead.
- Raw same-sign addition does not cancel `cos(3*delta)`.
- If the action supplies a negative relative sign with `rho` roughly in `[-0.102738, -0.066376]`, `cos(9*delta)` becomes the largest oscillating harmonic.
- Exact `cos(3*delta)` cancellation occurs at `rho = -1920/24269`, and then `cos(9*delta)` is dominant.

What does not survive:

- There is no automatic cancellation from the preserved scalar formulas alone.
- One coupling cannot exactly cancel both `cos(3*delta)` and `cos(6*delta)`.
- This does not select the empirical phase `delta ~= 2/9`; it only addresses harmonic dominance.
- This does not upgrade Issue #5 from `EMPIRICAL`.

## Next Gate

The next bounded question is not another scalar scan. It is:

```text
Does Rivero's actual action Lagrangian fix the relative sign and magnitude of V_cross versus V_pure near rho ~= -0.079?
```

If yes, this becomes a legitimate Rivero re-contact lead. If no, the cross-term lane remains a tuned harmonic fact rather than a selector.
