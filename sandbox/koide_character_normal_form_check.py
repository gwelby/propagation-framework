#!/usr/bin/env python3
"""
Check the 1+2 / Z3 character normal form of a real triple.
"""

import sympy as s


def main() -> None:
    x0, x1, x2 = s.symbols("x0 x1 x2", real=True)
    omega = s.exp(2 * s.pi * s.I / 3)

    A = (x0 + x1 + x2) / 3
    alpha = (2 * x0 - x1 - x2) / 3
    beta = (x2 - x1) / s.sqrt(3)
    z = alpha + s.I * beta

    y0 = s.re(z)
    y1 = s.expand_complex(s.re(omega * z))
    y2 = s.expand_complex(s.re(omega**2 * z))

    print("A =", A)
    print("alpha =", alpha)
    print("beta =", beta)
    print("z =", z)
    print()
    print("Recovered traceless coordinates from Re(omega^k z):")
    print("  y0 =", s.simplify(y0))
    print("  y1 =", s.simplify(y1))
    print("  y2 =", s.simplify(y2))
    print()
    print("Check x_k = A + Re(omega^k z):")
    print("  x0 - (A+y0) =", s.simplify(x0 - (A + y0)))
    print("  x1 - (A+y1) =", s.simplify(x1 - (A + y1)))
    print("  x2 - (A+y2) =", s.simplify(x2 - (A + y2)))
    print()
    print("Canonical phase slope:")
    print("  tan(delta) = beta/alpha =", s.simplify(beta / alpha))


if __name__ == "__main__":
    main()
