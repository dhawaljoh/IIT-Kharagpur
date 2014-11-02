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

def readData1(filename):
    labels = ['LATITUDE', 'LONGITUDE', 'DISTANCE']
    data = csv.DictReader(open(filename,'r').readlines()[1:], labels)
    coords = [(float(d['LATITUDE']), float(d['LONGITUDE'])) for d in data if len(d['LATITUDE']) > 0]
    return coords

def readData(filename):
    labels = ['LATITUDE', 'LONGITUDE', 'DISTANCE']
    data = csv.DictReader(open(filename, 'r').readlines()[1:], labels)
    coords = [(float(d['LATITUDE']), float(d['LONGITUDE']),float(d['DISTANCE'])) for d in data]
    return coords

def visulaizeOnMap(coords,filename):
    resultFile=open(filename,'wb')
    resultFile.write("Type,Latitude,Longitude,name\n")
    for i in range(len(coords)):
        lati,loni,te=coords[i]
        resultFile.write('W,'+str(lati)+","+str(loni)+","+str(i+1)+" "+str(te)+'\n')
    resultFile.close()

def writeHotspotsOnFile(coords,filename):
    resultFile=open(filename,'wb')
    for i in range(len(coords)):
        lati,loni,dist=coords[i]
        resultFile.write(str(lati)+","+str(loni)+","+str(dist)+'\n')
    resultFile.close()

def calculateDistanceMatrix(coords):
    n=len(coords)
    distance_matrix = np.zeros((n,n))
    for i in range(n):
        for j in range(i):
            lati,loni,dist=coords[i]
            latj,lonj,dist=coords[j]
            distance_matrix[i,j]=haversine(loni,lati,lonj,latj)
            distance_matrix[j,i]=distance_matrix[i,j]
    return distance_matrix

def plotKNearestNeighbour(distance_matrix,k,n):
    finalis=[]
    for i in range(n):
        lis=[]
        for j in range(n):
            if i!=j:
                lis.append(distance_matrix[i][j])
        lis.sort()
        finalis.append(lis[k-1])
    finalis.sort()
    plt.plot(finalis)
    plt.show()
    # for i in range(len(finalis)):
    #     print str(i+1)+" "+str(finalis[i])

def visulaizeClustering(labels,core_samples):
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    unique_labels = set(labels)
    colors = pl.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = 'k'
            markersize = 1
        class_members = [index[0] for index in np.argwhere(labels == k)]
        cluster_core_samples = [index for index in core_samples
                                if labels[index] == k]
        for index in class_members:
            x = coords[index]
            if index in core_samples and k != -1:
                markersize = 12
            else:
                markersize = 1
            pl.plot(x[1], x[0], 'o', markerfacecolor=col,markeredgecolor='k', markersize=markersize)
    pl.title('Estimated number of clusters: %d' % n_clusters_)
    pl.show()

def getHotspotsFromClusters(db):
    meanLats=[]
    meanLons=[]
    dists=[]
    for k in set(db.labels_):
        if k!=-1:
            class_members = [index[0] for index in np.argwhere(db.labels_==k)]
            cluster_core_samples = [index for index in core_samples if labels[index] == k]
            meanLat=0
            meanLon=0
            dist=[]
            for index in cluster_core_samples:
                lat,lon,te=coords[index]
                meanLat+=lat
                meanLon+=lon
                dist.append(te)
            meanLat=meanLat/(len(cluster_core_samples))
            meanLon=meanLon/(len(cluster_core_samples))
            x=np.array(dist)
            dists.append(np.median(x))
            mini=999999
            for index in cluster_core_samples:
                lat,lon,te=coords[index]
                if(haversine(lon,lat,meanLon,meanLat)<mini):
                    storeIndex=index
            meanLat,meanLon,dist=coords[storeIndex]
            meanLats.append(meanLat)
            meanLons.append(meanLon)
    return zip(meanLats,meanLons,dists)

def visualizeAllCoreClusterSamples(db,filename):
    color=['red','blue','green',"black", "fuchsia", "olive", "skyblue", "papayawhip"]
    counter = 0
    resultFile=open(filename,'wb')
    for k in set(db.labels_):
        resultFile.write("Type,Latitude,Longitude,name,color\n")
        if k!=-1:
            class_members = [index[0] for index in np.argwhere(db.labels_==k)]
            cluster_core_samples = [index for index in core_samples if labels[index] == k]
            for index in cluster_core_samples:
                lati,loni,te=coords[index]
                resultFile.write('W,'+str(lati)+","+str(loni)+","+str(te)+","+color[counter%8]+'\n')
        counter=counter+1
    resultFile.close()

def sortingHotspots(hotspots):
    mini=99999
    lat=22.815614
    lon=86.294536
    store=-1
    meanLons=[]
    meanLats=[]
    dists=[]
    n=len(hotspots)
    print n
    for i in range(n):
        lati,loni,te=hotspots[i]
        if(haversine(loni,lati,lon,lat)<mini):
            mini=haversine(loni,lati,lon,lat)
            store=i
    lat,lon,dist=hotspots[store]
    meanLats.append(lat)
    meanLons.append(lon)
    dists.append(dist)
    visited=[]
    for i in range(n):
        visited.append(False)
    visited[store]=True
    current=store
    for i in range(n-1):
        mini=99999
        lati,loni,te=hotspots[current]
        for j in range(n):
            if visited[j]==False:
                lat,lon,te=hotspots[j]
                if(haversine(loni,lati,lon,lat)<mini):
                    mini=haversine(loni,lati,lon,lat)
                    store=j
        lat,lon,dist=hotspots[store]
        meanLats.append(lat)
        meanLons.append(lon)
        dists.append(dist)
        current=store
        visited[store]=True
    return zip(meanLats,meanLons,dists)

coords = readData('toBeClustered5.csv')
distance_matrix= calculateDistanceMatrix(coords)
print "Done"
# plotKNearestNeighbour(distance_matrix,4 ,len(coords))
e = 50
sam= 4
db = DBSCAN(eps=float(e)/1000,min_samples=sam,metric='precomputed').fit(distance_matrix)
labels=db.labels_
core_samples = db.core_sample_indices_
hotspots = getHotspotsFromClusters(db)
sortedHotspots= sortingHotspots(hotspots)
visulaizeOnMap(sortedHotspots,"discontinuityPoints"+str(e)+"-"+str(sam)+".csv")
writeHotspotsOnFile(sortedHotspots,"RoadPoints"+str(e)+"-"+str(sam)+".csv")
visualizeAllCoreClusterSamples(db,"allClusterCores"+str(e)+"-"+str(sam)+".csv")
visulaizeClustering(labels,core_samples)