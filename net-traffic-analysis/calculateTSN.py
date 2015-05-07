from scapy.all import *

def calTSN(tgt):
	"Returns predicted next Sequence number"

	seqNum = 0
	preNum = 0
	diffSeq = 0

	for x in range(1, 5):

		if preNum != 0:
			preNum = seqNum

		pkt = IP(dst=tgt) / TCP()
		ans = sr1(pkt, verbose=0)
		seqNum = ans.getlayer(TCP).seq
		diffSeq = seqNum - preNum
		print '[+] TCP Seq number difference: ' + str(diffSeq)

	return seqNum + diffSeq

tgt = "10.20.14.205"
seqNum = calTSN(tgt)
print "[+] Next TCP Sequence number to ACk is: " + str(seqNum + 1)