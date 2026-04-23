#!/usr/bin/env python3
"""
Exact check for the minimal cubic selector class in the reduced Koide phase variable.

This script verifies:
1. degree < 3 cannot isolate cos(9 delta)
2. the unique cubic family that does isolate it
3. the explicit Chebyshev-tuned cubic in f(delta)
"""

import sympy as s


def main() -> None:
    f, x = s.symbols("f x", real=True)
    A, B, C, D = s.symbols("A B C D", real=True)
    k, c = s.symbols("k c", real=True)

    print("Setup:")
    print("  f(delta) = -1/2 + x/sqrt(2), where x = cos(3 delta)")
    print("  target   = cos(9 delta) = T3(x) = 4 x^3 - 3 x")
    print()

    cheb = s.expand(s.chebyshevt(3, s.sqrt(2) * (f + s.Rational(1, 2))))
    print("Chebyshev target expressed in f:")
    print(" ", cheb)
    print()

    generic = A + B * f + C * f**2 + D * f**3
    generic_x = s.expand(generic.subs(f, -s.Rational(1, 2) + x / s.sqrt(2)))

    print("Generic cubic in x after substitution:")
    print(" ", generic_x)
    print()

    print("Coefficient map:")
    print("  x^3:", s.expand(generic_x).coeff(x, 3))
    print("  x^2:", s.expand(generic_x).coeff(x, 2))
    print("  x^1:", s.expand(generic_x).coeff(x, 1))
    print("  x^0:", s.expand(generic_x).coeff(x, 0))
    print()

    sol = s.solve(
        [
            s.Eq(s.expand(generic_x).coeff(x, 3), 4 * k),
            s.Eq(s.expand(generic_x).coeff(x, 2), 0),
            s.Eq(s.expand(generic_x).coeff(x, 1), -3 * k),
            s.Eq(s.expand(generic_x).coeff(x, 0), c),
        ],
        [A, B, C, D],
        dict=True,
    )

    print("Unique cubic family for c + k*(4*x^3 - 3*x):")
    for row in sol:
        print(" ", row)
    print()

    tuned = s.sqrt(2) * (8 * f**3 + 12 * f**2 + 3 * f - s.Rational(1, 2))
    tuned_back = s.expand(tuned.subs(f, -s.Rational(1, 2) + x / s.sqrt(2)))

    print("Normalized tuned cubic:")
    print(" ", tuned)
    print()
    print("Back-substitution check:")
    print(" ", tuned_back)


if __name__ == "__main__":
    main()
