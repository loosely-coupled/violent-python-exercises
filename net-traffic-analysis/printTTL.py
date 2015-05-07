
from scapy.all import *

def testTTL(pkt):

	try:

		if pkt.haslayer(IP):				#check if IP Layer exist

			ipsrc = pkt.getlayer(IP).src	#Get src IP address from IP layer
			ttl = str(pkt.ttl)				#Get ttl from pkt
			print '[+] Pkt Received From: %s with TTL: %s' % (ipsrc, ttl)

	except:
		pass

def main():

	sniff(prn=testTTL, store=0) #sniff packets with tetTTL as callback function?


if __name__ == '__main__':
	main()