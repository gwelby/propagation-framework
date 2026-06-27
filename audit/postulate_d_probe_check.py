#!/usr/bin/env python3
"""
Does 'seven approaches converged on a=0' hold up?
Test whether the symmetric-mode probes (#4 mutual info, #5 Fisher, #6 pointer
basis) actually DISCRIMINATE a=0 from a!=0, or whether they prefer the
symmetric mode for EVERY a (in which case they are not evidence for a=0).

Setup from G3_CLOSURE: U = a*I + b*M, with M = Sbar + Sbar^T on Z3,
constraint a + 2b = 1 (symmetric-mode invariant).
"""
import numpy as np

# Z3 cyclic shift
S = np.array([[0,1,0],[0,0,1],[1,0,0]], float)
M = S + S.T
e_sym = np.ones(3)/np.sqrt(3)     # symmetric mode

print("a      b       U@e_sym (should=e_sym, eval=1?)   U|Q eigenvalue   U^3|Q")
for a in [0.0, 0.25, 0.5, 0.95]:
    b = (1-a)/2
    U = a*np.eye(3) + b*M
    Ue = U @ e_sym
    eval_sym = (Ue / e_sym)[0]
    # Q sector = orthogonal complement of e_sym
    w, V = np.linalg.eigh(U)
    # eigenvalue on Q (the non-symmetric one)
    qval = (3*a-1)/2
    print(f"{a:.2f}   {b:.3f}   eval_sym={eval_sym:+.4f}   U|Q={qval:+.4f}        {qval**3:+.5f}")

print()
print("CONCLUSION:")
print("  * Symmetric mode e_sym is an eigenvector with eigenvalue 1 for ALL a.")
print("    => 'symmetric mode is preferred / pointer / max-info' is TRUE for every a.")
print("    => probes #4,#5,#6 do NOT discriminate a=0; they restate Z3 symmetry.")
print("  * The Q-sector eigenvalue (3a-1)/2 DOES depend on a:")
print("    a=0 gives exactly -1/2 = cos(2pi/3), hence U^3|Q = -1/8 = the 'prediction'.")
print("    => a=0 is the value CHOSEN to reproduce cos(2pi/3); the eigenvalue match")
print("       is target-loaded, not independent confirmation.")
