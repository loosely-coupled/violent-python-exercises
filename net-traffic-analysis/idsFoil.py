from scapy.all import *

def ddosTest(src, dst, iface, count):

	pkt = IP(src=src, dst=dst) / ICMP(type=8, id=678) / Raw(load='1234')
	send(pkt, iface=iface, count=count)
	pkt = IP(src=src, dst=dst) / ICMP(type=0) / Raw(load='AAAAAAAAA')
	send(pkt, iface=iface, count=count)
	pkt = IP(src=src, dst=dst) / UDP(dport=3133)/ Raw(load='PONG')
	send(pkt, iface=iface, count=count)
	pkt = IP(src=src, dst=dst) / ICMP(type=0, id=456)
	send(pkt, iface=iface, count=count)

def exploitTest(src, dst, iface, count):

	pkt = IP(src=src, dst=dst) / UDP(dport=518) / Raw(load="\x01\x03\x00\x00\x00\x00\x00\x01\x00\x02\x02\xE8")
	send(pkt, iface=iface, count=count)
	pkt = IP(src=src, dst=dst) / UDP(dport=635) / Raw(load="\xB0\x02\x89\x06\xFE\xC8\x89F\x04\xB0\x06\x89F")

def scanTest(scr, dst, iface, count):

	pkt = IP(src=src, dst=dst) / UDP(dport=7) / Raw(load='cybercop')
	send(pkt)
	pkt = IP(src=src, dst=dst) / UDP(dport=10080) / Raw(load='Amanda')
	send(pkt)

src =  "10.0.2.15"
dst = "10.0.0.3"
iface = "eth0"
count = 1

ddosTest(src, dst, iface, count)
exploitTest(src, dst, iface, count)