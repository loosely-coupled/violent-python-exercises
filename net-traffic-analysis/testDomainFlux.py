##
# This module determines all failed DNS lookups.
# Failed dns lookups hint towared Domain-flux.
##
from scapy.all import *

def dnsQRTest(pkt):
	"Determine if DNS lookup failed"

	if pkt.haslayer(DNSRR) and pkt.getlayer(UDP).sport == 53:

		rcode = pkt.getlayer(DNS).rcode
		qname = pkt.getlayer(DNSQR).qname

		if rcode == 3:			#rcode of 3 indicates domain name does not exist

			print '[!] Name Request lookup failed: ' + qname
			return True

		else:
			return False

def main():

	unAnsReqs = 0
	pkts = rdpcap('CH4/domainFlux.pcap')
	
	for pkt in pkts:				#iterate through all pcap complete packets
		if dnsQRTest(pkt):				#test if failed DNS query
			unAnsReqs += 1

	print '[!] %s Total Unanswered Name Requests' % str(unAnsReqs)

if __name__ == "__main__":
	main()