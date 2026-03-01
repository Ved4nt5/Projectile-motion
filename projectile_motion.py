# =============================================================================
# PROJECTILE MOTION SIMULATION
# =============================================================================
# Author      : Ved4nt5
# Date        : March 2026
# Language    : Python 3.10
# Libraries   : NumPy, Matplotlib
# Description : Simulates projectile motion, computes key parameters,
#               and shows a 2D animated projectile flying along its trajectory.
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as mpatches

# -----------------------------------------------------------------------------
# CONSTANTS
# -----------------------------------------------------------------------------
g = 9.81  # Acceleration due to gravity (m/s²)

# =============================================================================
# FUNCTION: get_user_input()
# Prompts the user for initial velocity and launch angle.
# =============================================================================
def get_user_input():
    print("=" * 50)
    print("      PROJECTILE MOTION SIMULATION")
    print("=" * 50)
    v0    = float(input("Enter Initial Velocity (m/s)  : "))
    angle = float(input("Enter Launch Angle (degrees)  : "))
    return v0, angle

# =============================================================================
# FUNCTION: compute_parameters(v0, angle_deg)
# Converts angle to radians, computes velocity components,
# time of flight, maximum height, and range.
# =============================================================================
def compute_parameters(v0, angle_deg):
    theta = np.radians(angle_deg)
    vx = v0 * np.cos(theta)
    vy = v0 * np.sin(theta)
    T  = (2 * v0 * np.sin(theta)) / g
    H  = (v0**2 * np.sin(theta)**2) / (2 * g)
    R  = (v0**2 * np.sin(2 * theta)) / g
    return vx, vy, T, H, R

# =============================================================================
# FUNCTION: compute_trajectory(vx, vy, T)
# Generates 200 time points and computes x(t) and y(t) arrays.
# =============================================================================
def compute_trajectory(vx, vy, T):
    t = np.linspace(0, T, 200)
    x = vx * t
    y = vy * t - 0.5 * g * t**2
    return t, x, y

# =============================================================================
# FUNCTION: print_results(v0, angle_deg, T, H, R)
# Prints the computed parameters to the console in formatted style.
# =============================================================================
def print_results(v0, angle_deg, T, H, R):
    print("\n" + "=" * 50)
    print("         SIMULATION RESULTS")
    print("=" * 50)
    print(f"  Initial Velocity   :  {v0:.2f} m/s")
    print(f"  Launch Angle       :  {angle_deg:.2f}°")
    print("-" * 50)
    print(f"  Time of Flight     :  {T:.4f} s")
    print(f"  Maximum Height     :  {H:.4f} m")
    print(f"  Horizontal Range   :  {R:.4f} m")
    print("=" * 50)

# =============================================================================
# FUNCTION: animate_trajectory(x, y, t, v0, angle_deg, H, R)
# Animates the projectile flying along its parabolic path.
# =============================================================================
def animate_trajectory(x, y, t, v0, angle_deg, H, R):
    fig, ax = plt.subplots(figsize=(10, 5))

    # Set axis limits with a little padding
    ax.set_xlim(0, x[-1] * 1.05)
    ax.set_ylim(0, max(y) * 1.25)

    # Static reference: faint full trajectory in background
    ax.plot(x, y, color='royalblue', linewidth=1.5, linestyle='--', alpha=0.3,
            label='Full trajectory (reference)')

    # Mark launch and landing points
    ax.plot(0, 0, 'go', markersize=9, label='Launch (0, 0)')
    ax.plot(x[-1], 0, 'bs', markersize=9, label=f'Landing  R = {R:.2f} m')

    # Mark the peak
    peak_idx = np.argmax(y)
    ax.plot(x[peak_idx], y[peak_idx], 'r^', markersize=9,
            label=f'Max Height  H = {H:.2f} m')
    ax.annotate(f'  H = {H:.2f} m',
                xy=(x[peak_idx], y[peak_idx]),
                fontsize=9, color='red')

    # Animated elements
    trail_line, = ax.plot([], [], color='royalblue', linewidth=2.5, label='Path')
    projectile_dot, = ax.plot([], [], 'o', color='darkorange',
                              markersize=12, label='Projectile', zorder=5)

    # Time label in the upper-left corner
    time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes,
                        fontsize=10, color='dimgray', va='top')

    # Labels and formatting
    ax.set_title(f'Projectile Motion Animation\n(v₀ = {v0} m/s, θ = {angle_deg}°)',
                 fontsize=14, fontweight='bold')
    ax.set_xlabel('Horizontal Distance (m)', fontsize=12)
    ax.set_ylabel('Vertical Height (m)', fontsize=12)
    ax.legend(fontsize=9, loc='upper right')
    ax.grid(True, linestyle='--', alpha=0.6)

    # -------------------------------------------------------------------------
    # INIT: clear the animated objects
    # -------------------------------------------------------------------------
    def init():
        trail_line.set_data([], [])
        projectile_dot.set_data([], [])
        time_text.set_text('')
        return trail_line, projectile_dot, time_text

    # -------------------------------------------------------------------------
    # UPDATE: called for each frame i
    # -------------------------------------------------------------------------
    def update(i):
        trail_line.set_data(x[:i+1], y[:i+1])
        projectile_dot.set_data([x[i]], [y[i]])
        time_text.set_text(f'Time: {t[i]:.2f} s')
        return trail_line, projectile_dot, time_text

    # interval in ms between frames (total ~3 s for 200 frames → 15 ms each)
    ani = animation.FuncAnimation(
        fig, update,
        frames=len(x),
        init_func=init,
        interval=15,
        blit=True,
        repeat=False
    )

    plt.tight_layout()

    # Save as GIF (requires Pillow) — comment out if not needed
    try:
        ani.save('projectile_animation.gif', writer='pillow', fps=60)
        print("\n  [INFO] Animation saved as 'projectile_animation.gif'")
    except Exception as e:
        print(f"\n  [WARNING] Could not save GIF: {e}")

    plt.show()

