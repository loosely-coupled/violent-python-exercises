#This is firefox recon script from Violent python.
#needed to replace the sqlite3.dll with latest one from sqlite.org.
#This is becaused I assumed firefox is using sqlite with WAL.
#http://stackoverflow.com/questions/11456623/using-an-sqlite3-database-with-wal-enabled-python


import sqlite3
import os
import optparse

def printDownloads(downloadDB):

	conn = sqlite3.connect(downloadDB)
	c = conn.cursor()
	c.execute('SELECT content, datetime((dateAdded/1000000), \'unixepoch\') FROM moz_annos;')
	print '\n[*] --- Files Downloaded ---'

	for row in c:
		print '[+] File: ' + str(row[0]) + ' at: ' + str(row[1])

def main():

 	parser = optparse.OptionParser('usage %prog -d <directory to firefox places.sqlite>')
 	parser.add_option('-d', dest='DbDir', type='string', help='specify directory to firefox places.sqlite')

 	(option, args) = parser.parse_args()
 	DbDir = option.DbDir

 	if DbDir == None:

 		print parser.usage
 		exit(0)

 	elif os.path.isdir(DbDir) == False:

 		print '[!] Path Does Not Exist: ' + pathname
 		exit(0)

 	placesDB = os.path.join(DbDir, 'places.sqlite')

 	if os.path.isfile(placesDB):
 		printDownloads(placesDB)
 	else:
 		print "[!] places.sqlite not Found"
if __name__ == "__main__":
	main()