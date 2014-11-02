import os
import csv
from operator import itemgetter
import math
import linecache

def sort_DT_MESSAGE(timestamp):	#Function to generate a sorting value
	month = {'Jan':1, 'Feb':2 , 'Mar':3, 'Apr':4 , 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
	timestamp = timestamp.split()
	timestamp[0] = timestamp[0].split('-')
	timestamp[1] = timestamp[1].split(':')
	val1 = int(timestamp[0][0]) + month[timestamp[0][1]]
	val2 = int(timestamp[1][0]) * 60 + int(timestamp[1][1])
	timestamp = val1 + val2
	return timestamp

def add_time(timestamp, current_time):	#function to add time
	waiting_time = 0
	timestamp[1] = timestamp[1].split(':')
	seconds = int(timestamp[1][2])
	minutes = int(timestamp[1][1])
	hours = int(timestamp[1][0])
	current_time[2] = current_time[2] - seconds
	if current_time[2] < 0:
		current_time[2] = current_time

	return waiting_time

list_of_all_rows = []
f=open("collect.csv",'r')
read = csv.reader(f)
header = read.next()	#save the header
read.next()	#skip the header

for r in read:
	timevalue = sort_DT_MESSAGE(r[4])
	r.append(timevalue)		#adding the sorting value
	list_of_all_rows.append(r)
f.close()

list_of_all_rows = sorted(list_of_all_rows, key=itemgetter(22))	#sort according to sorting value

for ele in list_of_all_rows:		#delete the sorting value
	ele.pop()

fout = open("collect.csv", 'w')		#open write file
writer = csv.writer(fout)
writer.writerow(tuple(header))

for ele in list_of_all_rows:	
	writer.writerow(tuple(ele))		#re-write the file with sorted timestamps
fout.close()

distance = []		#vector to keep distances between pairs of points
R = 6371 		#radius of the earth = 6371km
for i in range(len(list_of_all_rows) - 1):
	#use the haversine formula to calculate distance between two geo points

	del_lat = (float(list_of_all_rows[i][2]) * 3.14 / 180.0) - (float(list_of_all_rows[i+1][2]) * 3.14 / 180.0)
	del_lon = (float(list_of_all_rows[i][3]) * 3.14 / 180.0) - (float(list_of_all_rows[i+1][3]) * 3.14 / 180.0)
	a = math.sin(del_lat/2)**2 + (math.cos(float(list_of_all_rows[i][2]) * 3.14 / 180.0) * math.cos(float(list_of_all_rows[i+1][2]) * 3.14 / 180.0) * math.sin(del_lon/2)**2)
	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
	d = R * c
	distance.append(d)
f.close()
def difference(e,s):
	st=s.split(' ')
	_start=st[1].split(':')
	end=e.split(' ')
	_end=end[1].split(':')
	time1=int(_end[0])*60+int(_end[1])
	time2=int(_start[0])*60+int(_start[1])
	return (time1-time2)

'''   DHAWAL
vector = []		#vector to keep a track of moving/stopped truck
f=open("collect.csv",'r')
f.readline()	#read the header
timestamp=f.readline().split(',')[4]	#read the first line

threshold = 1 		#define threshold limit (any distance below this value -> standstill)

print "The journey started at: " + str(timestamp)
for i in range(len(distance)):
	if distance[i]<threshold:
		for j in range(i, len(distance)):
			if distance[j]<threshold:
				continue
			else:
				pos = j
				break
		print "Waited till time: " + str(linecache.getline("collect.csv", pos)[4])
		break

	#run a loop for all the timestamps
	#then run an inner loop to go till the last standstill point
	#subtract last - first to get total time


	#old_timestamp = timestamp
	timestamp=f.readline().split(',')[4]
	if distance[i] < threshold:
		print "At time: " + str(timestamp) + '-> Standstill.'
		#total_waiting_time = add_time(timestamp, old_timestamp)
	else:
		print "At time: " + str(timestamp) + '-> Moving.'
		#total_travel_time = 
	# take 4-5 GPS_Data files and do the analysis for the same vehicle/trip number
	#Do this for many trips and study a number of sample trip summaries to 
	#identify patterns, individual variation, etc, time of day for long stops, etc
	
	'''

