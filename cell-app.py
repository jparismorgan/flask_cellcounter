##Web and File Libraries
from __future__ import division, unicode_literals, print_function  # for compatibility with Python 2 and 3
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from werkzeug.utils import secure_filename
import sys


##Cell Counting Libraries
import matplotlib as mpl
mpl.use('Agg') #non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
import pandas as pd
from pandas import DataFrame, Series  # for convenience
import pims
import trackpy as tp

#Debug
import logging

UPLOAD_FOLDER = 'uploads'	#where we put the final images
DOWNLOAD_FOLDER = 'downloads' #where we put the un-marked user images
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'tif'])

app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

@app.route("/")
def main():
	return render_template('index.html')

# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
	#clear the DOWNLOAD directory
	for root, dirs, files in os.walk(app.config['DOWNLOAD_FOLDER']):
	    for f in files:
	    	os.unlink(os.path.join(root, f))
	    for d in dirs:
	    	shutil.rmtree(os.path.join(root, d))
	#clear the UPLOAD directory
	for root, dirs, files in os.walk(app.config['UPLOAD_FOLDER']):
	    for f in files:
	    	os.unlink(os.path.join(root, f))
	    for d in dirs:
	    	shutil.rmtree(os.path.join(root, d))

	# Get specifications
	uploaded_files = request.files.getlist("file[]")
	_invert = request.form['invert']
	_diameter = int(request.form['diameter'])
	_min_mass = float(request.form['minmass'])
	_noise_size = float(request.form['noise_size'])
	_smoothing_size = float(request.form['smoothing_size'])
	_separation = float(request.form['separation'])
	#list of files for use on upload.html
	filenames = []

#TODO - Save original images into an uploads folder, then get them and put them in a downloads folder.
#Clear both every time. will avoid save issues

	for file in uploaded_files:
		# Check if the file is one of the allowed types/extensions
		if file and allowed_file(file.filename):
			# Make the filename safe, remove unsupported chars
			filename = secure_filename(file.filename)
			#Save file to upload folder
			file.save(os.path.join(app.config['DOWNLOAD_FOLDER'], filename))
			#load the image frames
			frames = pims.ImageSequence(os.path.join(app.config['DOWNLOAD_FOLDER'], filename), as_grey=True)
			#for loop of 1 to deal with PIMS bug.
			for frame in frames: 
				#locate features
				f = tp.locate(frames, _diameter, minmass=_min_mass, separation=_separation, invert=_invert) #noise_size=_noise_size, smoothing_size=_smoothing_size, 
				plt.ioff() #interactive mode = off
				plt.figure(filename) # make a new figure
				plt.xlabel('Number of cells: ' + str(len(f))) #label axis
				tp.annotate(f, frame) #display the iamge and the circle overlay
				
				#filename_png_extension = os.path.splitext(filename)[0] + ".png"

				plt.savefig(os.path.join(app.config['UPLOAD_FOLDER'], filename), format='png')   # save the figure to filenames
				plt.close() #close figure
					
				# Save the filename into a list, we'll use it later
				filenames.append(filename)
	# Load an html page with a link to each uploaded file
	return render_template('upload.html', filenames=filenames)

# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

##Helper Functions
def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

if __name__ == "__main__":
	#for debugging, remove for production
	app.run(debug=True)
