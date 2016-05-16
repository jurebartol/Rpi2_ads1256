# -*- encoding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import math
from pylab import *


# enable čšž etc.
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def list_of_arrays(path):
	""" Save values from file to an array for each mode. """
	file = open(path,'r')
	list = []
	for line in file:
		list.append(str_to_flts(line))

	# Find borders between different modes (SE_MUX / DIFF_MUX / SE_CONT / DIFF_CONT)
	newModeLine = [0]
	for x in xrange(0,len(list)-1):
		if list[x+1][0] < list[x][0]:
			newModeLine.append(x+1)	
	newModeLine.append(len(list))

	# Create numpy arrays (one 2d array for each mode) 
	arrays = []
	for x in range(0, len(newModeLine)-1):
		arrays.append (np.array(list [newModeLine[x] : newModeLine[x+1]] ))

	file.close()
	return arrays


def str_to_flts(string):
	""" Convert string of values to floats. """
	return [float(num) for num in string.split()]


def clean_data(array):
	""" Delete data that is completely wrong. """ # modify for more than one channel
	size = np.size(array[:,0])

	#calculate average: do not include values that are out of 0 - 5 V range
	values = array[ array[:,1] < 5]
	avg = np.average(values[:,1])

	del_row = []
	row_num = 0
	for row in array:
		if abs(row[1] - avg) > 0.1: # modify this -> it is only usable for static voltages
			del_row.append(row_num)
		row_num += 1
	array = np.delete(array, del_row, 0)
	return array


def std_dev(array):
	""" Calculate standard deviation of a sample. """
	vals = array[:,1]
	avg = np.average(vals)
	size = len(array[:,1])
	var = 0 
	for val in vals:
		var += (val - avg)**2
	return math.sqrt(var/size)

def std_dev2(vals):
	""" Calculate standard deviation of a sample. """
	avg = np.average(vals)
	size = len(vals)
	var = 0 
	for val in vals:
		var += (val - avg)**2
	return math.sqrt(var/size)


def fourier(array):
	""" Calculate fourier transform of a sample. """
	val = np.fft.fft(array[:,1])
	abs_val = [math.sqrt(x) for x in val.real**2 + val.imag**2]
	return abs_val

def sampling(array):
	""" Calculate average sampling frequency. """
	time = array[len(array)-1,2] - array[0,2]
	samples = len(array)
	return samples/time*1e6      #time in microseconds
	#return samples/time         #time in seconds


def rms_noise(array):
	""" Calculare RMS of noise. """
	values = array[:,1]
	sumSqrs = 0
	for val in values:
		sumSqrs += val**2
	return math.sqrt(float(sumSqrs)/len(values))

def rms_noise_norm(array):
	""" Calculare normalized RMS of noise. """
	vals = array[:,1]
	avg = np.average(vals)
	vals = vals - avg
	sumSqrs = 0
	for val in vals:
		sumSqrs += val**2
	return math.sqrt(float(sumSqrs)/len(vals))

def rms_sin(points, peak2peak, offset):
	""" Calculate RMS of discretisized sine wave. """
	pts = np.linspace(0, 2*math.pi, points)
	sin = [(float(peak2peak)/2.0 * math.sin(val) + offset) for val in pts]
	sumSqrs = 0
	for val in sin:
		sumSqrs += val**2
	return math.sqrt(float(sumSqrs)/len(sin))

def snr_norm(array, peak2peak, offset):
	""" Calculate SNR of a sine wave with offset and normalized RMS of noise. 
	Return value is in dB. """
	rmsNoise = rms_noise_norm(array)
	rmsSin = math.sqrt(offset**2 + 0.5*((float(peak2peak)/2.0)**2))
	return 20 * math.log10(float(rmsSin)/float(rmsNoise))

def snr_min(bitWidth):
	""" Calculate theoretical minimum SNR for sine wave. Return value is in dB. """
	return 6.02*(bitWidth-1) + 1.76

def snr_variance(array, peak2peak):
	""" Calculate signal-to-noise ratio for discretisized sine wave.
	Return value is in dB. """
	points = np.linspace(0, 2*math.pi, 5000)
	sin = [float(peak2peak)/2.0 * math.sin(val) for val in points]
	values = array[:,1]
	avg_val = np.average(values)
	values = values - avg_val
	var_err = (std_dev2(values))**2
	var_sig = (std_dev2(sin))**2
	return (10 * math.log10( float(var_sig) / float(var_err) ))

############################################
## read file with data + perform cleaning ##
############################################

#arrays = list_of_arrays('test_4230') #ads1256

for x in xrange(0,len(arrays)):
	arrays[x] = clean_data(arrays[x])

##############################################
## calculate standard deviation and average ##
##############################################

deviation = []
average = []
for arr in arrays:
	deviation.append(std_dev(arr))
	average.append(np.average(arr[:,1]))

##################################
## calcualate fourier transform ##
##################################

ft = []   # fourier transform values
sps = []  # sampling speed values
freq = [] # frequency vectors - for plotting
for i in range(0,len(arrays)):
	ft.append(fourier(arrays[i]))
	sps.append(sampling(arrays[i]))
	freq.append( sps[i]/len(arrays[i]) * np.linspace(0, len(arrays[i])-1, len(arrays[i])))

##################
## plot results ##
##################

xlabel1 = "Time [ms]"
xlabel2 = "Frequency [Hz]"
ylabel1 = "Voltage [mV]"
ylabel2 = "Noise amplitude"

# plot volt - time graph
i = 0

for arr in arrays:
	fig = plt.figure(figsize=(3.5,3))
	plt.plot([(time- arr[0,2])*1e-3 for time in arr[:,2]], [(val-average[i])*1e3 for val in arr[:,1]], label = labels[i], linewidth = 0.4)   #time in microseconds
	#plt.plot([time*1e3-1000 for time in arr[:,2]], [(val-average[i])*1e3 for val in arr[:,1]], label = labels[i], linewidth = 0.4)  #time in seconds
	plt.xlabel(xlabel1)
	plt.ylabel(ylabel1)
	plt.grid(True)
	#fig.savefig("image_%d.png"%(i), dpi=300, format='png', bbox_inches='tight')
	i += 1

# plot amplitude - frequency graph
i = 0

for mode, f in zip(ft, freq):
	fig = plt.figure(figsize=(3.5,3))
	plt.plot(f[1:len(f)], [val*1e-6 for val in mode[1:len(mode)]], label = labels[i], linewidth = 0.4) #time in microseconds
	#plt.plot(f[1:len(f)], mode[1:len(mode)], label = labels[i], linewidth = 0.4) #time in seconds
	plt.xlabel(xlabel2)
	plt.ylabel(ylabel2)
	#fig.savefig("image_%d.png"%(i), dpi=300, format='png', bbox_inches='tight')
	i += 1
plt.show()


print "\nDeviation: " # unit: V
for x in deviation: print x

print "\nSNR: "
for arr in arrays:
	print snr_norm(arr, 5, 2.5)


print "Theoretical minimum SNR of a 24 bit AD converter: %3.2f" % (snr_min(24))
