import numpy as np 
import matplotlib.pyplot as plt
from PIL import Image
from typing import Tuple

image = Image.open("fermat.png").convert("RGBA")
image_array = np.array(image)

R = float(input("Enter the radius of curvature of the mirror (e.g., 0.8): "))

obj_width = 0.6   # m
obj_height = 0.6  # m
h, w = image_array.shape[:2]

step = 0.05  # m
x_obj = -1.0  # Start outside the center of curvature
y_obj = 0.0

def map(x: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Returns an array of coordinates for a real image of an object in a concave spherical mirror.

    Args:
        x (np.ndarray): x-coordinates of the original object.
        y (np.ndarray): y-coordinates of the original object.

    Returns:
        Tuple[np.ndarray, np.ndarray]: The array of points (X, Y) of the real image.
    """
    alpha = (1/2)* np.arctan(y / x)
    k = x / np.cos(2 * alpha)
    numerator_Y = (k/R) - np.cos(alpha) + (x/y) * np.sin(alpha)
    Y = (k * np.sin(alpha)) / numerator_Y
    X = x * Y / y
    return X, Y

fig, ax = plt.subplots(figsize=(10, 10))

def plot_scene():
    ax.clear()
    # draw the object image 
    ax.imshow(
        image_array,
        extent=(
            x_obj - obj_width / 2,
            x_obj + obj_width / 2,
            y_obj - obj_height / 2,
            y_obj + obj_height / 2,
        ),
    )
    #create the coordinate grid for the object 
    x_lin = np.linspace(x_obj - obj_width / 2, x_obj + obj_width / 2, w)
    y_lin = np.linspace(y_obj - obj_height / 2, y_obj + obj_height / 2, h)
    xx, yy = np.meshgrid(x_lin, y_lin)
    # Mask to avoid undefined values
    mask = (xx != 0) & (yy != 0)

    X, Y = map(xx[mask], yy[mask])
    pixels = (image_array)[mask] / 255.0
    ax.scatter(X, Y, c=pixels, s=1)

    #plot the conves mirror
    theta = np.linspace(np.pi / 2, 3*np.pi / 2, 200)
    x_mirror = R + R * np.cos(theta)
    y_mirror = R * np.sin(theta)
    ax.plot(x_mirror, y_mirror, color='red', linewidth=2)

    #formatting
    ax.axhline(0, color='black', linestyle='--', linewidth=0.5)  # Principal axis
    ax.set_title(f"Object center at ({x_obj:.2f}, {y_obj:.2f})")
    ax.set_xlim(-2 * R, 2 * R)
    ax.set_ylim(-2 * R, 2 * R)
    ax.set_xlabel("X-axis (m)")
    ax.set_ylabel("Y-axis (m)")
    ax.set_aspect("equal")
    ax.grid(True)
    fig.canvas.draw()

def on_key(event):
    global x_obj, y_obj
    if event.key == 'up':
        y_obj += step
    elif event.key == 'down':
        y_obj -= step
    elif event.key == 'left' and x_obj - step > -3*R:
        x_obj -= step
    elif event.key == 'right' and x_obj + step < 2 * R:
        x_obj += step
    plot_scene()

fig.canvas.mpl_connect('key_press_event', on_key)
print("\nPlot window is active. Use arrow keys to move the object.")
plot_scene()
plt.show()