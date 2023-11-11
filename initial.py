# %%
import time
import board
import busio
import numpy as np
import adafruit_mlx90640
import matplotlib.pyplot as plt
from scipy import ndimage

def initialize_camera():
    i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)  # setup I2C
    mlx = adafruit_mlx90640.MLX90640(i2c)  # begin MLX90640 with I2C comm
    mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_16_HZ  # set refresh rate
    return mlx

def interpolate_data(data, shape, interp_val):
    data_array = np.fliplr(np.reshape(data, shape))  # reshape, flip data
    return ndimage.zoom(data_array, interp_val)  # interpolate
    
def setup_display(interp_shape):
    # Live feed figure
    live_fig = plt.figure(figsize=(4, 3))
    live_ax = live_fig.add_subplot(111)
    live_fig.subplots_adjust(0.05, 0.05, 0.95, 0.95)
    live_therm = live_ax.imshow(np.zeros(interp_shape), interpolation='none',
                                cmap=plt.cm.coolwarm, vmin=0, vmax=45)
    live_fig.canvas.draw()
    live_ax_background = live_fig.canvas.copy_from_bbox(live_ax.bbox)
    live_fig.show()

    # Averaged figure
    avg_fig = plt.figure(figsize=(4, 3))
    avg_ax = avg_fig.add_subplot(111)
    avg_fig.subplots_adjust(0.05, 0.05, 0.95, 0.95)
    avg_therm = avg_ax.imshow(np.zeros(interp_shape), interpolation='none',
                              cmap=plt.cm.twilight, vmin=0, vmax=45)
    avg_fig.canvas.draw()
    avg_ax_background = avg_fig.canvas.copy_from_bbox(avg_ax.bbox)
    avg_fig.show()

    return (live_fig, live_ax, live_ax_background, live_therm), \
           (avg_fig, avg_ax, avg_ax_background, avg_therm)
           
           
def update_display(ax, fig, therm1, data_array, ax_background):
    fig.canvas.restore_region(ax_background)  # restore background
    therm1.set_array(data_array)  # set data
    therm1.set_clim(vmin=np.min(data_array), vmax=np.max(data_array))  # set bounds
    ax.draw_artist(therm1)  # draw new thermal image
    fig.canvas.blit(ax.bbox)  # draw background
    fig.canvas.flush_events()  # show the new image
    
def capture_and_max_frames(mlx, num_frames, mlx_shape, interp_val):
    first_frame = np.zeros(mlx_shape[0] * mlx_shape[1])  # Initialize frame array
    mlx.getFrame(first_frame)  # Capture the first frame to start with real data
    max_frame = np.reshape(first_frame, mlx_shape)  # Use the first frame as the starting point

    for _ in range(num_frames - 1):  # Already captured the first frame
        frame = np.zeros(mlx_shape[0] * mlx_shape[1])  # Initialize frame array
        mlx.getFrame(frame)  # Capture frame
        data_array = np.reshape(frame, mlx_shape)  # Reshape to the sensor's dimensions
        max_frame = np.maximum(max_frame, data_array)  # Compare and store the max value

    interpolated_frame = ndimage.zoom(max_frame, interp_val)  # Interpolate to enhance the image
    return interpolated_frame

# Parameters
mlx_shape = (24, 32)  # mlx90640 shape
mlx_interp_val = 10  # interpolate # on each dimension
mlx_interp_shape = (mlx_shape[0] * mlx_interp_val,
                    mlx_shape[1] * mlx_interp_val)  # new shape

# Initialization
mlx = initialize_camera()
live_display, avg_display = setup_display(mlx_interp_shape)
live_fig, live_ax, live_ax_background, live_therm = live_display
avg_fig, avg_ax, avg_ax_background, avg_therm = avg_display

# Main loop
frame = np.zeros(mlx_shape[0] * mlx_shape[1])  # initialize frame array
t_array = []  # initialize timing array
capture_interval = 20  # Number of frames to wait before capturing and averaging
frame_counter = 0  # Counter to track the number of frames

while True:
    t1 = time.monotonic()  # for determining frame rate
    try:
        mlx.getFrame(frame)
        live_data_array = interpolate_data(frame, mlx_shape, mlx_interp_val)
        update_display(live_ax, live_fig, live_therm, live_data_array, live_ax_background)

        frame_counter += 1  # Increment frame counter
        print(f'Frame Counter: {frame_counter} / {capture_interval}')
        if frame_counter >= capture_interval:
            print('Capturing and maxing frames...')
            max_data = capture_and_max_frames(mlx, 30, mlx_shape, mlx_interp_val)  # Corrected function name
            update_display(avg_ax, avg_fig, avg_therm, max_data, avg_ax_background)
            frame_counter = 0  # Reset counter after capturing
            
    except Exception as e:
        print(f"Error: {e}")
        continue
    # Frame rate calculation
    t2 = time.monotonic()
    t_array.append(t2 - t1)
    if len(t_array) > 10:
        t_array = t_array[1:]  # keep only recent times
    print(f'Frame Rate: {len(t_array) / np.sum(t_array):2.1f}fps')