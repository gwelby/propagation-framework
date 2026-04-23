#!/usr/bin/env python3
"""
Audit existing Koide observable families against the exact cubic selector target.
"""

import sympy as s


def main() -> None:
    f = s.symbols("f", nonzero=True)
    e1 = s.Integer(3)
    e2 = s.Rational(3, 2)
    e3 = f

    print("Koide reduced scalar:")
    print("  f(delta) = -1/2 + cos(3 delta)/sqrt(2)")
    print()

    print("Exact cubic selector target:")
    print("  Q*(f) = c + sqrt(2) * k * (8 f^3 + 12 f^2 + 3 f - 1/2)")
    print()

    # Reciprocal power sums for roots g_k with symmetric data (e1,e2,e3).
    E1 = e2 / e3
    E2 = e1 / e3
    E3 = s.Integer(1) / e3

    p1 = E1
    p2 = s.expand(E1 * p1 - 2 * E2)
    p3 = s.expand(E1 * p2 - E2 * p1 + 3 * E3)
    p4 = s.expand(E1 * p3 - E2 * p2 + E3 * p1)

    print("Reciprocal sums:")
    print("  sum 1/g    =", s.factor(p1))
    print("  sum 1/g^2  =", s.factor(p2))
    print("  sum 1/g^3  =", s.factor(p3))
    print("  sum 1/g^4  =", s.factor(p4))
    print()

    print("Rivero-style observable families in f:")
    print("  cross term  f^6 * sum 1/g^2 =", s.expand(f**6 * p2))
    print("  pure term   f^12 * sum 1/g^4 =", s.expand(f**12 * p4))
    print()

    # Low trace powers Tr G^n for diagonal Koide matrix G = diag(g0,g1,g2)
    power = {1: s.Integer(3), 2: s.Integer(6)}
    for n in range(3, 9):
        if n == 3:
            power[n] = s.expand(e1 * power[2] - e2 * power[1] + 3 * e3)
        else:
            power[n] = s.expand(e1 * power[n - 1] - e2 * power[n - 2] + e3 * power[n - 3])

    print("Low trace powers Tr G^n:")
    for n in range(1, 9):
        print(f"  Tr G^{n} =", power[n])


if __name__ == "__main__":
    main()
