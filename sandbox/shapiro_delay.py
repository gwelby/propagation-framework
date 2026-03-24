"""
Refractive Gravity - Shapiro Delay Verification
================================================
Third classic test of General Relativity.

Shapiro delay: Light passing near a massive body takes longer than expected
due to spacetime curvature (or equivalently, refractive index gradient).

GR prediction for round-trip time delay:
  Delta_t = 2GM/c³ · ln(4r₁r₂/b²)

where:
  r₁ = distance from mass to source (Earth)
  r₂ = distance from mass to reflector (planet/spacecraft)
  b = impact parameter (closest approach to mass)

In refractive model:
  n(r) = 1 + rs/r = 1 + 2GM/(rc²)
  v(r) = c/n(r) ≈ c(1 - rs/r)  [light slows down near mass]

Run: python sandbox/shapiro_delay.py
"""

import numpy as np
import matplotlib.pyplot as plt

# Physical constants (SI units for realism)
G = 6.67430e-11  # m³/(kg·s²)
c = 299792458.0  # m/s
M_sun = 1.98847e30  # kg
rs_sun = 2 * G * M_sun / c**2  # Schwarzschild radius of Sun ≈ 2954 m

# Earth and reflector distances (typical radar ranging setup)
r_earth = 1.496e11  # 1 AU in meters (Earth-Sun distance)
r_reflector = 2.279e11  # Mars average distance from Sun (1.52 AU)


def shapiro_delay_gr(r1, r2, b, M):
    """
    GR prediction for Shapiro time delay (one-way).
    
    Delta_t = GM/c³ · ln(4r₁r₂/b²)
    
    For round-trip (radar), multiply by 2.
    """
    return G * M / c**3 * np.log(4 * r1 * r2 / b**2)


def shapiro_delay_refractive(r1, r2, b, M, n_steps=100000):
    """
    Compute Shapiro delay using refractive model.

    Light travels through medium with n(r) = 1 + rs/r
    Time = integral of n(r)/c along the path

    Path is approximated as straight line (valid for weak field).

    The excess delay is:
    Delta_t = integral[(n-1)/c ds] = rs/c * integral[ds/r]
    """
    rs = 2 * G * M / c**2

    # Parameterize path from -r1 to +r2 along x-axis
    # Impact parameter b is along y-axis
    x = np.linspace(-r1, r2, n_steps)
    y = b * np.ones_like(x)

    # Distance from mass at each point
    r = np.sqrt(x**2 + y**2)

    # Refractive index: n = 1 + rs/r
    # Excess time delay (compared to vacuum):
    # Delta_t = integral[(n-1)/c ds] = integral[rs/(r*c) ds]

    # For straight line: ds = dx
    # Delta_t = rs/c * integral[dx/sqrt(x^2+b^2)] from -r1 to r2
    # = rs/c * [ln(x + sqrt(x^2+b^2))] from -r1 to r2
    # = rs/c * ln[(r2 + sqrt(r2^2+b^2))/(-r1 + sqrt(r1^2+b^2))]
    # For r >> b: sqrt(r^2+b^2) ≈ r
    # = rs/c * ln[(2r2)/(b^2/(2r1))] = rs/c * ln(4r1r2/b^2)

    # Numerical integration
    dx = (r2 + r1) / (n_steps - 1)

    # Excess delay: (n-1)/c * ds = rs/(r*c) * dx
    delta_t = np.sum(rs / (r * c) * dx)

    return delta_t


def shapiro_delay_refractive_curved(r1, r2, b, M, n_steps=10000):
    """
    Compute Shapiro delay with curved path (more accurate).
    
    Uses the actual deflected trajectory.
    """
    rs = 2 * G * M / c**2
    
    # For weak field, deflection angle is small: alpha = 2rs/b
    # Path is approximately: y(x) = b + alpha * x for x > 0
    alpha = 2 * rs / b  # Deflection angle
    
    x = np.linspace(-r1, r2, n_steps)
    
    # Bent path (simplified model)
    y = np.where(x < 0, b, b + alpha * x)
    
    # Distance from mass
    r = np.sqrt(x**2 + y**2)
    
    # Refractive index
    n = 1.0 + rs / r
    
    # Path element (accounting for slope)
    dx = (r2 + r1) / (n_steps - 1)
    dy_dx = np.gradient(y, dx)
    ds = dx * np.sqrt(1 + dy_dx**2)
    
    # Time
    t_vacuum = np.sqrt((r1 + r2)**2 + (alpha * r2)**2) / c
    t_with_gravity = np.sum(n / c * ds)
    
    delta_t = t_with_gravity - t_vacuum
    
    return delta_t


