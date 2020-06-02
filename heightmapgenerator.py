# Creating a randomly generated heightmap using a 2d SHM model
# PROCESS #
# Develop a function that randomly generates amplitudes for different frequencies
# Higher frequencies get low applitudes to simulate noise
# Lower amplitudes represent peaks of the moutain so they get higher amplitudes
# Using an rgb color scheme, the amplitudes will be mapped greyscale to an array
# The array will map the rgb color to the pixels on the image

from PIL import Image
from math import sin, pi, floor, ceil, pow
import random as rand

#creates the file that stores the rgb values as a jpg
def createHeightMapFile(file_name,image_size): #string, int
	image = Image.new('RGB',(image_size,image_size),color = 'white')
	image.save(file_name + ".png")
	return image
	
#generates a squared 3D sinwave
def generateSquaredSin(x, y, amplitude, frequency, offset):
	position = amplitude*pow(sin(frequency*x + offset)*sin(frequency*y + offset),2)
	return position
	
def generateSin(x, y, amplitude, frequency, offset):
	position = amplitude*sin(frequency*x + offset)*sin(frequency*y + offset)
	return position
	
#initializes the matrix
def generateHeightMatrix(image_size):
	height_matrix = []
	for i in range(image_size):
		row = []
		for j in range(image_size):
			row.append(0)
		height_matrix.append(row)
	return height_matrix
	
#creates a sin function based off the fundamental frequency
def initializeSinFunction(image_size):
	height_matrix = generateHeightMatrix(image_size)
	num_waves = rand.randint(1,4)
	fundamental_frequency = rand.uniform(1/(image_size/6), 1/(image_size/4))
	amplitude = rand.randint(100,255)
	offset = rand.randint(image_size/5,image_size/2)
	for x in range(image_size): #loops through x's and y's
		for y in range(image_size):
			height = floor(generateSquaredSin(x, y, amplitude, fundamental_frequency, offset))
			(height_matrix[x])[y] = (height_matrix[x])[y] + height
	return height_matrix

#Subtracts 255(white in rgb) from the maximum value in the height matrix and sets 
#that value as the maximum possible amplitude for noise
def maxNoiseAmplitude(height_matrix):
	max_matrix = 0
	for x in range(0,len(height_matrix)):
		max_value = max(height_matrix[x])
		if (max_value > max_matrix):
			max_matrix = max_value
	max_amplitude = 255 - max_matrix
	return max_amplitude

#sets frequency for small wavelengths
def smallNoiseFrequency(image_size):
	frequency = rand.uniform(1/(image_size/40),1/(image_size/80))
	return frequency

#sets frequency for large wavelengths
def largeNoiseFrequency(image_size):
	frequency = rand.uniform(1/(image_size/15),1/(image_size/20))
	return frequency
	
#generatees noise on top of the initial sine wave, can change the 
#amount of noise for large wavelengths and small wavelengths
def generateNoise(height_matrix,image_size,num_waves,freqSize):
	#generating small waves
	for i in range(0,num_waves):
		max_amplitude = maxNoiseAmplitude(height_matrix)/2
		amplitude = rand.uniform(0,max_amplitude)
		offset = rand.randint(0,image_size)
		if freqSize == True:
			frequency = smallNoiseFrequency(image_size)
		else:
			frequency = largeNoiseFrequency(image_size)
		for x in range(0,image_size):
			for y in range(0,image_size):
				height = floor(generateSin(x,y,amplitude,frequency,offset))
				(height_matrix[x])[y] = (height_matrix[x])[y] + height
	return height_matrix

#converts the matrix to a JPG by converting each element in the matrix to a corresponding pixel	
def convertToJPG(image,file_name,image_size,height_matrix):
	for x in range(image_size):
		for y in range(image_size):
			height_color = (height_matrix[x])[y]
			image.putpixel((x,y),(height_color,height_color,height_color))
	image.save(file_name + '.png')
		
###Main program:
file_name = 'heightmap'
image_size = 500

image = createHeightMapFile(file_name,image_size)
sin_wave = initializeSinFunction(image_size)
small_noise_matrix = generateNoise(sin_wave,image_size,5,False)
final_height_matrix = generateNoise(small_noise_matrix,image_size,5,True)
convertToJPG(image,file_name,image_size,final_height_matrix)