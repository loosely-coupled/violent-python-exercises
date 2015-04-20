import os
from _winreg import *

def ReturnDir():

	dirs=['C:\\Recycler\\', 'C:\\Recycled\\', 'C:\\$Recycle.Bin\\']
	for recycleDir in dirs:
		if os.path.isdir(recycleDir):
			return recycleDir
	return None	

def sid2user(sid):

	try:

		key = OpenKey(HKEY_LOCAL_MACHINE, "SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList" + 
					  "\\" + str(sid))

		(value, dtype) = QueryValueEx(key, 'ProfileImagePath')
		user = value.split('\\')[-1]
		return user

	except:
		return sid

def findRecycled(recycleDir):

	dirList = os.listdir(recycleDir)
	for sid in dirList:

		files = os.listdir(recycleDir + sid)
		user = sid2user(sid)
		
		print '\n[+] Listing Files For User: ' + user
		for filename in files:
			print '[+] Found File: ' + str(filename)

def main():
	recycledDir = ReturnDir()
	findRecycled(recycledDir)

if __name__ == "__main__":
	main()