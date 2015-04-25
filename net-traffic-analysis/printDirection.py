##
#This module determines the direction of packets in a pcap file, from souce IP to destination IP
##
import dpkt, pygeoip
import socket, optparse

def printPcap(pcap):

	for (ts, buf) in pcap:
		try:

			eth = dpkt.ethernet.Ethernet(buf)
			ip = eth.data
			src = socket.inet_ntoa(ip.src)
			dst = socket.inet_ntoa(ip.dst)

			print '[+] Src: %s --> Dst: %s' % (src, dst)
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