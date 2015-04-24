##
#This module parses firefox sqlite database file to extract certain information from it.
#The specific information extracted are: downloads, Cookies, History, search terms
##



import sqlite3
import optparse
import os
import re

def printDownloads(downloadDB):

	conn = sqlite3.connect(downloadDB)
	c = conn.cursor()
	c.execute('SELECT content, datetime((dateAdded/1000000), \'unixepoch\') FROM moz_annos;')
	print '\n[*] --- Files Downloaded ---'

	for row in c:
		print '[+] File: ' + str(row[0]) + ' at: ' + str(row[1])

def printCookies(cookiesDB):

	try:

		conn = sqlite3.connect(cookiesDB)
		c = conn.cursor()
		c.execute('SELECT baseDomain, name, value FROM moz_cookies')
		print '\n[*] ---Found Cookies ----'

		for row in c:

			host = str(row[0])
			name = str(row[1])
			value = str(row[2])
			print'[+] Host: %s, Cookie: %s, Value: %s' % (host, name, value)

	except Exception, e:

		if 'encrypted' in str(e) :

			print "\n[*] Error reading you cookies database"
			print "Please try update your python-sqlite3 library"

def printHistory(placesDB):

	try:

		conn = sqlite3.connect(placesDB)
		c = conn.cursor()
		c.execute('SELECT url, datetime(last_visit_date/1000000, \'unixepoch\') from moz_places')
		print '\n[*] ---Found Cookies ---'

		for row in c:

			url = str(row[0])
			date = str(row[1])
			print '[+] %s date Visited : %s' % (date, url)

	except Exception, e:

		if 'encrypted' in str(e) :

			print "\n[*] Error reading you places database"
			print "Please try update your python-sqlite3 library"

def printGoogle(placesDB):

	try:

		conn = sqlite3.connect(placesDB)
		c = conn.cursor()
		c.execute('SELECT url, datetime(last_visit_date/1000000, \'unixepoch\') from moz_places')
		print '\n[*] ---Found Google searches ---'
		for row in c:

			url = str(row[0])
			date = str(row[1])

			if 'google' in url.lower():

				r = re.findall(r'q=.*\&', url)
				if r:

					search = r[0].split('&')[0]
					search = search.replace('q=','').replace('+', ' ')
					print '[+] %s Searched for : %s' % (date, search)

	except Exception, e:

		if 'encrypted' in str(e) :

			print "\n[*] Error reading you places database"
			print "Please try update your python-sqlite3 library"


def main():

	parser = optparse.OptionParser('usage %prog -d <directory to firefox profile path> ')
	parser.add_option('-d', dest='DbDir', type='string', help='specify directory to firefox cookies.sqlite')

	(option, args) = parser.parse_args()
	DbDir = option.DbDir

 	if DbDir == None:

 		print parser.usage
 		exit(0)

 	elif os.path.isdir(DbDir) == False:

 		print '[!] Path Does Not Exist: ' + pathname
 		exit(0)

	cookiesDB = os.path.join(DbDir, 'cookies.sqlite')
	if os.path.isfile(cookiesDB):
		printCookies(cookiesDB)
	else:
		print "[!] cookies.sqlite not Found"

	placesDB = os.path.join(DbDir, 'places.sqlite')
	if os.path.isfile(placesDB):
		printDownloads(placesDB)
		printHistory(placesDB)
		printGoogle(placesDB)
	else:
		print "[!] places.sqlite not Found"


if __name__ == "__main__":
	main()