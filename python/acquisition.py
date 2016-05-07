"""
	Author: Jure Bartol
	Date:   16/04/2016

	TO-DO:
	- (optional) live plotting
	- acquisition.py: 
		- use pickle instead of write
		- ConfigureFile() -> convert every value to volt
		-(DONE) write time to file too
	- ads1256.py:
		- Add comments + organize
	- gui
"""

from ads1256 import *
import time
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


def GetSample(channel):
	""" Get AD value from analog channel. 
		Chanels are: A0=0, A1=1, A2=2, A3=3, A4=4, A5=5, A6=6, A7=7. """
	SetChannel(channel)
	return ReadData()


def GetData(channels, timeStop):
	""" Acquire data from channels (input as list) for given time (input as timeStop).
		Every time buffer is filled with 500*len(channels), data is written to file"""
	loopNum = 0
	fileNum = 0
	data = []
	clock = []
	timeStart = time.time()
	#for i in xrange(0,10000):
	while (time.time() - timeStart) < timeStop:
		for ch in channels:
			data.append(GetSample(ch))
			clock.append(time.time())
		loopNum += 1
		if loopNum == 500:
			Write2File(fileNum, data, clock, len(channels))
			fileNum += 1
			loopNum = 0
			del data[:]
			del clock[:]
	Write2File(fileNum, data, clock, len(channels))
	
	
def Write2File(fileNum, data, time, chNum):
	""" Writes arranged data to file. Data for each channel is in a separate column. """
	f = open("Data%s.txt" % fileNum, 'w+')
	for row in xrange(len(data)/chNum):
		for col in xrange(chNum):
			#f.write("%i %f " % (data[row*chNum + col], time[row*chNum + col]))s
			f.write("%s " % (data[row*chNum + col]))
		f.write("\n")
	f.close()

def ConfigureFile(fileName):
	""" Convert values in files to volts. """
	f = open(filename,'w+')
	
	
	f.close()

ADInitialize()
t = time.time()
GetData([0,1,2,3,4,5,6,7],1)
print "Elapsed time is: %fs." % (time.time() - t)
ADEnd()

""" **Plotting**

ADInitialize()
var1 = [0]*6000
var2 = [0]*6000
time0 = time.time()
for x in xrange(0,6000):
	SetChannel(1)
	var1[x] = ReadData()
	SetChannel(2)
	var2[x] = ReadData()
print time.time() - time0

plt.plot(convert2volt(var1), label="ch1")
plt.plot(convert2volt(var2), label="ch2")
plt.legend()
plt.show()

ADEnd()

"""
