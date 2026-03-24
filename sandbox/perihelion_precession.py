"""
Refractive Gravity - Perihelion Precession Verification
========================================================
Tests that massive particle orbits precess at the GR rate.

GR prediction for Mercury-like orbit:
  Delta_phi_per_orbit = 6πGM/(a(1-e²)c²) = 3πrs/(a(1-e²))

where:
  a = semi-major axis
  e = eccentricity
  rs = 2GM/c² = Schwarzschild radius

For a nearly circular orbit (e << 1):
  Delta_phi ≈ 3πrs/a  [radians per orbit]

Run: python sandbox/perihelion_precession.py
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Natural units: G = c = 1
G = 1.0
c = 1.0
M = 1.0
rs = 2 * G * M / (c ** 2)  # = 2


def effective_potential(r, L, rs):
    """
    Effective potential for massive particle in Schwarzschild.
    
    V_eff(r) = -GM/r + L²/(2r²) - GM·L²/(c²r³)
    
    The last term is the GR correction that causes precession.
    """
    GM = G * M
    return -GM/r + L**2/(2*r**2) - GM*L**2/(c**2 * r**3)


def orbit_equation(y, phi, mu, h):
    """
    Orbit equation: d²u/dφ² + u = mu/h² + 3·mu·u²
    
    where u = 1/r, mu = GM/c², h = L/c (angular momentum per unit mass / c)
    
    This is the exact equation for massive particles in Schwarzschild.
    """
    u, dudphi = y
    # d²u/dφ² = mu/h² + 3·mu·u² - u
    d2udphi2 = mu/h**2 + 3*mu*u**2 - u
    return [dudphi, d2udphi2]


def find_perihelion_positions(y_sol, phi):
    """
    Find perihelion positions (minimum r = maximum u) in the solution.
    """
    u = y_sol[:, 0]
    
    # Find local maxima of u (minima of r)
    du_dphi = np.gradient(u, phi)
    sign_changes = np.where(np.diff(np.sign(du_dphi)) < 0)[0]
    
    perihelion_phis = []
    for idx in sign_changes:
        # Refine with quadratic interpolation
        if idx > 0 and idx < len(phi) - 1:
            phi_local = phi[idx-1:idx+2]
            u_local = u[idx-1:idx+2]
            # Fit parabola and find maximum
            coeffs = np.polyfit(phi_local, u_local, 2)
            phi_max = -coeffs[1] / (2*coeffs[0])
            perihelion_phis.append(phi_max)
    
    return perihelion_phis


def compute_precession_refractive(a, e, dt=0.01, n_orbits=2):
    """
    Compute perihelion precession by direct simulation in the refractive medium.
    """
    GM = G * M

    # Initial conditions at perihelion
    r0 = a * (1 - e)
    x, y = r0, 0.0

    # Angular momentum: h = sqrt(GM·a·(1-e²))
    h = np.sqrt(GM * a * (1 - e**2))

    # Velocity at perihelion: v_phi = h/r0 (tangential)
    v_x, v_y = 0.0, h / r0

    # Track r values to find minima
    r_history = [r0]
    theta_history = [0.0]

    # Integrate for fixed number of steps (enough for n_orbits)
    n_steps = 500000  # Fixed limit
    perihelion_indices = []

    r_prev = r0
    for i in range(n_steps):
        r = np.sqrt(x**2 + y**2)
        theta = np.arctan2(y, x)

        # Refractive index and gradient
        n = 1.0 + rs / r if r > 1e-10 else 1.0
        dndx = -rs * x / (r**3) if r > 1e-10 else 0.0
        dndy = -rs * y / (r**3) if r > 1e-10 else 0.0

        # Geodesic equation
        v_dot_gradn = v_x * dndx + v_y * dndy
        ax = -c**2 * dndx / n + 2.0 * v_dot_gradn * v_x
        ay = -c**2 * dndy / n + 2.0 * v_dot_gradn * v_y

        # Update
        v_x += ax * dt
        v_y += ay * dt
        x += v_x * dt
        y += v_y * dt

        # Check for local minimum (perihelion)
        if len(r_history) >= 2:
            if r_history[-2] > r_history[-1] and r_history[-1] < r:
                # Found a minimum
                perihelion_indices.append(len(r_history) - 1)

        r_history.append(r)
        theta_history.append(theta)
        r_prev = r

        # Stop if we have enough perihelia
        if len(perihelion_indices) >= n_orbits + 1:
            break

        # Stop if particle escapes
        if r > 10 * a:
            break

    # Compute precession from perihelion angles
    if len(perihelion_indices) < 2:
        return None, None, None

    # Get angles at perihelia
    perihelion_angles = [theta_history[i] for i in perihelion_indices]

    # Unwrap angles (they should be increasing)
    for i in range(1, len(perihelion_angles)):
        while perihelion_angles[i] < perihelion_angles[i-1]:
            perihelion_angles[i] += 2 * np.pi

    # Angle between consecutive perihelia
    delta_thetas = np.diff(perihelion_angles)

    # Precession per orbit = delta_theta - 2π
    precessions = delta_thetas - 2 * np.pi
    delta_phi_measured = np.mean(precessions)

    # GR prediction
    delta_phi_gr = 6 * np.pi * GM / (a * (1 - e**2) * c**2)

    # Error
    if abs(delta_phi_gr) > 1e-10:
        error = abs(delta_phi_measured - delta_phi_gr) / abs(delta_phi_gr) * 100
    else:
        error = np.inf

    return delta_phi_measured, delta_phi_gr, error


def plot_orbit(a, e, n_orbits=3):
    """
    Plot the orbit in polar coordinates.
    """
    h = np.sqrt(a * (1 - e**2))
    mu = rs / 2
    
    r_min = a * (1 - e)
    u0 = 1.0 / r_min
    u0_dphi = 0.0
    
    phi_max = 2 * np.pi * n_orbits
    phi = np.linspace(0, phi_max, 50000)
    
    sol = odeint(orbit_equation, [u0, u0_dphi], phi, args=(mu, h))
    u = sol[:, 0]
    r = 1.0 / u
    
    # Convert to Cartesian
    x = r * np.cos(phi)
    y = r * np.sin(phi)
    
    return x, y, r, phi


def main():
    print("=" * 75)
    print("REFRACTIVE GRAVITY - PERIHELION PRECESSION VERIFICATION")
    print("=" * 75)
    print()
    print("Testing: Delta_phi = 6*pi*GM/(a(1-e^2)c^2) = 3*pi*rs/(a(1-e^2))")
    print(f"Schwarzschild radius: rs = {rs}")
    print()
    
    # Test cases: vary semi-major axis and eccentricity
    test_cases = [
        # (a, e, description)
        (20.0, 0.1, "Large circular-ish orbit"),
        (30.0, 0.1, "Larger orbit"),
        (50.0, 0.1, "Very large orbit"),
        (20.0, 0.3, "Moderate eccentricity"),
        (20.0, 0.5, "High eccentricity"),
        (100.0, 0.05, "Mercury-like (scaled)"),
    ]
    
    print(f"{'Case':>25} | {'GR Prediction':>14} | {'Simulation':>14} | {'Error':>10}")
    print("-" * 75)

    results = []
    for a, e, desc in test_cases:
        print(f"Testing: {desc} (a={a}, e={e})...")
        delta_phi_sim, delta_phi_gr, error = compute_precession_refractive(a, e, dt=0.05, n_orbits=1)
        print(f"  Result: sim={delta_phi_sim}, gr={delta_phi_gr}, error={error}")

        if delta_phi_sim is not None and delta_phi_gr is not None and error is not None:
            results.append((desc, a, e, delta_phi_gr, delta_phi_sim, error))
            print(f"{desc:>25} | {delta_phi_gr:>14.6f} | {delta_phi_sim:>14.6f} | {error:>9.2f}%")
        else:
            print(f"{desc:>25} | {delta_phi_gr if delta_phi_gr else 'N/A':>14} | {'N/A':>14} | {'N/A':>10}")
    
    print()
    print("=" * 75)
    
    # Summary statistics
    if results:
        errors = [r[5] for r in results if r[5] is not None]
        avg_error = np.mean(errors)
        max_error = np.max(errors)
        
        print(f"Average error: {avg_error:.2f}%")
        print(f"Maximum error: {max_error:.2f}%")
        print()
        
        if avg_error < 5.0:
            print("VERIFIED: Perihelion precession matches GR to within 5%")
        elif avg_error < 10.0:
            print("ACCEPTABLE: Perihelion precession matches GR to within 10%")
        else:
            print("WARNING: Discrepancy - check numerical integration")
    
    # Plot: Error vs 1/a (should be linear for small corrections)
    if results:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Plot 1: Precession vs 1/a
        a_vals = [r[1] for r in results]
        gr_vals = [r[3] for r in results]
        sim_vals = [r[4] for r in results]
        
        ax1.plot([1/a for a in a_vals], gr_vals, 'b-', label='GR Prediction', linewidth=2)
        ax1.plot([1/a for a in a_vals], sim_vals, 'ro', label='Simulation', markersize=8)
        ax1.set_xlabel('1/a (inverse semi-major axis)')
        ax1.set_ylabel('Precession per orbit (rad)')
        ax1.set_title('Perihelion Precession vs Orbit Size')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Error vs a
        errors = [r[5] for r in results]
        ax2.plot(a_vals, errors, 'g-', linewidth=2, marker='s', markersize=8)
        ax2.set_xlabel('Semi-major axis a')
        ax2.set_ylabel('Error (%)')
        ax2.set_title('Error vs Orbit Size')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('d:\\Fundamentals\\sandbox\\perihelion_precession.png', dpi=150)
        print("Plot saved: sandbox/perihelion_precession.png")
        plt.show()
    
    # Plot example orbit
    print()
    print("Generating example orbit plot...")
    x, y, r, phi = plot_orbit(a=20.0, e=0.3, n_orbits=3)
    
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.plot(x, y, 'b-', linewidth=1, label='Orbit')
    ax.plot(0, 0, 'ro', markersize=15, label='Central mass')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Precessing Orbit (a=20, e=0.3)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    plt.savefig('d:\\Fundamentals\\sandbox\\precessing_orbit.png', dpi=150)
    print("Orbit plot saved: sandbox/precessing_orbit.png")
    plt.show()


if __name__ == "__main__":
    main()
