import os
from tifffile import imread
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Function to calculate pixel size in micrometers
def calculate_pixel_size_um(sensor_size_mm, num_pixels):
    # mm is 10e-3 meter, um is 10e-6 meter
    sensor_size_um = sensor_size_mm * 1000 # Convert from mm to um
    # The size of each pixel is the size of the total area over the numer of pixels in the area
    pixel_size_um = sensor_size_um / num_pixels 
    return pixel_size_um 

# Gaussian function
def gaussian(x, amplitude, mean, stddev, background):
    return amplitude * np.exp( (-pow(x - mean, 2)) / (2*pow(stddev,2)) ) + background

# Function to calculate the beam size in um and position in pixels
def calculate_beam_properties(image, pixel_size_um, iteration):
    
    # Sum the values of the pixels along x and y axes
    sum_x = np.sum(image, axis=0)
    sum_y = np.sum(image, axis=1)
    
    # Init axes
    x_axis = np.arange(len(sum_x))
    y_axis = np.arange(len(sum_y))

    # Init figure for subplots
    # 2D array with one row and 2 colums (basically 1D array)
    figure, (x_axis_plot, y_axis_plot) = plt.subplots(1, 2, layout='constrained')

    # Plot the raw data for sum x
    x_axis_plot.plot(x_axis, sum_x, label='sum_x')
    x_axis_plot.set_xlabel('x index')
    x_axis_plot.set_title("x axis")

    # Plot the raw data for sum y
    y_axis_plot.plot(sum_y, y_axis, label='sum_y')
    y_axis_plot.set_ylabel('y index')
    y_axis_plot.set_title("y axis")
    y_axis_plot.invert_yaxis() # from top to bottom (similar to the image axes)
    
    # Fit Gaussian function to summed pixel values along x-axis and set Initial guesses and bounds (Chapter 4.1)
    # amplitude geuss: close to max value
    # mean_guess = close to he center of the axis
    # stddev_guess = middle of the bounds (common sense)
    # background_guess = minimum of the data
    initial_guesses = [np.max(sum_x), len(x_axis) / 2, len(x_axis) / 4, np.min(sum_x)]
    bounds = (
        # Lower bounds: A > 0              , mean >= 0          , stddev > 1             , background >= 0
        # Upper bounds: A < axis len * 2**8, mean <= len(x_data), stddev <= len(x_data)/2, background < A
        [0, 0, 1, 0], 
        [pow(2,8)*len(x_axis), len(x_axis), len(x_axis) / 2, np.max(sum_x)]
    )
    # The first return value from curve fit is the optimal values
    fit_x, _ = curve_fit(gaussian, x_axis, sum_x, p0=initial_guesses, bounds=bounds, maxfev=5000)
    amplitude_x, mean_x, stddev_x, background_x = fit_x
    
    # Fit Gaussian function to summed pixel values along y-axis and set Initial guesses and bounds
    initial_guesses = [np.max(sum_y), len(y_axis) / 2, len(y_axis) / 4, np.min(sum_y)]
    bounds = (
        [0, 0, 1, 0], 
        [pow(2,8)*len(y_axis), len(y_axis), len(y_axis) / 2, np.max(sum_y)]
    )
    fit_y, _ = curve_fit(gaussian, y_axis, sum_y, p0=initial_guesses, bounds=bounds, maxfev=5000)
    amplitude_y, mean_y, stddev_y, background_y = fit_y
    
    # Plot the fit on the raw data (Chapter 4.2)
    x_axis_plot.plot(x_axis, gaussian(x_axis, *fit_x), label='fit_x')
    y_axis_plot.plot(gaussian(y_axis, *fit_y), y_axis, label='fit_y')

    # Figure title and labels
    figure.suptitle('beam profiler', fontsize=16) # Title of the figure
    x_axis_plot.legend() # Apply the labels of x axis subplot
    y_axis_plot.legend() # Apply the labels of y axis subplot

    # Plot only the first iteration (Chapter 3.3)
    if(iteration == 0): plt.show() 

    # Calculate beam size (twice the standard deviation) and position in pixel (Chapter 3.2)
    w0_x = 2 * stddev_x
    w0_y = 2 * stddev_y
    
    # Convert beam size and position to micrometers (Chapter 3.2)
    beam_size_um = (pixel_size_um * w0_x, pixel_size_um * w0_y)
    beam_position_um = (pixel_size_um * mean_x, pixel_size_um * mean_y)
    beam_position_pixel = (mean_x, mean_y)

    # Calculate beam size in (twice the standard deviation) and position
    return beam_size_um, beam_position_um, beam_position_pixel

