import numpy as np
import matplotlib.pyplot as plt

c= 299792458.0   #speed of light m/s

def f_to_w(freq):
    return (c / (freq * 1e12)) * 1e9 #converts frequency to wavelength nm

def n_of_water(wavelength_nm): #calculates refractive index of water for given wavelength 
    return 1.325 + 3076 / (wavelength_nm**2)  #simple empirical model for water's refractive index vs. wavelength

def frequency_to_rgb(freq): #maps frequencies to colours 
    f = freq
    if f < 430 or f > 790:
        return (0.0, 0.0, 0.0)

    if 430 <= f < 465:
        r, g, b = 1.0, 0.0, 0.0
    elif 465 <= f < 517:
        r, g, b = 1.0, (f - 465) / (517 - 465), 0.0
    elif 517 <= f < 588:
        r, g, b = -(f - 588) / (588 - 517), 1.0, 0.0
    elif 588 <= f < 612:
        r, g, b = 0.0, 1.0, (f - 588) / (612 - 588)
    elif 612 <= f < 682:
        r, g, b = 0.0, -(f - 682) / (682 - 612), 1.0
    elif 682 <= f <= 790:
        r, g, b = (f - 682) / (790 - 682), 0.0, 1.0
    else:
        r, g, b = 0.0, 0.0, 0.0
        
    #dimming at edges
    factor = 1.0
    if f>714 and f<=790: # Fades in the violet end
        factor = 0.3 + 0.7 * (790 - f) / (790 - 714)
    elif 430 <= f < 465: # Fades out the red end
        factor = 0.3 + 0.7 * (f - 430) / (465 - 430)
        
    return (r * factor, g * factor, b * factor)

# plotting function
def plot_rainbow_at_sea_level(ax, solar_angle_deg, rainbow_angles_p, rainbow_angles_s, freqs):
    alpha_rad = np.deg2rad(solar_angle_deg)
    
    # Generate colors for each frequency
    colors = [frequency_to_rgb(f) for f in freqs]
    for i in range(len(freqs)):
        # Get the angles for specific color
        eps_p_rad = np.deg2rad(rainbow_angles_p[i])
        eps_s_rad = np.deg2rad(rainbow_angles_s[i])
        # Calculate the maximum angle for the arcs
        cos_beta_p_max = np.clip(alpha_rad / eps_p_rad, -1, 1) if eps_p_rad > 0 else -1
        cos_beta_s_max = np.clip(alpha_rad / eps_s_rad, -1, 1) if eps_s_rad > 0 else -1
        beta_p_max = np.arccos(cos_beta_p_max)
        beta_s_max = np.arccos(cos_beta_s_max)
        # Create the parametric angle for drawing the arcs
        beta_p = np.linspace(-beta_p_max, beta_p_max, 200)
        beta_s = np.linspace(-beta_s_max, beta_s_max, 200)

        # Calculate the Azimuth (x) and Elevation (y) for plotting
        x_p = np.rad2deg(eps_p_rad * np.sin(beta_p))
        y_p = np.rad2deg(eps_p_rad * np.cos(beta_p) - alpha_rad)
        x_s = np.rad2deg(eps_s_rad * np.sin(beta_s))
        y_s = np.rad2deg(eps_s_rad * np.cos(beta_s) - alpha_rad)
        # Plot the arcs
        ax.plot(x_p, y_p, color=colors[i], linewidth=2.5)
        ax.plot(x_s, y_s, color=colors[i], linewidth=2.5)
        
    #Plot
    ax.set_title(f'Solar angle α={solar_angle_deg}°', fontsize=10)
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim(-60, 60)
    ax.set_ylim(-5, 60)
    ax.set_xticks([])
    ax.set_yticks([])


#calclations
freq = np.linspace(430, 790, 200)
wavelengths_nm = f_to_w(freq)
n = n_of_water(wavelengths_nm)
arg_p = np.clip((4 - n**2) / 3, 0, 1) #ensures values remain between 0 and 1
arg_s = np.clip((9 - n**2) / 8, 0, 1)
#angles of incidence
theta_i_p_rad = np.arcsin(np.sqrt(arg_p))
theta_i_s_rad = np.arcsin(np.sqrt(arg_s))
#Using snell's law to calculate the angle of refraction
theta_r_p_rad = np.arcsin(np.sin(theta_i_p_rad) / n)
theta_r_s_rad = np.arcsin(np.sin(theta_i_s_rad) / n)
#elevation angles
eps_p_rad = 4 * theta_r_p_rad - 2 * theta_i_p_rad
eps_s_rad = np.pi + 2 * theta_i_s_rad - 6 * theta_r_s_rad
eps_p_deg = np.rad2deg(eps_p_rad)
eps_s_deg = np.rad2deg(eps_s_rad)

fig, axes = plt.subplots(2, 2, figsize=(8, 6))
solar_angles_to_plot = [5, 20, 30, 40]
axes_flat = axes.flatten()

for i in range(len(solar_angles_to_plot)):
    ax = axes_flat[i]
    solar_angle = solar_angles_to_plot[i]
    plot_rainbow_at_sea_level(ax, solar_angle, eps_p_deg, eps_s_deg, freq)

plt.tight_layout()
plt.show()