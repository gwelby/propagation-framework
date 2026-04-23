#!/usr/bin/env python3
"""
Minimal matrix trace check for the abstract cos(9 delta) carrier.
"""

import sympy as s


def main() -> None:
    delta = s.symbols("delta", real=True)
    omega = s.exp(2 * s.pi * s.I / 3)

    U = s.exp(s.I * delta) * s.diag(1, omega, omega**2)

    # `simplify` leaves root-of-unity sums half-reduced here; `expand_complex` collapses them cleanly.
    tr1 = s.expand_complex(s.trace(U))
    tr2 = s.expand_complex(s.trace(U**2))
    tr3 = s.simplify(s.trace(U**3))
    obs = s.simplify(s.re(tr3**3) / 27)

    print("omega =", omega)
    print("Tr U   =", tr1)
    print("Tr U^2 =", tr2)
    print("Tr U^3 =", tr3)
    print("Re[(Tr U^3)^3]/27 =", s.expand_trig(obs))


if __name__ == "__main__":
    main()
