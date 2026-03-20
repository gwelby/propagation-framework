import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def simulate_movie_orbits():
    fig, ax = plt.subplots(figsize=(10, 10), facecolor='#000000')
    ax.set_facecolor('#000000')
    
    # 1. Background Refractive Density
    grid_res = 200
    x = np.linspace(-10, 10, grid_res)
    y = np.linspace(-10, 10, grid_res)
    X, Y = np.meshgrid(x, y)
    R = np.sqrt(X**2 + Y**2)
    R[R < 0.5] = 0.5
    N = np.exp(1.0 / R)
    
    ax.imshow(N, extent=[-10, 10, -10, 10], cmap='magma', alpha=0.4, origin='lower')
    
    # 2. Particle Wavefronts
    particles = [
        {'r': 8.0, 'color': '#00FFCC', 'freq': 1.0, 'trail': []}, # Gen 1
        {'r': 4.0, 'color': '#FFCC00', 'freq': 2.0, 'trail': []}, # Gen 2
        {'r': 1.5, 'color': '#FF3366', 'freq': 4.0, 'trail': []}  # Gen 3
    ]
    
    plots = [ax.plot([], [], color=p['color'], lw=2, alpha=0.9)[0] for p in particles]
    points = [ax.plot([], [], 'o', color=p['color'], markersize=8)[0] for p in particles]
    
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.axis('off')

    def init():
        for line, pt in zip(plots, points):
            line.set_data([], [])
            pt.set_data([], [])
        return plots + points

    def animate(i):
        t = i / 20.0
        for idx, p in enumerate(particles):
            theta = p['freq'] * t
            
            # The "Wobble" (Critical Slowing Down)
            wobble_amp = 0.05 * (p['freq'] ** 1.5)
            wobble = wobble_amp * np.sin(10 * t)
            
            curr_r = p['r'] + wobble
            px = curr_r * np.cos(theta)
            py = curr_r * np.sin(theta)
            
            p['trail'].append((px, py))
            if len(p['trail']) > 50:
                p['trail'].pop(0)
            
            tx, ty = zip(*p['trail'])
            plots[idx].set_data(tx, ty)
            points[idx].set_data([px], [py])
            
        return plots + points

    ani = animation.FuncAnimation(fig, animate, frames=200, init_func=init, interval=50, blit=True)
    
    output_path = 'sandbox/propagation_movie_raw.gif'
    print(f"Generating movie frames for {output_path}...")
    ani.save(output_path, writer='pillow', fps=20)
    print(f"Raw Footage Generated: {output_path}")

if __name__ == "__main__":
    simulate_movie_orbits()
