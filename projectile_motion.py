# =============================================================================
# PROJECTILE MOTION SIMULATION
# =============================================================================
# Author      : Ved4nt5
# Date        : March 2026
# Language    : Python 3.10
# Libraries   : NumPy, Matplotlib
# Description : Simulates 5 modes of projectile motion, computes key
#               parameters, and shows a 2D animated projectile trajectory.
# =============================================================================

import numpy as np
import matplotlib
matplotlib.use('TkAgg')          # Use TkAgg backend for interactive window
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# -----------------------------------------------------------------------------
# CONSTANTS
# -----------------------------------------------------------------------------
g = 9.81  # Acceleration due to gravity (m/s²)

# =============================================================================
# FUNCTION: get_user_input()
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
# =============================================================================
def compute_trajectory(vx, vy, T):
    t = np.linspace(0, T, 200)
    x = vx * t
    y = vy * t - 0.5 * g * t**2
    return t, x, y

# =============================================================================
# FUNCTION: print_results(v0, angle_deg, T, H, R)
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

    # Set axis limits with padding
    ax.set_xlim(0, x[-1] * 1.05)
    ax.set_ylim(0, max(y) * 1.25)

    # Static reference: faint full trajectory in background
    ax.plot(x, y, color='royalblue', linewidth=1.5, linestyle='--', alpha=0.3,
            label='Full trajectory (reference)')

    # Mark launch, peak, and landing points
    ax.plot(0, 0, 'go', markersize=9, label='Launch (0, 0)')
    ax.plot(x[-1], 0, 'bs', markersize=9, label=f'Landing  R = {R:.2f} m')

    peak_idx = np.argmax(y)
    ax.plot(x[peak_idx], y[peak_idx], 'r^', markersize=9,
            label=f'Max Height  H = {H:.2f} m')
    ax.annotate(f'  H = {H:.2f} m',
                xy=(x[peak_idx], y[peak_idx]),
                fontsize=9, color='red')

    # Animated elements
    trail_line,     = ax.plot([], [], color='royalblue', linewidth=2.5, label='Path')
    projectile_dot, = ax.plot([], [], 'o', color='darkorange',
                               markersize=12, label='Projectile', zorder=5)

    # Live time counter
    time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes,
                        fontsize=10, color='dimgray', va='top')

    # Labels and formatting
    ax.set_title(f'Projectile Motion Animation\n(v₀ = {v0} m/s, θ = {angle_deg}°)',
                 fontsize=14, fontweight='bold')
    ax.set_xlabel('Horizontal Distance (m)', fontsize=12)
    ax.set_ylabel('Vertical Height (m)', fontsize=12)
    ax.legend(fontsize=9, loc='upper right')
    ax.grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()

    # -------------------------------------------------------------------------
    # INIT: clear animated objects
    # -------------------------------------------------------------------------
    def init():
        trail_line.set_data([], [])
        projectile_dot.set_data([], [])
        time_text.set_text('')
        return trail_line, projectile_dot, time_text

    # -------------------------------------------------------------------------
    # UPDATE: draw each frame
    # -------------------------------------------------------------------------
    def update(i):
        trail_line.set_data(x[:i+1], y[:i+1])
        projectile_dot.set_data([x[i]], [y[i]])
        time_text.set_text(f'Time: {t[i]:.2f} s')
        return trail_line, projectile_dot, time_text

    # Keep a reference to ani — required to prevent garbage collection
    ani = animation.FuncAnimation(
        fig, update,
        frames=len(x),
        init_func=init,
        interval=20,       # ms between frames
        blit=True,
        repeat=False
    )

    # Show the live animation window FIRST
    plt.show()

    # Save as GIF after window closes (requires Pillow: pip install pillow)
    save = input("\n  Save animation as GIF? (y/n): ").strip().lower()
    if save == 'y':
        try:
            print("  [INFO] Saving animation, please wait...")
            ani.save('projectile_animation.gif', writer='pillow', fps=50)
            print("  [INFO] Animation saved as 'projectile_animation.gif'")
        except Exception as e:
            print(f"  [WARNING] Could not save GIF: {e}")

    return ani   # return to prevent garbage collection if called from main

# =============================================================================
# FUNCTION: run_test_cases()
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

    # Validation note — fixed unpacking (was broken with splat operator)
    _, _, T30, H30, R30 = compute_parameters(50, 30)
    _, _, T60, H60, R60 = compute_parameters(50, 60)
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
# FUNCTION: show_menu()
# Displays the main menu and returns the user's choice.
# =============================================================================
def show_menu():
    print("\n" + "=" * 30)
    print("  PROJECTILE MOTION SIMULATOR")
    print("=" * 30)
    print("Select a simulation mode:")
    print("  1. Normal Projectile Motion")
    print("  2. Varying Gravity Projectile Motion")
    print("  3. Inclined Plane Projectile Motion")
    print("  4. Projectile Motion with Air Resistance")
    print("  5. Varying Mass Projectile Motion")
    print("-" * 30)
    return input("Enter choice (1-5): ").strip()

