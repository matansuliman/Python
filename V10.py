import os
from tifffile import imread
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# 3.1 Function to calculate pixel size
def calculate_pixel_size(sensor_size_mm, num_pixels):
    # mm is 10e-3 meter, um is 10e-6 meter
    return sensor_size_mm / num_pixels * 1000  # Convert from mm to micrometers

# 3.2 Define Gaussian function for fitting
def gaussian(x, amplitude, mean, stddev, up_shift):
    return amplitude * np.exp( (-pow(x - mean, 2)) / (2*pow(stddev,2)) ) + up_shift

# 3.2 Function to calculate the beam size and position
def calculate_beam_properties(image, pixel_size_um):
    #reshape image if needed
    if(len(image.shape) == 3): image = image[:, :, 2]

    # Sum the values of the pixels along x and y axes
    sum_x = np.sum(image, axis=0)
    sum_y = np.sum(image, axis=1)
    
    x_axis = np.arange(len(sum_x))
    y_axis = np.arange(len(sum_y))

    #plot the beam
    figure, axis = plt.subplots(1, 2) 
    axis[0].plot(x_axis, sum_x, label='sum_x') 
    axis[0].set_title("x axis")
    axis[1].plot(sum_y, y_axis, label='sum_y') 
    axis[1].set_title("y axis")
    axis[1].invert_yaxis() #from top to bottom
    
    # Fit Gaussian function to summed pixel values along x-axis and set Initial guesses and bounds 
    initial_guess = [np.max(sum_x), len(x_axis) / 2, len(x_axis) / 4, np.min(sum_x)]
    bounds = (
        [0, 0, 1, 0],  # Lower bounds: A > 0, mean >= 0, sigma > 1, background >= 0
        [np.inf, len(x_axis), len(x_axis) / 2, np.max(sum_x)]  # Upper bounds: no upper bound for A, mean <= len(x_data), sigma <= len(x_data)/2, background < A
    )
    optimal_x, _ = curve_fit(gaussian, x_axis, sum_x, p0=initial_guess, bounds=bounds, maxfev=5000)
    amplitude_x, mean_x, stddev_x, up_shift_x = optimal_x
    
    # Fit Gaussian function to summed pixel values along y-axis and set Initial guesses and bounds 
    initial_guess = [np.max(sum_y), len(y_axis) / 2, len(y_axis) / 4, np.min(sum_y)]
    bounds = (
        [0, 0, 1, 0],  # Lower bounds: A > 0, mean >= 0, sigma > 1, background >= 0
        [np.inf, len(y_axis), len(y_axis) / 2, np.max(sum_y)]  # Upper bounds: no upper bound for A, mean <= len(x_data), sigma <= len(x_data)/2, background < A
    )
    optimal_y, _ = curve_fit(gaussian, y_axis, sum_y, p0=initial_guess, bounds=bounds, maxfev=5000)
    amplitude_y, mean_y, stddev_y, up_shift_y = optimal_y
    
    #plot the optimal
    axis[0].plot(x_axis, gaussian(x_axis, *optimal_x), label='optimal_x')
    axis[1].plot(gaussian(y_axis, *optimal_y), y_axis, label='optimal_y')
    axis[0].legend() #apply the labels
    axis[1].legend()
    plt.show()


    # Calculate beam size (twice the standard deviation) and position
    w0_x = 2 * stddev_x
    w0_y = 2 * stddev_y
    
    # Convert beam size and position to micrometers
    beam_size_x_um = pixel_size_um * w0_x
    beam_size_y_um = pixel_size_um * w0_y
    beam_position_x_um = pixel_size_um * mean_x
    beam_position_y_um = pixel_size_um * mean_y

    #Convert the mean values to micrometers
    mean_x_um = pixel_size_um * mean_x
    mean_y_um = pixel_size_um * mean_y

    return mean_x_um, (beam_size_x_um, beam_size_y_um), mean_y_um, (beam_position_x_um, beam_position_y_um)


# Function to calculate RMS
def calculate_rms(data_x, data_y):
    #RMS_x
    mean_x = np.mean(data_x)
    rms_x = np.sqrt(np.mean(pow(data_x-mean_x, 2)))
    #RMS_y
    mean_y = np.mean(data_y)
    rms_y = np.sqrt(np.mean(pow(data_y-mean_y, 2)))
    #RMS_r
    radial_distances = np.sqrt(pow(data_x - mean_x, 2) + pow(data_y - mean_y, 2))
    rms_r = np.sqrt(np.mean(pow(radial_distances, 2)))
    return rms_x, rms_y, rms_r


# Read input file
input_file = 'input.txt'
with open(input_file, encoding="UTF-8") as f:
    lines = f.readlines()
    directory = lines[0].strip()
    sensor_size_mm = float(lines[1].strip())

# List all files in the directory
image_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.tif')]

# Initialize lists to store beam positions
beam_positions_x = []
beam_positions_y = []

f = open("Beam_Size_measerment_results.txt", "w", encoding="UTF-8")
# Load each image and calculate pixel size
for image_file in image_files:

    print(f'Image: {image_file}', end='\n', file=f)

    # Load image
    image = imread(image_file)
    
    # Get image dimensions (assuming image is a 2D array)
    num_pixels_x = image.shape[1]  # Number of pixels along x-axis
    
    # 3.1 Calculate pixel size in micrometers
    pixel_size_um = calculate_pixel_size(sensor_size_mm, num_pixels_x)
    print(f'\tPixel size: {pixel_size_um:.3f} μm', end='\n', file=f)

    # 3.2 Calculate beam size and position
    mean_x_um, beam_size_um, mean_y_um, beam_position_um = calculate_beam_properties(image, pixel_size_um)
    
    print(f'\tBeam size x in micrometers: {beam_size_um[0]}', end='\n', file=f)
    print(f'\tBeam size y in micrometers: {beam_size_um[0]}', end='\n', file=f)
    print(f'\tBeam position (x, y) in micrometers: {beam_position_um}', end='\n', file=f)


    
    beam_positions_x.append(mean_x_um)
    beam_positions_y.append(mean_y_um)

    print('\n', file=f)

# Convert lists to numpy arrays
beam_positions_x = np.array(beam_positions_x)
beam_positions_y = np.array(beam_positions_y)

# Calculate RMS for x and y beam positions
rms_x, rms_y, rms_r = calculate_rms(beam_positions_x, beam_positions_y)

print(f'Pointing stability in axis x in micrometers: {rms_x:.2f}', end='\n', file=f)
print(f'Pointing stability in axis y in micrometers: {rms_y:.2f}', end='\n', file=f)
print(f'Pointing stability in axis r in micrometers: {rms_r:.2f}', end='\n', file=f)

f.close()



    






