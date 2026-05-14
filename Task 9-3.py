import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from typing import Tuple

image = Image.open("fermat.png")
image_array = np.array(image)

R = float(input("Enter the radius of curvature of the mirror (e.g., 0.8): "))

obj_width = 0.6   # m
obj_height = 0.6  # m
h, w = image_array.shape[:2]

step = 0.05   # m
x_obj = -1.0  # Start object in front of the mirror
y_obj = 0.0

#new mapping with correct curvature or barrel distortion 
def map_with_barrel_distortion(x: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:

    x_shifted = x - R
    theta = np.arctan(y / np.sqrt(R**2 - y**2))
    m = np.tan(2 * theta)

    numerator_X = m * np.sqrt(R**2 - y**2) - y
    denominator_X = (y / x_shifted) + m
    X_shifted = -numerator_X / denominator_X
    Y = (y / x_shifted) * X_shifted
    X = X_shifted + R

    return X, Y

fig, ax = plt.subplots(figsize=(10, 10))

def plot_scene():
    ax.clear()
    
    ax.imshow(
        image_array,
        extent=(
            x_obj - obj_width / 2,
            x_obj + obj_width / 2,
            y_obj - obj_height / 2,
            y_obj + obj_height / 2,
        ),
    )
    
    x_lin = np.linspace(x_obj - obj_width / 2, x_obj + obj_width / 2, w)
    y_lin = np.linspace(y_obj - obj_height / 2, y_obj + obj_height / 2, h)
    xx, yy = np.meshgrid(x_lin, y_lin)
    # Mask to avoid undefined values
    mask = (np.abs(yy) < R) & (xx != 0)

    X, Y = map_with_barrel_distortion(xx[mask], yy[mask])
    
    pixels = np.flipud(image_array)[mask] / 255.0
    ax.scatter(X, Y, c=pixels, s=1)

    # Plot the convex mirror
    theta = np.linspace(np.pi / 2, 3 * np.pi / 2, 200)
    x_mirror = R + R * np.cos(theta)
    y_mirror = R * np.sin(theta)
    ax.plot(x_mirror, y_mirror, color='blue', linewidth=2, label="Convex Mirror")
    
    # Formatting
    ax.axhline(0, color='black', linestyle='--', linewidth=0.5)
    ax.set_title(f"Object center at ({x_obj:.2f}, {y_obj:.2f})")
    ax.set_xlim(-2 * R, 2 * R)
    ax.set_ylim(-2 * R, 2 * R)
    ax.set_xlabel("X-axis (m)")
    ax.set_ylabel("Y-axis (m)")
    ax.set_aspect("equal")
    ax.grid(True)
    ax.legend()
    fig.canvas.draw()

def on_key(event):
    global x_obj, y_obj
    if event.key == 'up':
        y_obj += step
    elif event.key == 'down':
        y_obj -= step
    elif event.key == 'left':
        x_obj -= step
    elif event.key == 'right':
        if x_obj + step < -obj_width / 2:
            x_obj += step
    plot_scene()

fig.canvas.mpl_connect('key_press_event', on_key)
print("\nPlot window is active. Use arrow keys to move the object.")
plot_scene()
plt.show()