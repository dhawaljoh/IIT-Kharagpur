import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import pylab as bp

def getData(segmentNumber):
	data=[]
	for i in range(24):
		hour=i
		mylines=[]
		lines=[line.strip() for line in open("./Plotting/SegmentAnalysis/HourlyInfoSegments/hourInfoOfSegments"+str(hour)+".txt")]
		mylines=[float(val) for val in lines[segmentNumber].split()]
		if len(mylines) == 0:
			data.append(float(0.0))
		else :
			x=np.array(mylines)
			data.append(float(x.mean()))
	return data

for i in range(65):
	segmentNumber=i
	data=getData(segmentNumber)
	x=np.array(data)
	fig=plt.figure()
	fig.suptitle('Average_Speed_Over_The_Day_On_Segment'+str(segmentNumber+1),fontsize=14,fontweight='bold')
	ax = fig.add_subplot(111)
	ax.set_xlabel('Time_Of_Day')
	ax.set_ylabel('Average_Speed(In Km/hrs)')
	bins = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
	plt.bar(bins,x,color='c',width=1.0)
	bp.xlim(0,24)
	bp.ylim(0,50)
	# plt.show()
	bp.savefig('./Plotting/SegmentAnalysis/HourlySegmentSpeedPlots/speed_Distribution_Segment'+str(segmentNumber+1), bbox_inches='tight')
