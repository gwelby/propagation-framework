import numpy as np
import matplotlib.pyplot as plt

def refractive_index(r, rs=1.0):
    """Gordian Metric: n(r) = exp(rs / r)"""
    return np.exp(rs / r)

def visualize_orbits():
    # 1. Setup the field
    grid_size = 500
    x = np.linspace(-10, 10, grid_size)
    y = np.linspace(-10, 10, grid_size)
    X, Y = np.meshgrid(x, y)
    R = np.sqrt(X**2 + Y**2)
    R[R < 0.5] = 0.5 # Avoid singularity at center
    
    N = refractive_index(R)
    
    # 2. Define the Three Generations (Harmonic Radii)
    # Ratios from Koide and Top/Tau findings
    # Gen 1 is the "Seed", Gen 2 is "Symmetry", Gen 3 is the "Limit"
    radii = [8.0, 3.5, 1.2] # Arbitrary but proportional to the energy scales
    colors = ['#00FFCC', '#FFCC00', '#FF3366'] # Cyan (Light), Gold (Mid), Magenta (High)
    labels = ['Gen 1: The Seed', 'Gen 2: Symmetry', 'Gen 3: The Limit']
    
    fig, ax = plt.subplots(figsize=(12, 12), facecolor='#0A0A0A')
    ax.set_facecolor('#0A0A0A')
    
    # Plot the refractive field (The Medium)
    im = ax.imshow(N, extent=[-10, 10, -10, 10], origin='lower', cmap='magma', alpha=0.6)
    
    # Plot the Phase-Locked Orbits
    theta = np.linspace(0, 2*np.pi, 1000)
    for r, color, label in zip(radii, colors, labels):
        # Add "Wave interference" patterns to the orbits
        # Frequency increases with depth (towards center)
        freq = 15.0 / r 
        phase_wave = 0.2 * np.sin(freq * theta)
        orbit_x = (r + phase_wave) * np.cos(theta)
        orbit_y = (r + phase_wave) * np.sin(theta)
        
        ax.plot(orbit_x, orbit_y, color=color, linewidth=2, label=label, alpha=0.9)
        # Add a glow effect
        for i in range(1, 5):
            ax.plot(orbit_x, orbit_y, color=color, linewidth=2 + i*2, alpha=0.1)

    # 3. The Coherence Ceiling (The Barrier)
    ceiling_r = 0.8
    circle = plt.Circle((0, 0), ceiling_r, color='white', fill=False, linestyle='--', linewidth=2, label='Coherence Ceiling')
    ax.add_patch(circle)
    
    # Textual Annotations in LUMEN style
    ax.text(-9.5, 9, "Gordian Metric: n(r) = exp(rs/r)", color='white', fontsize=12, family='monospace')
    ax.text(-9.5, 8.2, "⦿ → ∇ → Σ(3) → ⚡", color='cyan', fontsize=14, family='monospace')
    ax.text(ceiling_r + 0.2, 0.2, "Duck Limit: Phase Incoherence", color='white', fontsize=10, style='italic')

    # Styling
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.axis('off')
    ax.legend(loc='lower right', facecolor='#1A1A1A', edgecolor='white', labelcolor='white')
    
    plt.title("Propagation Framework: The Three-Stage Harmonic Orbits", color='white', fontsize=18, pad=20)
    plt.tight_layout()
    
    output_path = 'sandbox/refractive_gravity_orbits.png'
    plt.savefig(output_path, dpi=150, facecolor='#0A0A0A')
    print(f"Visualization rendered: {output_path}")

if __name__ == "__main__":
    visualize_orbits()
