import numpy as np
import matplotlib.pyplot as plt


def f_to_w(freq): 
    C = 299792458.0 
    return (C / (freq * 1e12)) * 1e9

def n_of_glass(wavelength_nm): #refractive index of glass (BK7) using the Sellmeier equation
    wl = (wavelength_nm / 1000.0)**2
    n2 = 1 + (1.03961212 * wl) / (wl - 0.0060007) + (0.231792344 * wl) / (wl - 0.0200179) + (1.01046945 * wl) / (wl - 103.56065)
    return np.sqrt(n2)


def calculate_deflection(theta_i_rad, alpha_rad, n):
    #transmissopn and deflection angles of a prism 
    #for first graph -> works out transmission angle
    sin_ti = np.sin(theta_i_rad)
    cos_ti = np.cos(theta_i_rad)
    sin_a = np.sin(alpha_rad)
    cos_a = np.cos(alpha_rad)
    # Calculate the argument for the square root, handling invalid cases
    arg_sqrt = n**2 - sin_ti**2
    arg_sqrt[arg_sqrt < 0] = np.nan 
    # Calculate sin(theta_t)
    sin_tt = sin_a * np.sqrt(arg_sqrt) - cos_a * sin_ti #first formula
    sin_tt[np.abs(sin_tt) > 1] = np.nan # Total Internal Reflection
    # Calculate theta_t and delta
    theta_t_rad = np.arcsin(sin_tt)
    #for second graph -> works out deflection angle 
    delta_rad = theta_i_rad + theta_t_rad - alpha_rad 
    
    return np.rad2deg(theta_t_rad), np.rad2deg(delta_rad) #in degrees for plotting


def plot_fixed_alpha():
    #fist two graphs with fixed alpha and frequency
    alpha_deg = 45.0
    freq = 542.5
    # Calculate the single refractive index for this frequency
    wavelength = f_to_w(freq)
    n = n_of_glass(wavelength)
    #incident angles
    theta_i_deg = np.linspace(0, 90, 500)
    theta_i_rad = np.deg2rad(theta_i_deg)
    #calculation
    theta_t_deg, delta_deg = calculate_deflection(theta_i_rad, np.deg2rad(alpha_deg), n)
    
    #maximum transmission angle
    max_t_idx = np.nanargmax(theta_t_deg)
    max_theta_i_for_t = theta_i_deg[max_t_idx]
    max_t_val = theta_t_deg[max_t_idx]

    # TIR cutoff angle for the bottom graph
    first_valid_idx = np.where(~np.isnan(delta_deg))[0][0]
    cutoff_theta_i_deg = theta_i_deg[first_valid_idx]

    # Create the plot with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10))
    fig.suptitle(f'Prism Deflection for α = {alpha_deg}° and n = {n:.4f}', fontsize=14)
    
    #transmission angle vs. incident angle
    ax1.plot(theta_i_deg, theta_t_deg, 'b-')
    ax1.axvline(x=max_theta_i_for_t, color='purple', linestyle='--', lw=1) # Line for max
    ax1.set_title(r'$\theta_t$ vs $\theta_i$')
    ax1.set_xlabel('Angle of incidence $\\theta_i$ /deg')
    ax1.set_ylabel('Transmission angle $\\theta_t$ /deg')
    ax1.text(max_theta_i_for_t - 30, max_t_val - 5, f'$\\theta_{{t,max}} = {max_t_val:.2f}^\\circ$') # Text for max
    ax1.grid(True)
    ax1.set_xlim(0, 90)
    ax1.set_ylim(0, 100)
    
    # deflection angle vs. incident angle
    ax2.plot(theta_i_deg, delta_deg, 'b-')
    ax2.axvline(x=cutoff_theta_i_deg, color='red', linestyle='--', lw=1)
    ax2.set_title(f'Deflection angle $\delta$ vs $\theta_i$')
    ax2.set_xlabel('Angle of incidence $\\theta_i$ /deg')
    ax2.set_ylabel('Deflection angle $\\delta$ /deg')
    ax2.text(cutoff_theta_i_deg + 2, 52, f'$\\theta_{{max}} = {cutoff_theta_i_deg:.3f}^\\circ$')
    ax2.grid(True)
    ax2.set_xlim(0, 90)
    ax2.set_ylim(25, 55)
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])

def plot_variable_alpha():
    freq = 542.5
    wavelength = f_to_w(freq)
    n = n_of_glass(wavelength)

    # incident angles 
    theta_i_deg = np.linspace(0.1, 90, 500)
    theta_i_rad = np.deg2rad(theta_i_deg)
    #alpha values 
    alpha_values_deg = np.arange(10, 80, 5) #increases in increments of 5
    
    #plot
    fig, ax = plt.subplots(figsize=(8, 6))
    colours = plt.cm.rainbow(np.linspace(0, 1, len(alpha_values_deg)))
    
    for i, alpha_deg in enumerate(alpha_values_deg):
        _, delta_deg = calculate_deflection(theta_i_rad, np.deg2rad(alpha_deg), n)
        ax.plot(theta_i_deg, delta_deg, color=colours[i], label=f'α={alpha_deg}°')
        
    ax.set_title(f'Deflection angle $\delta$ /deg using f={freq}THz')
    ax.set_xlabel('Angle of incidence $\\theta_i$ /deg')
    ax.set_ylabel('Deflection angle $\\delta$ /deg')
    ax.grid(True)
    ax.set_xlim(0, 90)
    ax.set_ylim(0, 80)
    ax.legend(title='Prism Angle α')


plot_fixed_alpha()
plot_variable_alpha()
plt.show()