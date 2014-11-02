import csv
import os
fout = open("feature.csv", 'w')		#open write file
writer = csv.writer(fout)
features = [1,2,3,4,5,6,10,14,15,16,17,18,21]           #selection of indices of the features wanted

def get_parent_dir(directory):
    import os
    return os.path.dirname(directory)

current_dirs_parent = get_parent_dir(os.getcwd())

for filename in os.listdir(current_dirs_parent):
	if filename.startswith("GPS_"):
		print "Parsing for file: " + filename
		f = open(current_dirs_parent + '/' + filename, 'r')         #open read file
		read = csv.reader(f)
		read.next()	#skip the header
		for r in read:
			row = []
			for i in features:
				row.append(str(r[i]))	
			writer.writerow(tuple(row))
		f.close()
fout.close()