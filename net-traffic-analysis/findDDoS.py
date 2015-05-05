
import dpkt
import socket
import optparse

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

def findHivemind(pcap):
	"Determine if !lazor command issued"

	for (ts, buf) in pcap:

		try:

			eth = dpkt.ethernet.Ethernet(buf)		#Create an ethernet object from the complete packet
			ip = eth.data							#get data payload of ethernet object
			src = socket.inet_ntoa(ip.src)			#Convert 32-bit packed binary string to dotted-quad string
			dst = socket.inet_ntoa(ip.dst)			#Convert 32-bit packed binary string to dotted-quad string
			tcp = ip.data							#get data payload of IP object
			dport = tcp.dport						#destination port number
			sport = tcp.sport						#source port number

			if dport == 6667:

				if '!lazor ' in tcp.data.lower():	# check if !lazor command issued
					
					print '[!] DDos Hivemind issued by: ' + src
					print '[+] Target CMD: ' + tcp.data

			if sport == 6667:

				if '!lazor' in tcp.data.lower():

					print '[!] DDos Hivemind issued to: ' + src
					print '[+] Target CMD: ' + tcp.data

		except:
			pass

def findAttack(pcap):
	"Determine if DDOS attack in progress"

	pktCount = {}
	for (ts, buf) in pcap:

		try:

			eth = dpkt.ethernet.Ethernet(buf)		#Create an ethernet object from the complete packet
			ip = eth.data							#get data payload of ethernet object
			src = socket.inet_ntoa(ip.src)			#Convert 32-bit packed binary string to dotted-quad string
			dst = socket.inet_ntoa(ip.dst)			#Convert 32-bit packed binary string to dotted-quad string
			tcp = ip.data							#get data payload of IP object
			dport = tcp.dport						#destination port
			
			#Count the number of packets sent from src to dst
			if dport == 80:

				stream = src + ':' + dst
				if pktCount.has_key(stream):
					pktCount[stream] += 1
				else:
					pktCount[stream] = 1

		except:
			pass

	#Give me all the DDOS attacks
	for stream in pktCount:
		pktsSent = pktCount[stream]
		if pktsSent > THRESH :

			src = stream.split(':')[0] 
			dst = stream.split(':')[1]
			print '[+] %s attacked %s with %s pkts' % (src, dst, str(pktsSent))
				 
def main():

	argparser = optparse.OptionParser("usage %prog -p <pcap filepath> -t <thresh>")
	argparser.add_option("-p", dest='pcapFile', type='string')
	argparser.add_option("-t", dest='thresh', type='int')

	(option, args) = argparser.parse_args()
	
	pcapFile = option.pcapFile

	if option.pcapFile == None:
		print argparser.usage
		exit(0)

	if option.thresh != None:
		THRESH = options.thresh


	f = open(pcapFile,'rb')
	pcap = dpkt.pcap.Reader(f)
	findDownload(pcap)
	findHivemind(pcap)
	findAttack(pcap)
	f.close()

if __name__ == '__main__':
	main()