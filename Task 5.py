import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

image = Image.open('fermat.png')
image_array = np.array(image)
x_obj = 0.4
y_obj = 0.5
step = 0.05

fig, ax = plt.subplots()

def plot():
    ax.clear()
    x_img = -x_obj
    y_img = y_obj
    ax.imshow(image_array, extent=[x_obj-0.2, x_obj+0.2, y_obj-0.2, y_obj+0.2])
    ax.imshow(np.fliplr(image_array), extent=[x_img-0.2, x_img+0.2, y_img-0.2, y_img+0.2])
    ax.axvline(x=0, color='gray', linestyle='--', label='mirror (y-axis)')
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_title('Virtual Image')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_aspect('equal')
    ax.legend()
    ax.grid(True)
    fig.canvas.draw()  

def arrow(event):
    global x_obj, y_obj
    if event.key == 'up':
        y_obj += step
    elif event.key == 'down':
        y_obj -= step
    elif event.key == 'left':
        x_obj -= step
    elif event.key == 'right':
        x_obj += step
    plot()

fig.canvas.mpl_connect('key_press_event', arrow)
plot()
plt.show()