# =============================================================================
# MODE 1 — Normal Projectile Motion
# Wraps the existing interactive simulation (unchanged behaviour).
# =============================================================================
def mode1_normal():
    v0, angle_deg = get_user_input()
    vx, vy, T, H, R = compute_parameters(v0, angle_deg)
    print_results(v0, angle_deg, T, H, R)

    t, x, y = compute_trajectory(vx, vy, T)
    ani = animate_trajectory(x, y, t, v0, angle_deg, H, R)  # keep reference

    run_test = input("\n  Run predefined test cases? (y/n): ").strip().lower()
    if run_test == 'y':
        run_test_cases()
    return ani

# =============================================================================
# MODE 2 — Varying Gravity Projectile Motion
# Same as Mode 1 but lets the user supply a custom gravitational acceleration.
# =============================================================================
def mode2_varying_gravity():
    print("=" * 50)
    print("   VARYING GRAVITY PROJECTILE MOTION")
    print("=" * 50)
    v0      = float(input("Enter Initial Velocity (m/s)              : "))
    angle   = float(input("Enter Launch Angle (degrees)              : "))
    gravity = float(input("Enter Gravity (m/s²)  [default 9.81]      : ").strip() or "9.81")

    theta = np.radians(angle)
    vx    = v0 * np.cos(theta)
    vy    = v0 * np.sin(theta)
    T     = (2 * v0 * np.sin(theta)) / gravity
    H     = (v0**2 * np.sin(theta)**2) / (2 * gravity)
    R     = (v0**2 * np.sin(2 * theta)) / gravity

    print("\n" + "=" * 50)
    print("         SIMULATION RESULTS")
    print("=" * 50)
    print(f"  Initial Velocity   :  {v0:.2f} m/s")
    print(f"  Launch Angle       :  {angle:.2f}°")
    print(f"  Gravity            :  {gravity:.4f} m/s²")
    print("-" * 50)
    print(f"  Time of Flight     :  {T:.4f} s")
    print(f"  Maximum Height     :  {H:.4f} m")
    print(f"  Horizontal Range   :  {R:.4f} m")
    print("=" * 50)

    t_arr = np.linspace(0, T, 200)
    x_arr = vx * t_arr
    y_arr = vy * t_arr - 0.5 * gravity * t_arr**2
    ani   = animate_trajectory(x_arr, y_arr, t_arr, v0, angle, H, R)
    return ani