# Function to calculate RMS (Root Mean Square)
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

# Driver code

# Read input file
input_file = 'input.txt'
with open(input_file, encoding="UTF-8") as f_in:
    lines = f_in.readlines() # Return all lines as an array
    directory = lines[0].strip() # First line in the path
    sensor_size_mm = float(lines[1].strip()) # Second line is the sensor size in millimeters
    # 'with' Automatically closes f_in file

# List all files in the directory
image_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.tif')]

# Initialize lists to store beam positions
beams_size_um = ([],[])
beams_position_pixel = ([],[])

iteration = 0
# Load each image and calculate pixel size
for image_file in image_files:

    # Load image
    image = imread(image_file)

    # Reshape image if needed
    # first two dimentions are the hight and width of the image, they represent each pixel
    # the third dimention is an RBGA(red,blue,green,alpha=opacity)
    # black is (0,0,0,1) white is (255,255,255,0<=x<=1)
    if(len(image.shape) == 3): image = image[:, :, 2] #slice the third dimention and leave only the first item
    
    # Get image dimensions
    pixels_num_x = image.shape[1]  # number of pixels along x-axis
    
    # 3.1 Calculate pixel size in micrometers
    pixel_size_um = calculate_pixel_size_um(sensor_size_mm, pixels_num_x)

    # 3.2 Calculate beam size and position
    beam_size_um, beam_position_um, beam_position_pixel = calculate_beam_properties(image, pixel_size_um, iteration)
    
    #Append te values
    beams_size_um[0].append(beam_size_um[0])
    beams_size_um[1].append(beam_size_um[1])
    beams_position_pixel[0].append(beam_position_pixel[0])
    beams_position_pixel[1].append(beam_position_pixel[1])

    # Step up the iteration by one
    if(iteration == 0): iteration += 1


# Convert lists to numpy arrays
# The reason is that in calculate rms function we use np.mean and it recives only np arrays 
beams_position_pixels = (np.array(beams_position_pixel[0]), np.array(beams_position_pixel[1]))

# Calculate RMS for x,y axis and calculate r(Radius) RMS
rms_x, rms_y, rms_r = calculate_rms(beams_position_pixels[0], beams_position_pixels[1])

# Write output file
f_out = open("Beam_Size_measerment_results.txt", "w", encoding="UTF-8") #open file in write mode
print(f'Beams average size x in micrometers: {np.mean(beams_size_um[0]):1.2e}', end='\n', file=f_out)
print(f'Beams average size x in micrometers: {np.mean(beam_size_um[1]):1.2e}', end='\n', file=f_out)
print(f'Pointing stability in axis x in micrometers: {rms_x:1.2e}', end='\n', file=f_out)
print(f'Pointing stability in axis y in micrometers: {rms_y:1.2e}', end='\n', file=f_out)
print(f'Pointing stability in axis r in micrometers: {rms_r:1.2e}', end='\n', file=f_out)
print(f'Beams average x postion in pixels: {np.mean(beams_position_pixels[0]):1.2e}', end='\n', file=f_out)
print(f'Beams average y postion in pixels: {np.mean(beams_position_pixels[1]):1.2e}', end='\n', file=f_out)
print(f'Pixel size in micrometers: {pixel_size_um:1.2e}', end='\n', file=f_out)
print(f'Name of the directory of the images: {directory}', end='', file=f_out)
f_out.close()