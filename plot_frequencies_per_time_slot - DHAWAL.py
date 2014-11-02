import matplotlib.pyplot as plt
import os
import csv
from operator import itemgetter
import math
import linecache
import sys
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.axes as ax
import matplotlib
import random
from numpy import *
import numpy as np
from os import listdir
from os.path import isfile, join

#fig, ax = plt.subplots()
#fig.canvas.draw()

#-------------------------------------------------------------------------------------------------------------------------------------

def get_vehicle_IDs():		#Get trip IDs 		CHANGE the "count" variable in this function to get plots for different number of trips
	#count = 0
	for row in reader:
		if row[5] not in trip_IDs:
			trip_IDs.append(row[6])
		# 	count = count + 1
		# if count == 100:
		# 	print "Trip IDs generated."
		# 	return

def generate_csvs():		#Function to generate the csv files for the trips in trip_IDs
	for trip in trip_IDs:
		fout = open(str(trip)+".csv", 'w')
		writer = csv.writer(fout)
		writer.writerow(tuple(header))	#write the header
		for row in reader:
			if row[6] == trip:
				writer.writerow(tuple(row))
		f.seek(0)
		fout.close()
		print "File created for: " + str(trip)

def sort_DT_MESSAGE(timestamp):	#Function to generate a sorting value
	month = {'Jan':1, 'Feb':2 , 'Mar':3, 'Apr':4 , 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
	timestamp = timestamp.split()
	timestamp[0] = timestamp[0].split('-')
	timestamp[1] = timestamp[1].split(':')
	val1 = int(timestamp[0][0]) + month[timestamp[0][1]] * 12
	val2 = int(timestamp[1][0]) * 60 + int(timestamp[1][1])
	timestamp = val1 + val2
	return timestamp
	
def get_time_val(timestamp):
	month = {'Jan':1, 'Feb':2 , 'Mar':3, 'Apr':4 , 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
	timestamp = timestamp.split()
	timestamp[0] = timestamp[0].split('-')
	timestamp[1] = timestamp[1].split(':')
	val1 = int(timestamp[0][0]) + month[timestamp[0][1]] + int(timestamp[0][2])
	val2 = int(timestamp[1][0]) * 60 + int(timestamp[1][1])
	timestamp = (val1 + val2)/10
	return timestamp

def sort_csvs_and_plot(trip):	#Function to sort the rows of the csv file
	global global_count
	list_of_all_rows = []
	count = 0
	fa=open(str(trip) + ".csv",'r')
	if fa == None:
		trip_IDs.remove(trip)
		return
	read = csv.reader(fa)

	total_rows = sum(1 for row in read)
	fa.seek(0)
	if total_rows>1:
		header = read.next()	#save the header
		read.next()	#skip the header

		for r in read:
			timevalue = sort_DT_MESSAGE(r[4])
			r.append(timevalue)		#adding the sorting value
			list_of_all_rows.append(r)
		fa.close()

		list_of_all_rows = sorted(list_of_all_rows, key=itemgetter(22))	#sort according to sorting value

		for ele in list_of_all_rows:		#delete the sorting value
			ele.pop()

		fout = open(str(trip) + ".csv", 'w')		#open write file
		writer = csv.writer(fout)
		writer.writerow(tuple(header))

		for ele in list_of_all_rows:	
			writer.writerow(tuple(ele))		#re-write the file with sorted timestamps
		fout.close()
		print "File: " + str(trip) + ".csv sorted."

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

		threshold = 1 		#define threshold limit (any distance below this value -> standstill)
		move_threshold = 3  #the truck is not moving in the interval if it's travelling atleast (6-threshold)% of time

		fa=open(str(trip) + ".csv",'r')
		read = csv.reader(fa)
		header = read.next()	#save the header

		trip_movement_per_slot = [0 for x in range(24)]


		for ele in distance:
			timeval = get_time_val(read.next()[4])
			if ele < threshold:
				plt.plot(global_count, timeval, 'rs', str(trip))
			else:
				plt.plot(global_count, timeval, 'gs', str(trip))
				trip_movement_per_slot[timeval/300] += 1

		for x in trip_movement_per_slot:
			if x>=move_threshold:
				frequencies[trip_movement_per_slot.index(x)] += 1

		global_count = global_count + 1


#-------------------------------------------------------------------------------------------------------------------------------------
#call order of functions
days = [str(f) for f in listdir("Data/") if isfile(join("Data/", f))]
days = sorted(days)
for file in days:
	f = open("Data/"+file, 'r')		#open read file
	if f == None:
		continue
	reader = csv.reader(f)

	header = reader.next() # read the header

#-------------------------------------------------------------------------------------------------------------------------------------
#Global variables:
	trip_IDs = []		#stores the trip ID's that are to be plotted.
	global_count = 0
	ylabels = ['1am', '2am', '3am', '4am', '5am', '6am', '7am', '8am', '9am', '10am', '11am', '12pm', '1pm', '2pm', '3pm', '4pm', '5pm', '6pm', '7pm', '8pm', '9pm', '10pm', '11pm']
	xlabels_slots = ['1-2am', '2-3am', '3-4am', '4-5am', '5-6am', '6-7am', '7-8am', '8-9am', '9-10am', '10-11am', '11-12pm', '12-1pm', '1-2pm', '2-3pm', '3-4pm', '4-5pm', '5-6pm', '6-7pm', '7-8pm', '8-9pm', '9-10pm', '10-11pm', '11-12am']
	get_trip_IDs()
	trip_IDs = trip_IDs[:30]
	frequencies = [0 for x in range(24)]
	generate_csvs()
	for trip in trip_IDs:
		sort_csvs_and_plot(trip)


	plt.figure()
	'''
	plt.subplot()
	plt.axis([-1, global_count+1, 0, 144])
	plt.xlabel('Trips')
	plt.ylabel('Time of the Day')


	y = [y for y in range(6,144,6)]
	x = [x for x in range(0, global_count)]

	ax.set_yticks(y)
	ax.set_xticks(x)
	plt.xticks(rotation=50)
	for i in range(len(trip_IDs)):
		if i%5 != 0:
			trip_IDs[i]=""

	ax.set_xticklabels(trip_IDs)
	ax.set_yticklabels(ylabels)
	plt.tight_layout()
	plt.show()
	'''

	#plt.subplot()
	pos = np.arange(len(xlabels_slots))
	width = 1
	ax = plt.axes()
	ax.set_xticks(pos + (width/2))
	plt.xticks(rotation=50)
	ax.set_xticklabels(xlabels_slots)
	plt.bar(pos, frequencies[:23], width, color='r')
	plt.tight_layout()
	plt.gcf()
	plt.savefig('histogram' + file + '.png', bbox_inches='tight')
	#plt.show()