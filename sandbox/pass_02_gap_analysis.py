import numpy as np
import matplotlib.pyplot as plt
from scipy.special import j0, j1, jn_zeros

def koide_factors(delta):
    return 1 + np.sqrt(2) * np.cos(delta + np.array([0, 2*np.pi/3, 4*np.pi/3])[:, None])

def fourier_coeffs(func, n_harmonics=20):
    deltas = np.linspace(0, 2*np.pi, 1000, endpoint=False)
    values = func(deltas)
    coeffs = np.fft.rfft(values) / len(deltas)
    return np.abs(coeffs[:n_harmonics])

def test_koide_harmonics():
    print("--- Koide Phase Harmonic Analysis ---")
    
    # f(delta) = product of g_k
    def f_delta(delta):
        g = koide_factors(delta)
        return np.prod(g, axis=0)
    
    # Sum of 1/g_k^n
    def sum_inv_g(delta, n):
        g = koide_factors(delta)
        return np.sum(1/g**n, axis=0)

    for n in [1, 2, 3, 4, 6]:
        coeffs = fourier_coeffs(lambda d: sum_inv_g(d, n))
        print(f"\nSum 1/g_k^{n} harmonics:")
        for i in range(1, 6):
            h = 3*i
            if h < len(coeffs):
                print(f"  cos({h} delta): {coeffs[h]:.6f} (ratio to cos(3d): {coeffs[h]/coeffs[3]:.4f})")

def test_pitch_matching():
    print("\n--- Helical Pitch Matching Analysis ---")
    # Z(rho) = 2*pi * rho * k * J0(zeta * rho) / (zeta * J1(zeta * rho))
    # Characteristic radius rho* where dJ_phi/d_rho = 0
    # Condition: J0(zeta * rho*) * [J0(zeta * rho*) - J2(zeta * rho*)] = 2 * J1^2(zeta * rho*)
    
    # Let x = zeta * rho
    # J0(x) * (J0(x) - J2(x)) = 2 * J1(x)^2
    # Since J2(x) = 2/x * J1(x) - J0(x)
    # J0(x) * (2*J0(x) - 2/x * J1(x)) = 2 * J1(x)^2
    # J0(x)^2 - (1/x) * J0(x) * J1(x) - J1(x)^2 = 0
    
    from scipy.optimize import fsolve
    from scipy.special import jv
    
    def condition(x):
        return j0(x)**2 - (1/x) * j0(x) * j1(x) - j1(x)**2
    
    x_star = fsolve(condition, 1.0)[0]
    print(f"Characteristic radius factor (zeta * rho*): {x_star:.6f}")
    
    # Z(rho*) = 2*pi * (x_star / zeta) * k * J0(x_star) / (zeta * J1(x_star))
    # Z(rho*) = 2*pi * (k / zeta^2) * x_star * J0(x_star) / J1(x_star)
    
    # In PF/Dirac units:
    # k is the longitudinal wave vector: k = p/hbar = gamma * m * beta * c / hbar = gamma * beta / r_C
    # zeta is the transverse wave vector. 
    # Hypothesis: zeta = 1 / r_C (confinement at Compton scale)
    
    # Z(rho*) = 2*pi * (gamma * beta / r_C) * r_C^2 * [x_star * J0(x_star) / J1(x_star)]
    # Z(rho*) = 2*pi * gamma * beta * r_C * [x_star * J0(x_star) / J1(x_star)]
    
    # Route H drift: d = 2*pi * beta * r_C
    
    # Ratio Z(rho*) / d = gamma * [x_star * J0(x_star) / J1(x_star)]
    
    c_factor = x_star * j0(x_star) / j1(x_star)
    print(f"Geometric factor (x* J0(x*) / J1(x*)): {c_factor:.6f}")
    
    # For Z(rho*) = d, we need gamma * c_factor = 1
    # gamma = 1 / c_factor
    gamma_target = 1 / c_factor
    beta_target = np.sqrt(1 - 1/gamma_target**2)
    sin2theta_target = beta_target**2 # Assuming x = beta^2 for Weinberg angle
    
    print(f"Required gamma for matching: {gamma_target:.6f}")
    print(f"Required beta for matching: {beta_target:.6f}")
    print(f"Predicted sin^2(theta_W) = beta^2: {sin2theta_target:.6f}")
    print(f"Experimental sin^2(theta_W) (MS-bar): ~0.231")
    print(f"Experimental sin^2(theta_W) (On-shell): ~0.223")

if __name__ == "__main__":
    test_koide_harmonics()
    test_pitch_matching()
