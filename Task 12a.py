import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

#constants
def n_of_glass(wavelength_nm): # refractive index of glass (BK7) using the Sellmeier equation
    wl = (wavelength_nm / 1000.0)**2
    n2 = 1 + (1.03961212 * wl) / (wl - 0.0060007) + (0.231792344 * wl) / (wl - 0.0200179) + (1.01046945 * wl) / (wl - 103.56065)
    return np.sqrt(n2)

def wavelength_to_rgb(wl_nm):#maps wavelength to RGB color
    if not (380 <= wl_nm <= 750): return (0.0, 0.0, 0.0)
    f = (wl_nm - 380) / (750 - 380)
    r = (1.0 - f)**0.7; g = (f**0.5) * ((1.0 - f)**0.5); b = f**0.7
    return (r, g, b)

class PrismModel:
    def __init__(self):
        # starting values for sliders  
        self.initial_alpha_deg = 30.0
        self.initial_theta_i_deg = 50.0

        #figure and axes
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        plt.subplots_adjust(left=0.1, bottom=0.25)
        self.fig.set_facecolor('#101010')
        self.ax.set_facecolor('black')
        # slider set up
        axcolor = '#222222'
        slider_ax_alpha = plt.axes([0.2, 0.1, 0.65, 0.03], facecolor=axcolor)
        slider_ax_theta_i = plt.axes([0.2, 0.05, 0.65, 0.03], facecolor=axcolor)
        self.slider_alpha = Slider(slider_ax_alpha, 'Prism Angle (α)', 30.0, 90.0, valinit=self.initial_alpha_deg)
        self.slider_theta_i = Slider(slider_ax_theta_i, 'Incident Angle (θi)', 0.0, 89.9, valinit=self.initial_theta_i_deg)
        
        for s in [self.slider_alpha, self.slider_theta_i]:
            s.label.set_color('white'); s.valtext.set_color('white')
        self.slider_alpha.on_changed(self.update)
        self.slider_theta_i.on_changed(self.update)
        self.update(None)

    def update(self, val):  #updates and runs every time slider is moved
        self.ax.clear()
        alpha_deg = self.slider_alpha.val
        theta_i_deg = self.slider_theta_i.val
        alpha_rad = np.deg2rad(alpha_deg)
        theta_i_rad = np.deg2rad(theta_i_deg)

        # prism
        prism_height = 1.0
        base_half_width = prism_height * np.tan(alpha_rad / 2.0)
        prism_verts = [[-base_half_width, 0], [base_half_width, 0], [0, prism_height]]
        prism_polygon = plt.Polygon(prism_verts, color='#223344', edgecolor='cyan')
        self.ax.add_patch(prism_polygon)
        #exact point on prisms face where light enters 
        entry_y = 0.6 * prism_height
        entry_x = (entry_y - prism_height) * np.tan(alpha_rad / 2.0)
        
        #incident ray
        normal_1_angle = np.pi - (alpha_rad / 2.0)
        inc_ray_angle = normal_1_angle - theta_i_rad
        start_x = -1.5 # A fixed x-position at the left edge
        slope = np.tan(inc_ray_angle)
        start_y = slope * (start_x - entry_x) + entry_y # Calculate y using the line equation
        self.ax.plot([start_x, entry_x], [start_y, entry_y], color='white', lw=3)
        wavelengths = np.linspace(400, 700, 100)
        tir_occurred = False
        
        #exact point light exits prism
        n_mid = n_of_glass(550.0)
        sin_theta_r1_mid = np.sin(theta_i_rad) / n_mid
        theta_r1_rad_mid = np.arcsin(sin_theta_r1_mid)
        internal_angle_rad_mid = normal_1_angle - theta_r1_rad_mid
        m_internal_mid = np.tan(internal_angle_rad_mid)
        m_right_face = -prism_height / base_half_width
        exit_x = (m_internal_mid * entry_x - entry_y - m_right_face * base_half_width) / (m_internal_mid - m_right_face)
        exit_y = m_internal_mid * (exit_x - entry_x) + entry_y

        self.ax.plot([entry_x, exit_x], [entry_y, exit_y], color='gray', lw=1.5, alpha=0.9)
        for wl in wavelengths:
            n = n_of_glass(wl) #refractive index for wavelength
            colour = wavelength_to_rgb(wl)
            sin_theta_r1 = np.sin(theta_i_rad) / n
            theta_r1_rad = np.arcsin(sin_theta_r1) #snells law to calculate how much colour bends 
            theta_i2_rad = alpha_rad - theta_r1_rad
            critical_angle = np.arcsin(1/n) #critical angle
            if abs(theta_i2_rad) >= critical_angle:
                tir_occurred = True; continue #determines if total internal reflection has occured
            #uses snells law to calculate how ray bends when exiting the prism
            sin_theta_t2 = n * np.sin(theta_i2_rad)
            theta_t2_rad = np.arcsin(sin_theta_t2)
            normal_2_angle = alpha_rad / 2.0
            exit_ray_angle = normal_2_angle - theta_t2_rad
            end_x = exit_x + 1.5 * np.cos(exit_ray_angle)
            end_y = exit_y + 1.5 * np.sin(exit_ray_angle)
            self.ax.plot([exit_x, end_x], [exit_y, end_y], color=colour, lw=2) # draws exit ray - all colours 

        if tir_occurred:
            self.ax.text(0, -0.1, 'Total Internal Reflection!', color='red', fontsize=16, ha='center', weight='bold') #if TIR occurs-displays warning 

        self.draw_plot_layout(theta_i_deg) 

    def draw_plot_layout(self, theta_i_deg=None, message=None): #plot
        self.ax.set_aspect('equal')
        self.ax.set_xlim(-1.5, 1.5); self.ax.set_ylim(-0.5, 1.2)
        self.ax.set_title("Dynamic Prism Dispersion Model", color='white')
        self.ax.axis('off')
        if theta_i_deg is not None:
             self.ax.text(0.02, 0.98, f"Incident Angle θi = {abs(theta_i_deg):.1f}°", 
                         transform=self.ax.transAxes, color='white', ha='left', va='top')
        if message:
            self.ax.text(0.5, 0.1, message, color='orange', fontsize=16, ha='center', weight='bold', transform=self.ax.transAxes)
        self.fig.canvas.draw_idle()


model = PrismModel()
plt.show()