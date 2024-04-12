# python project that profiles beams

# Overview
The goal of this project is to process images of laser beams to measure their size and position. The code uses a 1D Gaussian function to fit the data and measure beam properties. Tracking the position of the beam over time helps measure pointing stability.

## pre condition
* input.txt is in the same directory with beam_profiler.py
* the first line in input.txt has the abslute path to the directory with the tif files
* the second line in input.txt has the sensor size in millimeters
* the directory with the tif files has at least one tif file

## output
* Beams average size x in micrometers
* Pointing stability in axis x in micrometers
* Pointing stability in axis y in micrometers
* Pointing stability in axis r in micrometers
* Beams average x postion in pixels
* Beams average y postion in pixels
* Pixel size in micrometers
* Name of the directory of the images

# Dependencis
* tifffile
* numpy
* matplotlib
* scipy
