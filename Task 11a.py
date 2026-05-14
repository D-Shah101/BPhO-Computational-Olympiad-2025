import numpy as np
import matplotlib.pyplot as plt


n = float(input("Enter refractive index to 3dp (n) e.g water is 1.333: "))

#theta values for plotting
theta_deg = np.linspace(0, 90, 1000)
# Convert to radians for trig calculations
theta_rad = np.deg2rad(theta_deg)

# Clip arcsin arguments to [-1, 1] to prevent invalid values
arg = np.sin(theta_rad) / n
arg = np.clip(arg, -1.0, 1.0)
theta_r = np.arcsin(arg) # Refracted angle

#formulas for lines 
eps_primary_rad = 4 * theta_r - 2 * theta_rad  #primary rainbow (bottom)
eps_secondary_rad = np.pi + 2 * theta_rad - 6 * theta_r #secondary rainbow (top)

# Convert to degrees for plotting
eps_primary_deg = np.rad2deg(eps_primary_rad)
eps_secondary_deg = np.rad2deg(eps_secondary_rad)

# plotting
fig, ax = plt.subplots(figsize=(10, 7))



i1 = np.argmax(eps_primary_deg)
i2 = np.argmin(eps_secondary_deg)
ax.plot(theta_deg, eps_primary_deg, label=f'Primary Rainbow (~{eps_primary_deg[i1]:.1f}°)', color='red')
ax.plot(theta_deg, eps_secondary_deg, label=f'Secondary Rainbow (~{eps_secondary_deg[i2]:.1f}°)', color='purple')
ax.scatter(theta_deg[i1], eps_primary_deg[i1], color='red', s=60, zorder=5)
ax.scatter(theta_deg[i2], eps_secondary_deg[i2], color='purple', s=60, zorder=5)
ax.annotate(f'{eps_primary_deg[i1]:.1f}°',
            (theta_deg[i1], eps_primary_deg[i1]),
            textcoords="offset points", xytext=(0,10), ha='center', color='red')
ax.annotate(f'{eps_secondary_deg[i2]:.1f}°',
            (theta_deg[i2], eps_secondary_deg[i2]),
            textcoords="offset points", xytext=(0,10), ha='center', color='purple')

ax.set_xlabel(r'$\theta$ (Incidence Angle) / deg', fontsize=12)
ax.set_ylabel(r'$\varepsilon$ (Elevation Angle) / deg', fontsize=12)
ax.set_title(f'Rainbow Elevation vs. Incidence Angle (n = {n})')
ax.grid(True)
ax.legend()
ax.set_xlim(0, 90)
ax.set_ylim(0, 180)

text_str = fr"""$n$ = {n:.3f}"""
bbox_props = dict(boxstyle='round,pad=0.5', facecolor='aliceblue', alpha=0.9, edgecolor='gray')
ax.text(0.05, 0.95, text_str, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=bbox_props)

plt.show()