# =============================================================================
# MODE 3 — Inclined Plane Projectile Motion
# Projectile launched from an inclined surface. Computes range along the
# incline using the closed-form formula and animates with the slope drawn.
# =============================================================================
def mode3_inclined_plane():
    print("=" * 50)
    print("   INCLINED PLANE PROJECTILE MOTION")
    print("=" * 50)
    v0    = float(input("Enter Initial Velocity (m/s)                    : "))
    theta_deg = float(input("Enter Launch Angle from horizontal (degrees)   : "))
    alpha_deg = float(input("Enter Incline Angle (degrees)                  : "))

    theta_r = np.radians(theta_deg)
    alpha_r = np.radians(alpha_deg)

    # Guard: launch angle must be greater than incline angle for valid flight
    if theta_deg <= alpha_deg:
        print("  [ERROR] Launch angle must be greater than the incline angle.")
        return

    # Time of flight on inclined plane (closed-form)
    # T = 2 * v0 * sin(θ - α) / (g * cos(α))
    T         = (2 * v0 * np.sin(theta_r - alpha_r)) / (g * np.cos(alpha_r))
    # Range along the incline
    # R = 2 * v0² * cos(θ) * sin(θ - α) / (g * cos²(α))
    R_incline = (2 * v0**2 * np.cos(theta_r) * np.sin(theta_r - alpha_r)) / \
                (g * np.cos(alpha_r)**2)

    # Trajectory (standard kinematic equations from launch point)
    vx    = v0 * np.cos(theta_r)
    vy    = v0 * np.sin(theta_r)
    t_arr = np.linspace(0, T, 200)
    x_arr = vx * t_arr
    y_arr = vy * t_arr - 0.5 * g * t_arr**2
    H     = float(np.max(y_arr))      # max height above horizontal

    x_land = float(x_arr[-1])
    y_land = float(y_arr[-1])

    print("\n" + "=" * 50)
    print("         SIMULATION RESULTS")
    print("=" * 50)
    print(f"  Initial Velocity   :  {v0:.2f} m/s")
    print(f"  Launch Angle       :  {theta_deg:.2f}°")
    print(f"  Incline Angle      :  {alpha_deg:.2f}°")
    print("-" * 50)
    print(f"  Time of Flight     :  {T:.4f} s")
    print(f"  Maximum Height     :  {H:.4f} m  (above horizontal)")
    print(f"  Range along Incline:  {R_incline:.4f} m")
    print("=" * 50)

    # -------------------------------------------------------------------------
    # ANIMATION: inclined plane mode
    # -------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 5))

    # Draw inclined surface extending slightly past landing
    x_slope = np.linspace(0, x_land * 1.15, 100)
    y_slope = x_slope * np.tan(alpha_r)
    ax.plot(x_slope, y_slope, color='saddlebrown', linewidth=2.5,
            label=f'Incline  α = {alpha_deg:.1f}°')
    ax.fill_between(x_slope, y_slope, y2=-0.5, color='saddlebrown', alpha=0.15)

    ax.set_xlim(0, x_land * 1.15)
    ax.set_ylim(-0.5, H * 1.3)

    # Static reference trajectory
    ax.plot(x_arr, y_arr, color='royalblue', linewidth=1.5,
            linestyle='--', alpha=0.3, label='Full trajectory (reference)')

    # Key points
    ax.plot(0, 0, 'go', markersize=9, label='Launch (0, 0)')
    ax.plot(x_land, y_land, 'bs', markersize=9,
            label=f'Landing  R_incline = {R_incline:.2f} m')
    peak_idx = int(np.argmax(y_arr))
    ax.plot(x_arr[peak_idx], y_arr[peak_idx], 'r^', markersize=9,
            label=f'Max Height  H = {H:.2f} m')
    ax.annotate(f'  H = {H:.2f} m',
                xy=(x_arr[peak_idx], y_arr[peak_idx]), fontsize=9, color='red')

    # Animated elements
    trail_line,     = ax.plot([], [], color='royalblue', linewidth=2.5,
                               label='Path')
    projectile_dot, = ax.plot([], [], 'o', color='darkorange',
                               markersize=12, label='Projectile', zorder=5)
    time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes,
                        fontsize=10, color='dimgray', va='top')

    ax.set_title(
        f'Inclined Plane Projectile Motion\n'
        f'(v₀ = {v0} m/s, θ = {theta_deg}°, α = {alpha_deg}°)',
        fontsize=14, fontweight='bold')
    ax.set_xlabel('Horizontal Distance (m)', fontsize=12)
    ax.set_ylabel('Vertical Height (m)', fontsize=12)
    ax.legend(fontsize=9, loc='upper right')
    ax.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()

    def init():
        trail_line.set_data([], [])
        projectile_dot.set_data([], [])
        time_text.set_text('')
        return trail_line, projectile_dot, time_text

    def update(i):
        trail_line.set_data(x_arr[:i+1], y_arr[:i+1])
        projectile_dot.set_data([x_arr[i]], [y_arr[i]])
        time_text.set_text(f'Time: {t_arr[i]:.2f} s')
        return trail_line, projectile_dot, time_text

    ani = animation.FuncAnimation(
        fig, update, frames=len(x_arr),
        init_func=init, interval=20, blit=True, repeat=False
    )
    plt.show()

    save = input("\n  Save animation as GIF? (y/n): ").strip().lower()
    if save == 'y':
        try:
            print("  [INFO] Saving animation, please wait...")
            ani.save('inclined_animation.gif', writer='pillow', fps=50)
            print("  [INFO] Animation saved as 'inclined_animation.gif'")
        except Exception as e:
            print(f"  [WARNING] Could not save GIF: {e}")
    return ani

