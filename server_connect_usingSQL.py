import psycopg2
import sys
import pprint
def main():
	conn_string="host='10.72.16.72' dbname='russel'user='russel' password='russel'"
	print "Connection todatabase\n ->%s" %(conn_string)
	conn=psycopg2.connect(conn_string)
	cursor=conn.cursor()
	print "connected\n"
	date=01;
	month=03;
	f=open("records.txt",'w')
	while date<31:
		sql="CREATE TABLE account(TRIP_NO VARCHAR (100) UNIQUE NOT NULL,    LAT VARCHAR (100) NOT NULL,    LONG VARCHAR (100) NOT NULL);"
		cursor.execute(sql)
		records=cursor.fetchall()
		break
'''
		pprint.pprint(records)
		for row in records:
			f.write(str(row[0])+"\n")
		print "gps_data2013"+str(month/10)+str(month%10)+str(date/10)+str(date%10)+" : "+str(len(records))		
		if date==30:
			month+=1
			date=0
		if month==9:
			break
		date+=1
		#raw_input()
'''
		
if __name__=="__main__":
	main() 
