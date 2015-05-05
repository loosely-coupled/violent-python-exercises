
import dpkt
import socket

THRESH = 10000

def findDownload(pcap):
	"Determine if LOIC was intentionally downloaded"

	for (ts, buf) in pcap: #Each iteration returns a tuple which is a tuple and a timestamp. The buffer is the compplete packet

		try:

			eth = dpkt.ethernet.Ethernet(buf)	#Create an ethernet object from the complete packet
			ip = eth.data 						#get data payload of ethernet object
			src = socket.inet_ntoa(ip.src)		#Convert 32-bit packed binary string to dotted-quad string
			tcp = ip.data
			http = dpkt.http.Request(tcp.data)	#create an http object from received string

			if http.method == 'GET':

				uri = http.uri.lower()					#Get Universal resource indicator in lower case
				if '.zip' in uri and 'loic' in uri: 	#Check if zip extension and 'loic' string in uri
					print '[!] ' + src + ' Downloaded LOIC'

		except:
			pass

f = open('CH4/download.pcap', 'rb')
pcap = dpkt.pcap.Reader(f)
findDownload(pcap)