##
# This module analysis pcap files for fast flux occureneces
##
from scapy.all import *

dnsRecords = {}

def handlePkt(pkt):
	"Dns Record handler to store domain name and IP addresses"

	if pkt.haslayer(DNSRR): 					#check if packet is a DNS resource record (reply message)

		rrname = pkt.getlayer(DNSRR).rrname				#get resource record name
		rdata = pkt.getlayer(DNSRR).rdata				#get record IP address

		if dnsRecords.has_key(rrname):					#check if we have stored the domain name
			if rdata not in dnsRecords[rrname]:				#check if we have IP address stored for domain name
				dnsRecords[rrname].append(rdata)				#add IP since we dont have it stored
		else:

			dnsRecords[rrname] = []						#add the domain name
			dnsRecords[rrname].append(rdata)			#add the IP address

def main():

	pkts = rdpcap('CH4/fastFlux.pcap')			#read pcap file
	for pkt in pkts:							#iterate through complete packets
		handlePkt(pkt)								#handle each packet

	for item in dnsRecords:
		print '[+] %s has %s unique IPs.' % (item, str(len(dnsRecords[item])) )			

if __name__ == "__main__":
	main() 