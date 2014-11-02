from math import radians, cos, sin, asin, sqrt
import csv
import numpy as np
from scipy.spatial import distance
from sklearn.cluster import DBSCAN
import pylab as pl
import matplotlib.pyplot as plt
# Function Return haversine Distance

def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km 

def readData(filename):
    labels = ['LATITUDE', 'LONGITUDE', 'DISTANCE']
    data = csv.DictReader(open(filename,'r').readlines()[1:], labels)
    coords = [(float(d['LATITUDE']), float(d['LONGITUDE']), float(d['DISTANCE'])) for d in data]
    return coords

def transform(coords):
    lat=22.83559
    lon=86.22876
    prevDist=0
    list1=[]
    list2=[]
    dists=[]
    startDistance=0
    for i in range(len(coords)):
        lati,loni,te=coords[i]
        list1.append(lati)
        list2.append(loni)
        if(te<prevDist):
            lat=22.83559
            lon=86.22876
            startDistance=0
        val=haversine(lon,lat,loni,lati)
        dists.append(startDistance+val)
        startDistance=startDistance+val
        lon=loni
        lat=lati
        prevDist=te

    return zip(list1,list2,dists)

num_bins = 300   #binsize parameter
coords = readData('toBeClustered5.csv')
# coords = transform(coords)
coords2=readData('RoadPoints50-4.csv')
# coords2=transform(coords2)
data=[]
data2=[]
for loc in coords2:
	x,y,dist=loc
	data2.append(float(dist))
for loc in coords:
	x,y,dist=loc
	data.append(float(dist))
x=np.array(data)
fig=plt.figure()
ax = fig.add_subplot(111)
ax.set_xlabel('Distance_From_Origin')
ax.set_ylabel('Number_Of_Discontinuity')
n, bins, patches = plt.hist(x, num_bins,histtype='bar',facecolor='c',rwidth=01)
limits = ax.axis()
for i in range(len(data2)):
	plt.plot((data2[i],data2[i]),(0,limits[3]),'r',linestyle='dashed',linewidth=1,label='median')
plt.show()