# =============================================================================
# MODE 4 — Projectile Motion with Air Resistance
# Uses Euler numerical integration with drag force opposing velocity.
# Prints a no-drag comparison and animates both trajectories.
# =============================================================================
def mode4_air_resistance():
    print("=" * 50)
    print("  PROJECTILE MOTION WITH AIR RESISTANCE")
    print("=" * 50)
    v0    = float(input("Enter Initial Velocity (m/s)               : "))
    angle = float(input("Enter Launch Angle (degrees)               : "))
    Cd    = float(input("Enter Drag Coefficient Cd  [default 0.47]  : ").strip() or "0.47")
    A     = float(input("Enter Cross-sectional Area (m²) [0.01]     : ").strip() or "0.01")
    m     = float(input("Enter Mass (kg)            [default 1.0]   : ").strip() or "1.0")
    rho   = float(input("Enter Air Density ρ (kg/m³)[default 1.225] : ").strip() or "1.225")

    theta_r  = np.radians(angle)
    vx_now   = v0 * np.cos(theta_r)
    vy_now   = v0 * np.sin(theta_r)

    # Euler integration with drag
    dt = 0.001
    xs, ys, ts = [0.0], [0.0], [0.0]

    while ys[-1] >= 0:
        v_mag  = np.sqrt(vx_now**2 + vy_now**2)
        F_drag = 0.5 * rho * Cd * A * v_mag**2
        if v_mag > 0:
            ax_ = -(F_drag / m) * (vx_now / v_mag)
            ay_ = -g - (F_drag / m) * (vy_now / v_mag)
        else:
            ax_, ay_ = 0.0, -g
        vx_now += ax_ * dt
        vy_now += ay_ * dt
        xs.append(xs[-1] + vx_now * dt)
        ys.append(ys[-1] + vy_now * dt)
        ts.append(ts[-1] + dt)
        if ts[-1] > 1000:   # safety break
            break

    x = np.array(xs)
    y = np.array(ys)
    t = np.array(ts)
    T = float(t[-1])
    H = float(np.max(y))
    R = float(x[-1])

    # No-drag reference (analytical)
    _, _, T_nd, H_nd, R_nd = compute_parameters(v0, angle)

    print("\n" + "=" * 50)
    print("         SIMULATION RESULTS")
    print("=" * 50)
    print(f"  Initial Velocity   :  {v0:.2f} m/s")
    print(f"  Launch Angle       :  {angle:.2f}°")
    print(f"  Drag Coefficient   :  {Cd:.4f}")
    print(f"  Area               :  {A:.4f} m²")
    print(f"  Mass               :  {m:.4f} kg")
    print(f"  Air Density        :  {rho:.4f} kg/m³")
    print("-" * 50)
    print(f"  Time of Flight     :  {T:.4f} s")
    print(f"  Maximum Height     :  {H:.4f} m")
    print(f"  Horizontal Range   :  {R:.4f} m")
    print("-" * 50)
    print("  [No-Drag Reference]")
    print(f"  Time of Flight     :  {T_nd:.4f} s")
    print(f"  Maximum Height     :  {H_nd:.4f} m")
    print(f"  Horizontal Range   :  {R_nd:.4f} m")
    print("=" * 50)

    # No-drag trajectory for overlay
    t_nd   = np.linspace(0, T_nd, 200)
    vx_nd  = v0 * np.cos(theta_r)
    vy_nd  = v0 * np.sin(theta_r)
    x_nd   = vx_nd * t_nd
    y_nd   = vy_nd * t_nd - 0.5 * g * t_nd**2

    # Downsample drag trajectory for smooth animation (~200 frames)
    stride = max(1, len(x) // 200)
    x_anim = x[::stride]
    y_anim = y[::stride]
    t_anim = t[::stride]

    # -------------------------------------------------------------------------
    # ANIMATION: air resistance mode
    # -------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlim(0, max(R_nd, R) * 1.1)
    ax.set_ylim(0, max(H_nd, H) * 1.3)

    # Static reference trajectories
    ax.plot(x, y, color='royalblue', linewidth=1.5,
            linestyle='--', alpha=0.3, label='With drag (reference)')
    ax.plot(x_nd, y_nd, color='tomato', linewidth=1.5,
            linestyle=':', alpha=0.4, label='No drag (reference)')

    ax.plot(0, 0, 'go', markersize=9, label='Launch (0, 0)')
    ax.plot(R, 0, 'bs', markersize=9, label=f'Landing (drag)  R = {R:.2f} m')
    ax.plot(R_nd, 0, 'r^', markersize=9,
            label=f'Landing (no drag)  R = {R_nd:.2f} m')
    peak_idx = int(np.argmax(y))
    ax.annotate(f'  H = {H:.2f} m',
                xy=(x[peak_idx], y[peak_idx]), fontsize=9, color='royalblue')

    trail_line,     = ax.plot([], [], color='royalblue', linewidth=2.5,
                               label='Path (drag)')
    projectile_dot, = ax.plot([], [], 'o', color='darkorange',
                               markersize=12, label='Projectile', zorder=5)
    time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes,
                        fontsize=10, color='dimgray', va='top')

    ax.set_title(
        f'Projectile Motion with Air Resistance\n'
        f'(v₀ = {v0} m/s, θ = {angle}°, Cd = {Cd})',
        fontsize=14, fontweight='bold')
    ax.set_xlabel('Horizontal Distance (m)', fontsize=12)
    ax.set_ylabel('Vertical Height (m)', fontsize=12)
    ax.legend(fontsize=9, loc='upper right')
    ax.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()

    def init():
        trail_line.set_data([], [])
        projectile_dot.set_data([], [])
        time_text.set_text('')
        return trail_line, projectile_dot, time_text

    def update(i):
        trail_line.set_data(x_anim[:i+1], y_anim[:i+1])
        projectile_dot.set_data([x_anim[i]], [y_anim[i]])
        time_text.set_text(f'Time: {t_anim[i]:.2f} s')
        return trail_line, projectile_dot, time_text

    ani = animation.FuncAnimation(
        fig, update, frames=len(x_anim),
        init_func=init, interval=20, blit=True, repeat=False
    )
    plt.show()

    save = input("\n  Save animation as GIF? (y/n): ").strip().lower()
    if save == 'y':
        try:
            print("  [INFO] Saving animation, please wait...")
            ani.save('air_resistance_animation.gif', writer='pillow', fps=50)
            print("  [INFO] Animation saved as 'air_resistance_animation.gif'")
        except Exception as e:
            print(f"  [WARNING] Could not save GIF: {e}")
    return ani

