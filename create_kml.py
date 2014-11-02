import csv
import simplekml
import sys

f = open("plot.csv", 'r')
kml = simplekml.Kml()
reader = csv.reader(f)

for i in xrange(1, 10000):
	reader.next()
	
count = 0
for row in reader:
	kml.newpoint(coords=[(row[1], row[0])])
	count = count + 1
	if count == 16000:
		break

kml.save("plot.kml")