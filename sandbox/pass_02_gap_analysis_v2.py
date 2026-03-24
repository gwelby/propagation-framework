import numpy as np
from scipy.special import j0, j1

def koide_factors(delta):
    return 1 + np.sqrt(2) * np.cos(delta + np.array([0, 2*np.pi/3, 4*np.pi/3])[:, None])

def fourier_coeffs_safe(func, n_harmonics=20):
    offset = 0.5
    deltas = np.linspace(0, 2*np.pi, 2000, endpoint=False) + offset
    values = func(deltas)
    coeffs = np.fft.rfft(values) / len(deltas)
    return np.abs(coeffs[:n_harmonics])

def test_koide_harmonics():
    print("--- Koide Phase Harmonic Analysis (Finite Observables) ---")
    
    def f_pow(delta, n):
        g = koide_factors(delta)
        f = np.prod(g, axis=0)
        return f**n

    for n in [2, 4, 6]:
        coeffs = fourier_coeffs_safe(lambda d: f_pow(d, n))
        print(f"\nf(delta)^{n} harmonics:")
        for i in range(1, 6):
            h = 3*i
            if h < len(coeffs):
                print(f"  cos({h} delta): {coeffs[h]:.6f} (ratio to cos(3d): {coeffs[h]/coeffs[3]:.4f})")

    def sum_inv_g_safe(delta, n, eps=0.01):
        g = koide_factors(delta)
        return np.sum(1/(g**2 + eps)**(n/2), axis=0)

    print("\nSum 1/(g_k^2 + 0.01) harmonics (smoothed inverse):")
    coeffs = fourier_coeffs_safe(lambda d: sum_inv_g_safe(d, 2))
    for i in range(1, 6):
        h = 3*i
        if h < len(coeffs):
            print(f"  cos({h} delta): {coeffs[h]:.6f} (ratio to cos(3d): {coeffs[h]/coeffs[3]:.4f})")

def test_pitch_matching_refined():
    print("\n--- Refined Helical Pitch Matching ---")
    from scipy.optimize import fsolve
    
    def condition(x):
        return j0(x)**2 - (1/x) * j0(x) * j1(x) - j1(x)**2
    
    x_star = fsolve(condition, 1.0)[0]
    c_factor = x_star * j0(x_star) / j1(x_star)
    
    zeta_rc = 2.4048
    ratio = (1/zeta_rc**2) * c_factor
    print(f"At zeta = 2.4048/r_C (Compton radius waveguide), Z/d = {ratio:.6f} * gamma")
    
    beta2_w = 0.231
    gamma_w = 1 / np.sqrt(1 - beta2_w)
    zeta_rc_w = np.sqrt(gamma_w * c_factor)
    print(f"Required zeta for Weinberg angle (sin^2 theta = 0.231): {zeta_rc_w:.6f} / r_C")
    
    zeta_rc_sqrt2 = np.sqrt(2)
    gamma_sqrt2 = (zeta_rc_sqrt2**2) / c_factor
    beta2_sqrt2 = 1 - 1/gamma_sqrt2**2
    print(f"At zeta = sqrt(2)/r_C, predicted sin^2(theta_W) = {beta2_sqrt2:.6f}")

if __name__ == "__main__":
    test_koide_harmonics()
    test_pitch_matching_refined()