# =============================================================================
# FUNCTION: run_test_cases()
# Runs predefined test cases for validation (static multi-trajectory plot).
# =============================================================================
def run_test_cases():
    print("\n" + "=" * 50)
    print("         TEST CASES — VALIDATION")
    print("=" * 50)

    test_cases = [
        (50, 45, "Maximum Range"),
        (50, 30, "Complementary Angle A"),
        (50, 60, "Complementary Angle B"),
    ]

    fig, ax = plt.subplots(figsize=(12, 6))
    colors = ['royalblue', 'tomato', 'seagreen']

    for i, (v0, angle, label) in enumerate(test_cases):
        vx, vy, T, H, R = compute_parameters(v0, angle)
        t, x, y = compute_trajectory(vx, vy, T)

        print(f"\n  [{label}]  v₀ = {v0} m/s,  θ = {angle}°")
        print(f"  Time of Flight   : {T:.4f} s")
        print(f"  Maximum Height   : {H:.4f} m")
        print(f"  Horizontal Range : {R:.4f} m")

        ax.plot(x, y, color=colors[i], linewidth=2.2,
                label=f'θ = {angle}°  |  R = {R:.2f} m  |  H = {H:.2f} m')

    # Validation note
    _, _, T30, H30, R30 = compute_parameters(50, 30), *compute_parameters(50, 30)[2:]
    _, _, T60, H60, R60 = compute_parameters(50, 60), *compute_parameters(50, 60)[2:]
    print("\n" + "-" * 50)
    print(f"  ✅ Range @ 30°  =  {R30:.4f} m")
    print(f"  ✅ Range @ 60°  =  {R60:.4f} m")
    if abs(R30 - R60) < 0.01:
        print("  ✅ VALIDATED: Complementary angles produce equal range!")
    print("=" * 50)

    ax.set_title('Projectile Motion — Test Cases (v₀ = 50 m/s)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Horizontal Distance (m)', fontsize=12)
    ax.set_ylabel('Vertical Height (m)', fontsize=12)
    ax.legend(fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)

    plt.tight_layout()
    plt.savefig('test_cases.png', dpi=150, bbox_inches='tight')
    plt.show()
    print("  [INFO] Test case plot saved as 'test_cases.png'")

# =============================================================================
# MAIN — Entry Point
# =============================================================================
def main():
    # --- Interactive Simulation ---
    v0, angle_deg = get_user_input()

    # Compute parameters
    vx, vy, T, H, R = compute_parameters(v0, angle_deg)

    # Print results
    print_results(v0, angle_deg, T, H, R)

    # Compute trajectory and show animation
    t, x, y = compute_trajectory(vx, vy, T)
    animate_trajectory(x, y, t, v0, angle_deg, H, R)

    # --- Run Test Cases ---
    run_test = input("\n  Run predefined test cases? (y/n): ").strip().lower()
    if run_test == 'y':
        run_test_cases()

if __name__ == "__main__":
    main()