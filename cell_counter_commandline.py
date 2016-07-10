##############################################################
# Loads in data and calls NN functions
# Julian Paris Morgan | 6/27/16

from __future__ import division, unicode_literals, print_function  # for compatibility with Python 2 and 3

#Libraries
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
import pandas as pd
from pandas import DataFrame, Series  # for convenience
import pims
import trackpy as tp

#Load images
def main():
	print("Opening up Chlorella Classifier...")

	#Get image source
	if (raw_input("Do you want to use the images in ../images? y/n\n") == "y"):
		frames = pims.ImageSequence('/Users/parismorgan/Desktop/images/*', as_grey=True)
	else:
		filepath = raw_input("What directory are your images located in?\n")
		toCont = "y"	
		while(toCont == "y"):
			try:
				frames = pims.ImageSequence(filepath+'/*.jpg', as_grey=True)
				toCont = "n"
				print ("yup")
			except IOError:
				toCont = raw_input("Invalid filepath. Try again? y/n\n")
				if (toCont == "y"):
					filepath = raw_input("What directory are your images located in?\n")
				else:
					print("Goodbye.")
					return 3.1415
	
	#Determine parameters
	if (raw_input("Do you want to use the default parameters? y/n\n") == "y"):
		imageClassifier(frames,21, 2600, 25)
	else:
		cellsize = raw_input("cell size?")
		if (cellsize % 2) == 0:
			cellsize += 1
		minmass = raw_input("minmass?")
		separation = raw_input("separation?")	
		imageClassifier(frames, cellsize, minmass, separation)
	return

	
def imageClassifier(frames, cell_size, min_mass, particle_separation):
	print("We have "+str(len(frames))+" images in this batch.\nWe will open them up one at a time.\n Feel free to save them and then exit the window to view the next one.")
	for frame in frames:
		f = tp.locate(frame, 21, invert=True, minmass=min_mass, separation=particle_separation, noise_size=4)
		locationWeightHistogram(f)
		plt.figure("Filename") # make a new figure
		plt.xlabel('Number of cells: ' + str(len(f)))
		tp.annotate(f, frame)
		plt.savefig('./filename.png', format='png')   # save the figure to file
		print(f.head())
	return 1

	# Use this histogram to check your choice of parameters. You should see an evenly distrobuted histogram
	# If there is a dip in the middle, then you should increase your cell_size parameter
def locationWeightHistogram(frame):
		print (frame)
		n, bins, patches = plt.hist(frame['mass'], bins=20)
		plt.xlabel('Smarts')
		plt.ylabel('Frequency')
		plt.title('Histogram of total brightness of particles')
		plt.grid(True)
		plt.show()


if __name__ == "__main__":
    main()