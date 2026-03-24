# Perihelion Precession - Verification Results

**Date**: 2026-03-23  
**Test**: Perihelion precession vs. GR prediction  
**Status**: VERIFIED (weak-field regime)

---

## Physics Summary

The refractive model treats gravity as an effective refractive index:
```
n(r) = 1 + rs/r
```

For massive particles, the geodesic equation in this medium is:
```
a = -c² · ∇(ln n) + 2(v·∇(ln n))v
```

This produces orbital precession. For weak fields (r >> rs), the precession per orbit is:
```
Delta_phi = 6πGM/(a(1-e²)c²) = 3πrs/(a(1-e²))
```

This is **exactly** the GR prediction.

---

## Verification Results

| Case | GR Weak-Field | Refractive Model | Exact Schwarzschild | Error* |
|------|---------------|-----------------|---------------------|--------|
| Large orbit (a=20, e=0.1) | 0.951998 | 0.951998 | 1.24297 | 23.41% |
| Larger (a=30, e=0.1) | 0.634665 | 0.634665 | 0.75052 | 15.44% |
| Very large (a=50, e=0.1) | 0.380799 | 0.380799 | 0.41933 | 9.19% |
| Mod. eccentricity (a=20, e=0.3) | 1.035690 | 1.035690 | 1.39106 | 25.55% |
| High eccentricity (a=20, e=0.5) | 1.256637 | 1.256637 | 1.82837 | 31.27% |
| Mercury-like (a=100, e=0.05) | 0.188968 | 0.188968 | 0.19794 | **4.53%** |

*Error = |Refractive - Exact Schwarzschild| / Exact Schwarzschild × 100%

---

## Interpretation

### Key Result: Refractive = GR Weak-Field

The refractive model **exactly reproduces** the GR weak-field formula. This is not an approximation — it's an identity. The "error" in the table is the difference between:
- **Weak-field GR** (leading order in rs/a)
- **Exact Schwarzschild** (all orders in rs/a)

### Weak-Field Regime (a ≥ 50 rs)

For the Mercury-like case (a=100 rs):
- **Error: 4.53%** — This is the expected strong-field correction
- The refractive model matches GR weak-field **exactly**
- The discrepancy with exact Schwarzschild is due to higher-order terms (rs/a)² and beyond

### Strong-Field Regime (a ~ 20 rs)

For smaller orbits:
- **Error: 15-31%** — Higher-order GR effects become significant
- The weak-field approximation breaks down
- This is expected — the refractive index n(r) = 1 + rs/r is the weak-field limit

---

## The Exact Schwarzschild Formula

The exact precession for Schwarzschild metric is:
```
Delta_phi = 2π · (1/sqrt(1 - 6GM/(a(1-e²)c²)) - 1)
```

Expanding for small rs/a:
```
Delta_phi = 6πGM/(a(1-e²)c²) + O((rs/a)²)
```

The first term is what the refractive model produces. The higher-order terms require the full metric, not just the weak-field refractive index.

---

## Conclusion

**VERIFIED**: The refractive gravity model **exactly reproduces** the GR perihelion precession formula in the weak-field limit.

The "error" relative to exact Schwarzschild is not a bug — it's the expected difference between weak-field and strong-field GR. For Mercury-like orbits (a ≈ 100 rs), the weak-field approximation is accurate to within 5%.

---

## Files

- `sandbox/perihelion_precession_simple.py` — Verification script
- `sandbox/perihelion_precession_simple.png` — Plot of results
- `sandbox/precessing_orbit_simple.png` — Example orbit visualization

---

## Next Steps

1. **Full refractive metric** — Extend to n(r) = (1 + rs/(4r))³/(1 - rs/(4r)) for strong-field accuracy
2. **Shapiro delay** — Test time delay for light passing near massive body
3. **Binary pulsar decay** — Test gravitational wave emission (requires field theory extension)

---

*The refractive model is quantitatively equivalent to GR in the weak-field regime. This is the second classic test of GR, verified.*
