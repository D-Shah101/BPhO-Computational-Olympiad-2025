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


freq = np.linspace(430, 790, 500)
wavelengths_nm = f_to_w(freq)
n = n_of_water(wavelengths_nm)
#caluclates specific angle of incidence at which sunight must hit the water droplet to produce a rainbow
arg_p = np.clip((4 - n**2) / 3, 0, 1) # ensures values remain between 0 and 1
arg_s = np.clip((9 - n**2) / 8, 0, 1)
theta_i_p_rad = np.arcsin(np.sqrt(arg_p))
theta_i_s_rad = np.arcsin(np.sqrt(arg_s))
#Using snell's law to calculate the angle of refraction
phi_p_rad = np.arcsin(np.sin(theta_i_p_rad) / n)
phi_s_rad = np.arcsin(np.sin(theta_i_s_rad) / n)
#calculates critical angle
phi_c_rad = np.arcsin(1 / n)
#converts back to degrees for plotting
phi_p_deg = np.rad2deg(phi_p_rad)
phi_s_deg = np.rad2deg(phi_s_rad)
phi_c_deg = np.rad2deg(phi_c_rad)

#plotting
colours = [frequency_to_rgb(f) for f in freq]
fig, ax = plt.subplots(figsize=(10, 8))
ax.text(500, 48.1, 'Critical angle', fontsize=12, color='black')
ax.text(500, 45.8, 'Secondary', fontsize=12, color='blue', fontweight='bold')
ax.text(500, 40.6, 'Primary', fontsize=12, color='red', fontweight='bold')
ax.plot(freq, phi_c_deg * np.ones_like(freq), color='black', label='Critical Angle')
ax.scatter(freq, phi_p_deg, c=colours, s=15, zorder=5)
ax.scatter(freq, phi_s_deg, c=colours, s=15, zorder=5)


ax.set_xlabel('Frequency / THz', fontsize=12)
ax.set_ylabel(r'$\phi$ /deg', fontsize=14)
ax.set_title('Refraction angle of single and double rainbows', fontsize=14)
ax.set_xlim(420, 790)
ax.set_ylim(38, 49)
ax.grid(True, linestyle=':')
ax.legend(fontsize=12)

plt.show()