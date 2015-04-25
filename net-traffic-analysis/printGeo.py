import pygeoip

gi = pygeoip.GeoIP('data/GeoLiteCity.dat')

def printRecord(tgt):

	rec = gi.record_by_name(tgt)
	print rec.keys()
	city = rec['city']
	region = rec['region_code']
	country = rec['country_name']
	longitude = rec['longitude']
	latitude = rec['latitude']

	print '[*] Target: %s Geolocated' % tgt
	print '[+] %s, %s, %s' % (str(city), str(region), str(country))
	print '[+] Latitude: %s, Longitude: %s' % (latitude, longitude)

tgt = '173.255.226.98'
printRecord(tgt)