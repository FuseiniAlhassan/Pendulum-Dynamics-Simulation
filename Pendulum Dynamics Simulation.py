# pendulum_visualization.py
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# Output directory
FIG_DIR = "figures_pendulum"
os.makedirs(FIG_DIR, exist_ok=True)

# Parameters

g = 9.81            # gravity (m/s^2)
L = 1.0             # pendulum length (m)
theta0 = 0.2        # initial angle (rad)
omega0 = 0.0        # initial angular velocity (rad/s)
dt = 0.01           # time step (s)
T_total = 10        # total simulation time (s)
n_steps = int(T_total/dt)
t = np.linspace(0, T_total, n_steps)


# Small-angle approximation (linear)
# theta'' + (g/L)*theta = 0
theta_linear = theta0*np.cos(np.sqrt(g/L)*t)

# Full non-linear pendulum
# theta'' + (g/L)*sin(theta) = 0
# Using simple Euler method
theta = np.zeros(n_steps)
omega = np.zeros(n_steps)
theta[0] = theta0
omega[0] = omega0

for i in range(1, n_steps):
    omega[i] = omega[i-1] - (g/L)*np.sin(theta[i-1])*dt
    theta[i] = theta[i-1] + omega[i]*dt

# Plot comparison
fig, ax = plt.subplots(figsize=(8,4))
ax.plot(t, theta_linear, label="Linear approx (small-angle)")
ax.plot(t, theta, label="Non-linear")
ax.set_xlabel("Time [s]")
ax.set_ylabel("Angle [rad]")
ax.set_title("Pendulum Dynamics")
ax.grid(True)
ax.legend()
fname = os.path.join(FIG_DIR, "pendulum_theta_vs_time.png")
plt.savefig(fname, dpi=200)
plt.close(fig)
print("Saved pendulum comparison plot:", fname)

# Animation of pendulum motion
x = L*np.sin(theta)
y = -L*np.cos(theta)

fig, ax = plt.subplots(figsize=(5,5))
line, = ax.plot([], [], 'o-', lw=2)
ax.set_xlim(-1.2*L, 1.2*L)
ax.set_ylim(-1.2*L, 0.2*L)
ax.set_aspect('equal')
ax.grid(True)
ax.set_title("Pendulum Animation")

def init():
    line.set_data([], [])
    return line,

def animate(i):
    line.set_data([0, x[i]], [0, y[i]])
    return line,

anim = FuncAnimation(fig, animate, init_func=init, frames=n_steps, interval=20, blit=True)
anim_fname = os.path.join(FIG_DIR, "pendulum_animation.gif")
anim.save(anim_fname, writer='pillow', fps=50)
plt.close(fig)
print("Saved pendulum animation GIF:", anim_fname)
