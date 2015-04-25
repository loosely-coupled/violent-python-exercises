import dpkt, pygeoip
import socket, optparse

gi = pygeoip.GeoIP('data/GeoLiteCity.dat') # Object to convert IP to geolocation


def retKml(ip):
	"format ip to kml format"

	rec = gi.record_by_name(ip)
	try:
		longitude = rec['longitude']
		latitude = rec['latitude']

		kml = (
			'<Placemark>\n'
			'<name>%s</name>\n'
			'<Point>\n'
			'<coordinates>%6f,%6f</coordinates>\n'
			'</Point>\n'
			'</Placemark>\n'
			) % (ip, longitude, latitude)

		return kml
	except:
		return ''

def plotIPs(pcap):

	kmlPts = ''
	for (ts, buf) in pcap:
		try:

			eth = dpkt.ethernet.Ethernet(buf)
			ip = eth.data
			src = socket.inet_ntoa(ip.src)
			dst = socket.inet_ntoa(ip.dst)
			srcKml = retKml(src)
			dstKml = retKml(dst)
			kmlPts = kmlPts + srcKml + dstKml
		except Exception, e:
			pass

	return kmlPts

def main():

	argparser = optparse.OptionParser("usage %prog -p <pcap filepath>")
	argparser.add_option("-p", dest='pcapFile', type='string')

	(option, args) = argparser.parse_args()
	if option.pcapFile == None:
		print argparser.usage
		exit(0)

	pcapFile = option.pcapFile

	f = open(pcapFile, 'rb')
	pcap = dpkt.pcap.Reader(f)
	
	kmlheader = '<?xml version="1.0" encoding="UTF-8"?>\
				\n<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n'
	kmlfooter = '</Document>\n</kml>'
	kmldoc = kmlheader + plotIPs(pcap) + kmlfooter
	
	f = open("mykml.kml", 'wb')
	f.write(kmldoc)
	f.close()

if __name__ == "__main__":
	main()