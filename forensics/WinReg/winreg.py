import mechanize, urllib, re, urlparse
from _winreg import *

def val2addr(val):

	addr = ""
	for ch in val:
		addr+= ("%02x "% ord(ch))
	addr = addr.strip(" ").replace(" ",":")[0:17]
	return addr

def printNets(username, password):

	net = "SOFTWARE\Microsoft\Windows NT\CurrentVersion" +\
		"\NetworkList\Signatures\Unmanaged"
	key = OpenKey(HKEY_LOCAL_MACHINE, net, 0, KEY_READ | KEY_WOW64_64KEY)
	print '\n[*] Networks You have Joined.'
	
	for i in range(100):

		try:
			
			guid = EnumKey(key, i)
			netKey = OpenKey(key, str(guid))
			(n, addr, t) = EnumValue(netKey, 5)
			(n, name, t) = EnumValue(netKey, 4)
			macAddr = val2addr(addr)
			netName = str(name)
			print'[+] ' + netName + ', ' + macAddr
			wiglePrint(username, password, macAddr)
			CloseKey(netKey)
		
		except:
			pass

def wiglePrint(username, password, netid):

	browser = mechanize.Browser()
	browser.open('http://wigle.net')
	reqData = urllib.urlencode({'credential_0': username, 'credential_1':password} )
	print browser.open('https://wigle.net/gps/gps/main/login', reqData).read()
	params = {}
	params['netid'] = netid
	reqParams = urllib.encode(params)
	respURL = 'http://wigle.net/gps/gps/main/confirmquery/'
	resp = browse.open(respUrl, reqParams).read()
	mapLat = 'N/A'
	mapLon = 'N/A'
	print resp
	rLat = re.findall(r'maplat=.*\&', resp)
	if rLat:
		mapLat = rLat[0].split('&')[0].split('=')[1]

	rLong = re.findall(r'maplon=.*\&', resp)
	if rLon:
		mapLon = rLon[0].split
	print '[-] Lat: ' + mapLat + ', Lon: ' + mapLon

def main():
		
	printNets("Reishi91", "Penguin008wgl")

if __name__ == "__main__":
	main()