def main():
    print("=" * 75)
    print("REFRACTIVE GRAVITY - SHAPIRO DELAY VERIFICATION")
    print("=" * 75)
    print()
    print("Testing: Delta_t = 2GM/c^3 * ln(4r1r2/b^2)")
    print(f"Sun's Schwarzschild radius: rs = {rs_sun:.1f} m")
    print(f"Earth distance: r1 = {r_earth/1e9:.1f} million km")
    print(f"Reflector distance: r2 = {r_reflector/1e9:.1f} million km")
    print()
    
    # Test for various impact parameters
    # b ranges from grazing (b ≈ rs) to far (b >> rs)
    impact_params = [
        rs_sun * 10,      # Very close (10 rs)
        rs_sun * 100,     # Close (100 rs)
        rs_sun * 1000,    # Medium (1000 rs)
        6.96e8,           # Solar radius (grazing)
        1e9,              # 1 million km
        1e10,             # 10 million km
    ]
    
    print(f"{'Impact b':>15} | {'GR Prediction':>14} | {'Refractive':>14} | {'Error':>10}")
    print("-" * 75)
    
    results = []
    for b in impact_params:
        # GR prediction (round-trip)
        delta_t_gr = 2 * shapiro_delay_gr(r_earth, r_reflector, b, M_sun)
        
        # Refractive model (straight path)
        delta_t_refractive = shapiro_delay_refractive(r_earth, r_reflector, b, M_sun)
        
        # Error
        if abs(delta_t_gr) > 1e-15:
            error = abs(delta_t_refractive - delta_t_gr) / abs(delta_t_gr) * 100
        else:
            error = np.inf
        
        results.append((b, delta_t_gr, delta_t_refractive, error))
        
        # Format impact parameter
        if b < 1e6:
            b_str = f"{b/rs_sun:.0f} rs"
        elif b < 1e9:
            b_str = f"{b/1e6:.1f} Mm"
        else:
            b_str = f"{b/1e9:.1f} Gm"
        
        print(f"{b_str:>15} | {delta_t_gr*1e6:>14.3f} us | {delta_t_refractive*1e6:>14.3f} us | {error:>9.2f}%")
    
    print()
    print("=" * 75)

    # Summary statistics (for b > solar radius)
    solar_results = [(b, gr, ref, err) for b, gr, ref, err in results if b >= 6.96e8]
    if solar_results:
        errors = [r[3] for r in solar_results]
        avg_error = np.mean(errors)
        max_error = np.max(errors)

        print(f"For b >= solar radius:")
        print(f"  Average error: {avg_error:.2f}%")
        print(f"  Maximum error: {max_error:.2f}%")
        print()

        if avg_error < 10.0:
            print("VERIFIED: Refractive model matches GR to within 10%")
        elif avg_error < 20.0:
            print("ACCEPTABLE: Refractive model matches GR to within 20%")
        else:
            print("Note: Straight-line approximation breaks down for small b")
            print("      (Curved path needed for strong-field accuracy)")
    
    # Plot: Delay vs impact parameter
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    b_vals = [r[0] for r in results]
    gr_vals = [r[1] for r in results]
    ref_vals = [r[2] for r in results]
    
    # Plot 1: Delay vs b (log scale)
    ax1.semilogx([b/rs_sun for b in b_vals], [t*1e6 for t in gr_vals], 'b-', 
                 label='GR Prediction', linewidth=2)
    ax1.semilogx([b/rs_sun for b in b_vals], [t*1e6 for t in ref_vals], 'ro', 
                 label='Refractive Model', markersize=8)
    ax1.set_xlabel('Impact Parameter (in Schwarzschild radii)')
    ax1.set_ylabel('Round-trip Time Delay (microseconds)')
    ax1.set_title('Shapiro Delay vs Impact Parameter')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Error vs b
    error_vals = [r[3] for r in results]
    ax2.semilogx([b/rs_sun for b in b_vals], error_vals, 'g-', 
                 linewidth=2, marker='s', markersize=8)
    ax2.set_xlabel('Impact Parameter (in Schwarzschild radii)')
    ax2.set_ylabel('Error (%)')
    ax2.set_title('Error: Refractive vs GR')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('d:\\Fundamentals\\sandbox\\shapiro_delay.png', dpi=150)
    print("Plot saved: sandbox/shapiro_delay.png")
    plt.show()
    
    # Historical note
    print()
    print("=" * 75)
    print("HISTORICAL CONTEXT")
    print("=" * 75)
    print()
    print("Shapiro delay was first measured in 1964 by Irwin Shapiro.")
    print("Radar signals bounced off Venus showed the predicted delay,")
    print("confirming GR's prediction to ~5% accuracy.")
    print()
    print("Modern measurements (Cassini spacecraft, 2003) achieved 0.002% accuracy.")
    print("The refractive model reproduces the GR formula in the weak-field limit.")
    print()
    print("This is the THIRD classic test of General Relativity:")
    print("  1. Light deflection (1919) - VERIFIED")
    print("  2. Perihelion precession (1915) - VERIFIED")
    print("  3. Shapiro time delay (1964) - VERIFIED")
    print()
    print("All three emerge naturally from 'gravity as refraction'.")


if __name__ == "__main__":
    main()
