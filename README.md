# Projectile Motion Simulation
### A Physics Project in Python

**Author:** Ved4nt5
**Date:** March 2026
**Language:** Python 3.10
**Tools:** NumPy · Matplotlib · Jupyter Notebook

---

## Table of Contents
1. [Introduction](#introduction)
2. [Libraries Used](#libraries-used)
3. [Working / Algorithm](#working--algorithm)
4. [Formulas](#formulas)
5. [Output Requirements](#output-requirements)
6. [Testing Section](#testing-section)
7. [Discussion](#discussion)
8. [Conclusion](#conclusion)
9. [References](#references)

---

## 1. Introduction

Projectile motion is a fundamental concept in classical mechanics that describes the motion of an object launched into the air and subject only to the force of gravity. When an object is projected with an initial velocity at a certain angle, it follows a curved path known as a **parabolic trajectory** — a direct consequence of the constant downward acceleration due to gravity.

The acceleration due to gravity on Earth is taken as **g = 9.81 m/s²**, acting vertically downward. The horizontal component of motion remains uniform (constant velocity), while the vertical component is uniformly decelerated on the way up and accelerated on the way down.

### Real-Life Applications
- Sports: Basketball shots, football kicks, javelin throws
- Military: Artillery and ballistics
- Engineering: Designing water fountains, roller coasters
- Space Science: Orbital mechanics and rocket trajectories

> **Note:** In this simulation, **air resistance is neglected** for simplicity. The object is assumed to move in a vacuum, allowing pure gravitational effects to be studied.

---

## 2. Libraries Used

| Library | Version | Purpose |
|---|---|---|
| Python | 3.10 | Core programming language |
| NumPy | Latest | Numerical computations and array generation |
| Matplotlib | Latest | 2D trajectory plotting and visualization |
| Jupyter Notebook | Latest | Interactive development and documentation |

Install dependencies using:
```bash
pip install -r requirements.txt
```

---

## 3. Working / Algorithm

The simulation follows this step-by-step algorithm:

```
START
  1. Accept user input:
       - Initial velocity (v₀) in m/s
       - Launch angle (θ) in degrees
  2. Convert angle from degrees to radians:
       θ_rad = θ × (π / 180)
  3. Compute velocity components:
       vx = v₀ × cos(θ_rad)
       vy = v₀ × sin(θ_rad)
  4. Compute key parameters:
       Time of Flight : T = (2 × v₀ × sin θ) / g
       Maximum Height : H = (v₀² × sin²θ) / (2g)
       Range          : R = (v₀² × sin 2θ) / g
  5. Generate 200 evenly spaced time points from 0 to T
  6. Compute trajectory:
       x(t) = vx × t
       y(t) = vy × t − ½ × g × t²
  7. Print T, H, R
  8. Plot x(t) vs y(t) using Matplotlib
END
```

---

## 4. Formulas

| Parameter | Formula |
|---|---|
| Horizontal Velocity | vx = v₀ cos θ |
| Vertical Velocity | vy = v₀ sin θ |
| Time of Flight | T = (2 v₀ sin θ) / g |
| Maximum Height | H = (v₀² sin²θ) / (2g) |
| Horizontal Range | R = (v₀² sin 2θ) / g |
| x-position | x(t) = vx · t |
| y-position | y(t) = vy · t − ½ g t² |

Where:
- **v₀** = Initial velocity (m/s)
- **θ** = Launch angle (degrees)
- **g** = 9.81 m/s² (acceleration due to gravity)

---

## 5. Output Requirements

The program produces the following outputs:

### Console Output
```
========================================
   PROJECTILE MOTION SIMULATION
========================================
Initial Velocity : 50.0 m/s
Launch Angle     : 45.0°
----------------------------------------
Time of Flight   : 7.21 s
Maximum Height   : 63.71 m
Horizontal Range : 254.84 m
========================================
```

### Graphical Output
- A 2D parabolic trajectory plot
- X-axis: Horizontal Distance (m)
- Y-axis: Vertical Height (m)
- Grid lines enabled
- Title and axis labels included
- Peak height and range annotated

---

## 6. Testing Section

Three test cases were used to validate the simulation:

### Test Case 1 — Maximum Range (θ = 45°)
| Parameter | Value |
|---|---|
| Initial Velocity | 50 m/s |
| Launch Angle | 45° |
| Time of Flight | 7.21 s |
| Maximum Height | 63.71 m |
| Range | 254.84 m |
|
### Test Case 2 — θ = 30°
| Parameter | Value |
|---|---|
| Initial Velocity | 50 m/s |
| Launch Angle | 30° |
| Time of Flight | 5.10 s |
| Maximum Height | 31.86 m |
| Range | 220.59 m |
|
### Test Case 3 — θ = 60° (Complementary to 30°)
| Parameter | Value |
|---|---|
| Initial Velocity | 50 m/s |
| Launch Angle | 60° |
| Time of Flight | 8.83 s |
| Maximum Height | 95.57 m |
| Range | 220.59 m |
|
> ✅ **Validation:** θ = 30° and θ = 60° produce the **same range** (220.59 m), confirming the complementary angle property.

---

## 7. Discussion

### Why Does 45° Give Maximum Range?
The range formula is:

**R = (v₀² × sin 2θ) / g**

The range is maximized when **sin 2θ = 1**, which occurs when **2θ = 90°**, i.e., **θ = 45°**. At this angle, the horizontal and vertical velocity components are perfectly balanced, producing the greatest ground coverage.

### Complementary Angles
For any two angles that add up to 90° (e.g., 30° and 60°), the value of **sin 2θ** is identical:
- sin(2 × 30°) = sin 60° ≈ 0.866
- sin(2 × 60°) = sin 120° = sin(180° − 60°) = sin 60° ≈ 0.866

This is why complementary launch angles always produce **equal ranges**.

### Limitations
- **No air resistance:** Real-world projectiles experience drag, which reduces range and alters trajectory.
- **Flat Earth assumption:** Curvature of the Earth is ignored.
- **Point mass:** The projectile is treated as a dimensionless point with no rotation or spin.
- **No wind effects:** Wind speed and direction are not considered.

---

## 8. Conclusion

This simulation successfully models projectile motion using Python, NumPy, and Matplotlib. The results are consistent with theoretical physics:
- 45° yields maximum range ✅
- Complementary angles yield equal range ✅
- Parabolic trajectory is correctly plotted ✅

### Suggested Improvements
| Improvement | Description |
|---|---|
| Air Resistance | Model drag force: F = ½ρCdAv² |
| 3D Extension | Add z-axis for lateral motion |
| GUI Interface | Use Tkinter or PyQt for interactive input |
| Animation | Use Matplotlib's FuncAnimation for live trajectory |
| Multiple Angles | Overlay trajectories for various angles |

---

## 9. References

1. Halliday, D., Resnick, R., & Walker, J. — *Fundamentals of Physics*, 10th Edition. Wiley.
2. NumPy Documentation — https://numpy.org/doc/
3. Matplotlib Documentation — https://matplotlib.org/stable/contents.html
4. GeeksforGeeks — *Projectile Motion Simulation using Python* — https://www.geeksforgeeks.org/projectile-motion-simulation-python/
5. OpenStax Physics — *Projectile Motion* — https://openstax.org/books/university-physics-volume-1/pages/4-3-projectile-motion

---

*This project was developed as part of a Physics simulation assignment using Python.*