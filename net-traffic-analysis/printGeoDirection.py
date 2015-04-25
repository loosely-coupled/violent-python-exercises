##
#This module extends the printDirection module to give geographical address 
#rather than IP for src and dst.
##
import dpkt, pygeoip
import socket, optparse

def retGeoStr(tgt):

	try: 
		
		rec = gi.record_by_name(tgt)
		city = rec['city']
		country = rec['country_name']

		if city != '':
			geoLoc = "%s, %s" % (city, country)
		else:
			geoLoc = country
		
		return geoLoc			

	except Exception, e:
		return "Unregistered" 


def printPcap(pcap):

	for (ts, buf) in pcap:
		try:

			eth = dpkt.ethernet.Ethernet(buf)
			ip = eth.data
			src = socket.inet_ntoa(ip.src)
			dst = socket.inet_ntoa(ip.dst)

			print '[+] Src: %s --> Dst: %s' % (retGeoStr(src), retGeoStr(dst))
		except Exception, e:
			print str(e)
			pass

gi = pygeoip.GeoIP('data/GeoLiteCity.dat')

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
	printPcap(pcap)

if __name__ == "__main__":
	main()