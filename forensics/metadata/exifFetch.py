import urllib2
import optparse
from bs4 import BeautifulSoup
from urlparse import urlsplit
from os.path import basename
from PIL import Image
from PIL.ExifTags import TAGS


def findImages(url):

	print '[+] Finding images on ' + url
	urlContent = urllib2.urlopen(url).read()
	soup = BeautifulSoup(urlContent)
	imgTags = soup.findAll('img')
	return imgTags


def downloadImage(imgTag):

	try:

		print '[+] Downloading Image...'
		imgSrc = imgTag['src']
		print imgSrc
		imgContent = urllib2.urlopen(imgSrc).read()
		imgFileName = basename(urlsplit(imgSrc)[2])
		imgFile = open(imgFileName, 'wb')
		imgFile.write(imgContent)
		imgFile.close()
		return imgFileName

	except Exception, e:
		import traceback, os.path
    	top = traceback.extract_stack()[-1]
    	print ', '.join([type(e).__name__, os.path.basename(top[0]), str(top[1])])

def testForExif(imgFileName):

	try:
		
		print "[+] Testing for exif Metadata"
		exifData = {}
		imgFile = Image.open(imgFileName)
		info = imgFile._getexif()
		if info:
			for (tag, value) in info.items():

				decoded = TAGS.get(tag, tag)
				exifData[decoded] = value
			
			exifGPS = exifData['GPSInfo']
				
			if exifGPS:
				print '[*] ' + str(imgFileName) + ' contains GPS MetaData'
			else:
				print '[-] NO GPS data found'
		else:
				print '[-] NO  data found'



	except Exception, e:
		print "[-] Error : " + str(e)


def main():
 
 	parser = optparse.OptionParser('usage %prog -u <target url>')
 	parser.add_option('-u', dest='url', type='string', help='specify target url')

 	(option, args) = parser.parse_args()
 	url = option.url

 	if url == None:

 		print parser.usage
 		exit(0)

 	imgTags = findImages(url)
 	for imgTag in imgTags:

 		imgFileName = downloadImage(imgTag)
 		testForExif(imgFileName)

if __name__ == '__main__':
 	main()