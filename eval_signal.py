import matplotlib.pyplot as plt
import numpy as np
import math


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

	return arrays
	file.close()


def str_to_flts(string):
	""" Convert string of values to floats. """
	return [float(num) for num in string.split()]


def plot_1Mode(arrays):
	""" Plot values from one mode """ #modify for more than one channel
	for i in range(0,len(arrays)):	
		plt.figure(i)
		plt.plot(arrays[i][:,2],arrays[i][:,1])
		plt.show()
	return None


def clean_data(array):
	""" Delete data that is completely wrong. """ #modify for more than one channel
	size = np.size(array[:,0])

	#calculate average: do not include values that are out of 0 - 5 V range
	values = array[ array[:,1] < 5]
	avg = np.average(values[:,1])

	#delete rows that are more than 5uV different from average -> OK since we are measuring static voltage
	del_row = []
	row_num = 0
	for row in array:
		if abs(row[1] - avg) > 0.005: # modify this
			del_row.append(row_num)
		row_num += 1
	array = np.delete(array, del_row, 0)

	return array


def std_dev(array):
	""" Calculate standard deviation of a sample. """
	vals = array[:,1]
	avg = np.average(vals)
	size = len(array[:,1])
	var = 0 #variance
	for val in vals:
		var += (val - avg)**2/size
	return math.sqrt(var)


def fourier(array):
	""" Calculate fourier transform of a sample. """
	return np.fft.fft(array[:,1])


# read file with data
#arrays = list_of_arrays('test_file3_5s')
arrays = list_of_arrays('test_file4')
print len(arrays)
for x in xrange(0,len(arrays)):
	arrays[x] = clean_data(arrays[x])
#plot_1Mode(arrays)


#calculate standard deviation
for arr in arrays:
	print std_dev(arr)


#calcualate fourier transform
ft = []
for i in range(0,len(arrays)):
	temp = fourier(arrays[i])
	ft.append(temp)
 	#ft.append(fourier(arrays[i]))
i = 0
for ch in ft:
	plt.figure(i)
	plt.plot(ch[1:len(ch)])
	plt.show()
	i += 1

#f3 = fourier(arrays[3])
#plt.plot(f3[1:len(f3)])

#f2 = fourier(arrays[2])
#plt.plot(f2[1:len(f2)])

#print len(arrays[2])
#plt.plot(ft[2][1:len(ft[2])])


