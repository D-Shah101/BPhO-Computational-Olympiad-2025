import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

image = Image.open('fermat.png').convert('RGBA')
image_array = np.array(image)

# Dimentions of the object in meters 
obj_width = 0.4
obj_height = 0.4

# Pixel dimensions
h, w = image_array.shape[:2]

step = 0.1
x_obj = 2.0  #Object starting postition
y_obj = 0.0
f = float(input("Enter focal length of the lens (m): "))

fig, ax = plt.subplots()

def lens_transform(x, y, f):
    X = -f / (x - f) * x
    Y = (y / x) * X  
    return X, Y

def plot_scene():
    ax.clear()
    ax.imshow(image_array, extent=[ x_obj - obj_width/2, x_obj + obj_width/2, y_obj - obj_height/2, y_obj + obj_height/2])
    #Distoreted image 
    x_lin = np.linspace(x_obj - obj_width / 2, x_obj + obj_width / 2, w)
    y_lin = np.linspace(y_obj - obj_height / 2, y_obj + obj_height / 2, h)
    xx, yy = np.meshgrid(x_lin, y_lin)
    # Mask to avoid division by zero or undefined lens mapping
    mask = (xx != f) & (xx != 0)
    X, Y = lens_transform(xx[mask], yy[mask], f)
    pixels = image_array[mask] / 255.0
    ax.scatter(X, Y, c=pixels, s=1)
    #Formatting
    ax.axvline(0, color='blue', linestyle='--', linewidth=1)
    ax.set_title(f"Object at ({x_obj:.2f}, {y_obj:.2f}) | f = {f}")
    ax.set_xlim(-3, 3)
    ax.set_ylim(-2, 2)
    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    ax.set_aspect('equal')
    ax.grid(True)
    fig.canvas.draw()

def on_key(event):
    global x_obj, y_obj
    if event.key == 'up':
        y_obj += step
    elif event.key == 'down':
        y_obj -= step
    elif event.key == 'left' and x_obj - step > f + 0.01:
        x_obj -= step
    elif event.key == 'right':
        x_obj += step
    plot_scene()

fig.canvas.mpl_connect('key_press_event', on_key)
print("\nPlot window is active. Use arrow keys to move the object.")
plot_scene()
plt.show()
