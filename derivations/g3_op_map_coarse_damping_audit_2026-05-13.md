# G3-OP-MAP Coarse-Graining and Damping Audit
*Date: 2026-05-13*
*Auditor: Codex*
*Targets: `/mnt/d/DeepSeek/sandbox/coarse_graining_bridge.py`, `/mnt/d/DeepSeek/sandbox/damping_bridge.py`*
*Status: corrected subroute negatives; no claim-score change*

## Verdict

The coarse-graining and damping explorers support a negative result only after the
same codomain correction used in the spectral-contract audit.

Supported statement:

```text
In the tested linearized Z3 oscillator sandbox, simple block-average
coarse-graining and simple linear damping do not produce the T_sym^3 closure
operator in corrected spectral-power coordinates.
```

Unsupported overclaim:

```text
All coarse-graining maps fail.
All damping or environment maps fail.
G3-OP-MAP is closed negatively.
```

G3 remains `CONDITIONAL 0.88`.

## Audit Issue

The original coarse-graining script reused this invalid conversion:

```python
p_ch = abs(F @ p_spec)
```

where `p_spec` is already a Fourier-mode power distribution. Applying `F` to a
probability vector is not a valid inverse basis transform for amplitudes. The
headline `W=50`, `KL ~= 0.19-0.21` result came from that invalid Method A path.

The damping script also compared spectral probabilities through the wrong shape:
it evaluated a distribution against `T3 @ p` rather than comparing
`p_next` against the corrected spectral target derived from `p_t`.

## Applied Corrections

The scripts now separate two typed comparisons:

1. Corrected spectral-power comparison:

   ```text
   p = normalize(|F^dagger chi|^2)
   target(p) = normalize([p0, p1 / 64, p2 / 64])
   ```

   This is the canonical comparison for the spectral-power map because
   `T_sym^3` contracts Q-sector amplitudes by `-1/8`, so Q-sector powers contract
   by `1/64`.

2. Channel-power diagnostic:

   ```text
   p = normalize(|chi|^2)
   target(p) = T_sym^3 p
   ```

   This is allowed only as a diagnostic. It is not the spectral map and should
   not be mixed with the spectral-power codomain.

## Commands

```bash
python3.12 -m py_compile /mnt/d/DeepSeek/sandbox/coarse_graining_bridge.py /mnt/d/DeepSeek/sandbox/damping_bridge.py
python3.12 /mnt/d/DeepSeek/sandbox/coarse_graining_bridge.py
python3.12 /mnt/d/DeepSeek/sandbox/damping_bridge.py
```

## Corrected Results

### Coarse-Graining

Tested windows:

```text
W = 1, 2, 3, 5, 10, 20, 50, 100
```

Tested regimes:

```text
coupled: kappa=0.5, gamma=0
damped: kappa=0.5, gamma=0.1
heavy damped: kappa=0.5, gamma=0.5
```

Best corrected spectral-power result:

```text
W = 1
KL = 1.3629
bridge threshold = 0.05
verdict = NO BRIDGE
```

Best channel-power diagnostic:

```text
W = 50
KL = 0.4595
verdict = NO BRIDGE
```

The old `~0.19` floor should not be cited as a corrected spectral result.

### Damping

Tested damping values:

```text
gamma = 0, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0
```

Best corrected spectral-power result at horizon `h=3`:

```text
gamma = 2.0
mean KL = 1.1293
bridge threshold = 0.05
verdict = NO BRIDGE
```

Q-sector scaling remains qualitatively mismatched:

```text
T_sym^3 target alpha = -0.1250
observed alpha at gamma=0.0 = +0.8894
observed alpha at gamma=1.0 = +0.3747
```

Linear damping reduces persistence, but it does not create the required
Q-sector sign flip and contraction.

## Scope

This is a negative result for the tested sandbox lanes:

- state expansion evidence remains negative from the S2 gate,
- spectral/DFT map remains negative after codomain correction,
- simple linear damping remains negative after codomain correction,
- block-average coarse-graining remains negative after codomain correction.

This is not a theorem that every possible bridge is dead. The live remaining
classes are still:

- a PF-derived environment or measurement theory,
- a nonlinear completion,
- a stronger coarse-graining/RG map than block averaging,
- or an analytic proof that the primitive closure operator must be imported as
  an extra structure.

## Board Impact

No confidence-score change.

`G3-OP-MAP` remains the active bounded strike, but its easy linearized subroutes
are now mostly exhausted. Do not add more candidate states until the primitive
operator map is derived or explicitly declared extra physics.