# =============================================================================
# MODE 5 — Varying Mass Projectile Motion
# Euler integration: thrust applied along launch direction during burn phase;
# ballistic flight after burn.  Multi-panel animation with live telemetry,
# colour-coded phase trails, exhaust-flame effect, and speed/mass sub-charts.
# =============================================================================
def mode5_varying_mass():
    # =========================================================================
    # INPUT — press Enter on any field to accept the shown default value
    # =========================================================================
    print("=" * 50)
    print("     VARYING MASS PROJECTILE MOTION")
    print("=" * 50)
    print("  Preset defaults (press Enter to accept):")
    print("    v₀=50 m/s  θ=75°  m₀=10 kg  ṁ=0.5 kg/s")
    print("    t_burn=5 s  F_thrust=150 N")
    print("-" * 50)
    v0       = float(input("Enter Initial Velocity (m/s)         [50]  : ").strip() or "50")
    angle    = float(input("Enter Launch Angle (degrees)         [75]  : ").strip() or "75")
    m0       = float(input("Enter Initial Mass m0 (kg)           [10]  : ").strip() or "10")
    dm_dt    = float(input("Enter Mass Loss Rate dm/dt (kg/s)   [0.5]  : ").strip() or "0.5")
    t_burn   = float(input("Enter Burn Duration t_burn (s)        [5]  : ").strip() or "5")
    F_thrust = float(input("Enter Thrust Force F_thrust (N)     [150]  : ").strip() or "150")

    # Warn when the fuel budget exceeds initial mass
    if dm_dt > 0 and dm_dt * t_burn >= m0:
        print(f"  [WARNING] dm/dt × t_burn = {dm_dt * t_burn:.2f} kg ≥ m₀ = {m0:.2f} kg.")
        print(f"            Burn will cut off automatically when mass → 0.")

    # =========================================================================
    # EULER INTEGRATION — track position, velocity, and mass at every step
    # =========================================================================
    theta_r  = np.radians(angle)
    vx_now   = v0 * np.cos(theta_r)
    vy_now   = v0 * np.sin(theta_r)

    dt = 0.001
    xs, ys, ts = [0.0], [0.0], [0.0]
    vxs, vys   = [vx_now], [vy_now]
    masses     = [m0]

    while ys[-1] >= 0:
        t_now = ts[-1]
        if t_now <= t_burn:
            # Burn phase: decreasing mass, thrust along launch direction
            mass = max(m0 - dm_dt * t_now, 1e-6)
            ax_  = (F_thrust * np.cos(theta_r)) / mass
            ay_  = -g + (F_thrust * np.sin(theta_r)) / mass
        else:
            # Ballistic phase: no thrust, constant residual mass
            mass = max(m0 - dm_dt * t_burn, 1e-6)
            ax_, ay_ = 0.0, -g

        vx_now += ax_ * dt
        vy_now += ay_ * dt
        xs.append(xs[-1] + vx_now * dt)
        ys.append(ys[-1] + vy_now * dt)
        ts.append(t_now + dt)
        vxs.append(vx_now)
        vys.append(vy_now)
        masses.append(mass)
        if ts[-1] > 1000:   # safety break
            break

    x        = np.array(xs)
    y        = np.array(ys)
    t        = np.array(ts)
    speeds   = np.sqrt(np.array(vxs)**2 + np.array(vys)**2)
    mass_arr = np.array(masses)

    T      = float(t[-1])
    H      = float(np.max(y))
    R      = float(x[-1])
    v_peak = float(np.max(speeds))

    # =========================================================================
    # PRINT RESULTS
    # =========================================================================
    print("\n" + "=" * 50)
    print("         SIMULATION RESULTS")
    print("=" * 50)
    print(f"  Initial Velocity   :  {v0:.2f} m/s")
    print(f"  Launch Angle       :  {angle:.2f}°")
    print(f"  Initial Mass       :  {m0:.2f} kg")
    print(f"  Mass Loss Rate     :  {dm_dt:.4f} kg/s")
    print(f"  Burn Duration      :  {t_burn:.2f} s")
    print(f"  Thrust Force       :  {F_thrust:.2f} N")
    print("-" * 50)
    print(f"  Time of Flight     :  {T:.4f} s")
    print(f"  Maximum Height     :  {H:.4f} m")
    print(f"  Horizontal Range   :  {R:.4f} m")
    print(f"  Peak Velocity      :  {v_peak:.4f} m/s")
    print("=" * 50)

    # =========================================================================
    # BUILD ANIMATION ARRAYS — downsample to ~300 frames for smooth playback
    # =========================================================================
    stride    = max(1, len(x) // 300)
    x_anim    = x[::stride]
    y_anim    = y[::stride]
    t_anim    = t[::stride]
    spd_anim  = speeds[::stride]
    mass_anim = mass_arr[::stride]
    n_frames  = len(x_anim)

    # Index in each array where the coast phase begins
    bi_full = int(np.searchsorted(t, t_burn))                          # full array index
    bi_a    = min(int(np.searchsorted(t_anim, t_burn)), n_frames - 1)  # animation array index

    # Exhaust-flame length: ~4.5 % of the larger plot dimension for clear visibility
    flame_scale = max(R, H) * 0.045

    # =========================================================================
    # FIGURE — 3-panel layout: trajectory (left) + speed & mass charts (right)
    # =========================================================================
    fig = plt.figure(figsize=(14, 8))
    gs  = fig.add_gridspec(2, 2, width_ratios=[2, 1], hspace=0.42, wspace=0.32)
    ax_traj = fig.add_subplot(gs[:, 0])   # full-height left panel: trajectory
    ax_vel  = fig.add_subplot(gs[0, 1])   # top-right: speed vs time
    ax_mass = fig.add_subplot(gs[1, 1])   # bottom-right: mass vs time

    fig.suptitle(
        f'Varying Mass Projectile Motion\n'
        f'v₀={v0} m/s  |  θ={angle}°  |  m₀={m0} kg  |  '
        f'ṁ={dm_dt} kg/s  |  t_burn={t_burn} s  |  F={F_thrust} N',
        fontsize=11, fontweight='bold'
    )

    # ─── Trajectory panel ────────────────────────────────────────────────────
    ax_traj.set_xlim(0, max(R * 1.08, 1.0))
    ax_traj.set_ylim(0, max(H * 1.30, 1.0))
    ax_traj.set_xlabel('Horizontal Distance (m)', fontsize=11)
    ax_traj.set_ylabel('Vertical Height (m)', fontsize=11)
    ax_traj.set_title('Trajectory', fontsize=11, fontweight='bold')
    ax_traj.grid(True, linestyle='--', alpha=0.5)

    # Faint full reference paths, colour-coded by phase
    ax_traj.plot(x[:bi_full+1], y[:bi_full+1],
                 color='orangered', linewidth=1.2, linestyle='--', alpha=0.22)
    ax_traj.plot(x[bi_full:],   y[bi_full:],
                 color='royalblue', linewidth=1.2, linestyle='--', alpha=0.22)

    # Key static markers
    ax_traj.plot(0, 0, 'go', markersize=9, label='Launch')
    ax_traj.plot(R, 0, 'bs', markersize=9, label=f'Landing  R = {R:.1f} m')
    peak_idx = int(np.argmax(y))
    ax_traj.plot(x[peak_idx], y[peak_idx], 'r^', markersize=9,
                 label=f'Apogee  H = {H:.1f} m')
    ax_traj.annotate(f' H = {H:.1f} m',
                     xy=(x[peak_idx], y[peak_idx]), fontsize=9, color='red')
    if bi_full < len(x):
        ax_traj.plot(x[bi_full], y[bi_full], 'y*', markersize=14, zorder=6,
                     label=f'Burn-out  t = {t_burn:.1f} s')
        ax_traj.annotate(' Burn-out',
                         xy=(x[bi_full], y[bi_full]), fontsize=8, color='goldenrod')
    ax_traj.legend(fontsize=8, loc='upper right')

    # Animated trajectory elements
    burn_trail,  = ax_traj.plot([], [], color='orangered', linewidth=2.5)
    coast_trail, = ax_traj.plot([], [], color='royalblue', linewidth=2.5)
    proj_dot,    = ax_traj.plot([], [], 'o', color='darkorange',
                                markersize=13, zorder=7)
    # Exhaust-flame plume (two overlapping lines: bright core + soft glow)
    flame_core, = ax_traj.plot([], [], '-', color='gold',
                               linewidth=4, alpha=0.90, zorder=6)
    flame_glow, = ax_traj.plot([], [], '-', color='orangered',
                               linewidth=8, alpha=0.40, zorder=5)

    # Live telemetry box (monospace for column alignment)
    tele_text = ax_traj.text(
        0.03, 0.38, '', transform=ax_traj.transAxes,
        fontsize=9, va='top', family='monospace',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow',
                  edgecolor='gray', alpha=0.88)
    )

    # ─── Speed panel ─────────────────────────────────────────────────────────
    ax_vel.set_xlim(0, T * 1.05)
    ax_vel.set_ylim(0, v_peak * 1.20)
    ax_vel.set_xlabel('Time (s)', fontsize=9)
    ax_vel.set_ylabel('Speed (m/s)', fontsize=9)
    ax_vel.set_title('Speed vs Time', fontsize=10, fontweight='bold')
    ax_vel.grid(True, linestyle='--', alpha=0.5)
    # Orange shading marks the burn zone
    ax_vel.axvspan(0, min(t_burn, T), alpha=0.09, color='orangered',
                   label='Burn zone')
    # Faint full-run reference curves
    ax_vel.plot(t[:bi_full+1], speeds[:bi_full+1],
                color='orangered', linewidth=1.0, alpha=0.22)
    ax_vel.plot(t[bi_full:], speeds[bi_full:],
                color='royalblue', linewidth=1.0, alpha=0.22)
    ax_vel.legend(fontsize=7, loc='upper right')
    # Animated: growing speed lines + current-position dot
    vel_burn_line,  = ax_vel.plot([], [], color='orangered', linewidth=1.8)
    vel_coast_line, = ax_vel.plot([], [], color='royalblue', linewidth=1.8)
    vel_dot,        = ax_vel.plot([], [], 'o', color='darkorange',
                                  markersize=7, zorder=5)

    # ─── Mass panel ──────────────────────────────────────────────────────────
    m_final = float(mass_arr[-1])
    ax_mass.set_xlim(0, T * 1.05)
    ax_mass.set_ylim(max(m_final * 0.82, 0), m0 * 1.12)
    ax_mass.set_xlabel('Time (s)', fontsize=9)
    ax_mass.set_ylabel('Mass (kg)', fontsize=9)
    ax_mass.set_title('Mass vs Time', fontsize=10, fontweight='bold')
    ax_mass.grid(True, linestyle='--', alpha=0.5)
    ax_mass.axvspan(0, min(t_burn, T), alpha=0.09, color='orangered')
    # Faint full-run reference curves
    ax_mass.plot(t[:bi_full+1], mass_arr[:bi_full+1],
                 color='orangered', linewidth=1.0, alpha=0.22)
    ax_mass.plot(t[bi_full:], mass_arr[bi_full:],
                 color='steelblue',  linewidth=1.0, alpha=0.22)
    # Animated: growing mass lines + current-position dot
    mass_burn_line,  = ax_mass.plot([], [], color='orangered', linewidth=1.8)
    mass_coast_line, = ax_mass.plot([], [], color='steelblue',  linewidth=1.8)
    mass_dot,        = ax_mass.plot([], [], 'o', color='darkorange',
                                    markersize=7, zorder=5)

    plt.tight_layout(rect=[0, 0, 1, 0.93])   # leave room for suptitle

    # =========================================================================
    # ANIMATION CALLBACKS
    # blit=False is required here: blit=True only redraws one axis's background,
    # so artists on the velocity and mass sub-panels would not update correctly.
    # =========================================================================
    def init():
        burn_trail.set_data([], [])
        coast_trail.set_data([], [])
        proj_dot.set_data([], [])
        flame_core.set_data([], [])
        flame_glow.set_data([], [])
        tele_text.set_text('')
        vel_burn_line.set_data([], [])
        vel_coast_line.set_data([], [])
        vel_dot.set_data([], [])
        mass_burn_line.set_data([], [])
        mass_coast_line.set_data([], [])
        mass_dot.set_data([], [])
        return (burn_trail, coast_trail, proj_dot, flame_core, flame_glow,
                tele_text, vel_burn_line, vel_coast_line, vel_dot,
                mass_burn_line, mass_coast_line, mass_dot)

    def update(i):
        t_now    = t_anim[i]
        x_now    = x_anim[i]
        y_now    = y_anim[i]
        spd_now  = spd_anim[i]
        mass_now = mass_anim[i]
        in_burn  = (t_now <= t_burn)

        # ── Colour-coded trajectory trails ──
        if i <= bi_a:
            burn_trail.set_data(x_anim[:i+1],     y_anim[:i+1])
            coast_trail.set_data([], [])
        else:
            burn_trail.set_data(x_anim[:bi_a+1],   y_anim[:bi_a+1])
            coast_trail.set_data(x_anim[bi_a:i+1], y_anim[bi_a:i+1])

        # ── Projectile dot (colour flips with phase) ──
        proj_dot.set_data([x_now], [y_now])
        proj_dot.set_markerfacecolor('orangered' if in_burn else 'royalblue')

        # ── Exhaust-flame plume (only visible during burn) ──
        if in_burn and flame_scale > 0:
            fx = x_now - flame_scale * np.cos(theta_r)
            fy = y_now - flame_scale * np.sin(theta_r)
            flame_core.set_data([x_now, fx], [y_now, fy])
            flame_glow.set_data([x_now, fx], [y_now, fy])
        else:
            flame_core.set_data([], [])
            flame_glow.set_data([], [])

        # ── Live telemetry box ──
        # Trailing space on 'BURN ' keeps both labels at 5 chars so the
        # monospace columns stay aligned regardless of phase.
        phase_str = 'BURN ' if in_burn else 'COAST'
        tele_text.set_text(
            f'Phase  : {phase_str}\n'
            f'Time   : {t_now:>6.2f} s\n'
            f'Speed  : {spd_now:>6.1f} m/s\n'
            f'Alt    : {y_now:>6.1f} m\n'
            f'Mass   : {mass_now:>6.2f} kg'
        )
        # Box background colour flips with phase
        bbox_patch = tele_text.get_bbox_patch()
        if bbox_patch is not None:
            bbox_patch.set_facecolor('#ffe8d6' if in_burn else '#d6e8ff')

        # ── Speed subplot: growing lines + dot ──
        if i <= bi_a:
            vel_burn_line.set_data(t_anim[:i+1],     spd_anim[:i+1])
            vel_coast_line.set_data([], [])
        else:
            vel_burn_line.set_data(t_anim[:bi_a+1],   spd_anim[:bi_a+1])
            vel_coast_line.set_data(t_anim[bi_a:i+1], spd_anim[bi_a:i+1])
        vel_dot.set_data([t_now], [spd_now])

        # ── Mass subplot: growing lines + dot ──
        if i <= bi_a:
            mass_burn_line.set_data(t_anim[:i+1],     mass_anim[:i+1])
            mass_coast_line.set_data([], [])
        else:
            mass_burn_line.set_data(t_anim[:bi_a+1],   mass_anim[:bi_a+1])
            mass_coast_line.set_data(t_anim[bi_a:i+1], mass_anim[bi_a:i+1])
        mass_dot.set_data([t_now], [mass_now])

        return (burn_trail, coast_trail, proj_dot, flame_core, flame_glow,
                tele_text, vel_burn_line, vel_coast_line, vel_dot,
                mass_burn_line, mass_coast_line, mass_dot)

    ani = animation.FuncAnimation(
        fig, update, frames=n_frames,
        init_func=init, interval=20, blit=False, repeat=False
    )
    plt.show()

    save = input("\n  Save animation as GIF? (y/n): ").strip().lower()
    if save == 'y':
        try:
            print("  [INFO] Saving animation, please wait...")
            ani.save('varying_mass_animation.gif', writer='pillow', fps=50)
            print("  [INFO] Animation saved as 'varying_mass_animation.gif'")
        except Exception as e:
            print(f"  [WARNING] Could not save GIF: {e}")
    return ani

# =============================================================================
# MAIN — Entry Point
# =============================================================================
def main():
    choice = show_menu()
    if choice == '1':
        mode1_normal()
    elif choice == '2':
        mode2_varying_gravity()
    elif choice == '3':
        mode3_inclined_plane()
    elif choice == '4':
        mode4_air_resistance()
    elif choice == '5':
        mode5_varying_mass()
    else:
        print(f"  [ERROR] Invalid choice '{choice}'. Please enter 1–5.")

if __name__ == "__main__":
    main()