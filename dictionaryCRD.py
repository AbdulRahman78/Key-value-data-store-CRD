import time
import threading
from threading import *
d = dict()
def create(key,values,timeout=0):
	if key in d.keys():
		print("error: This key is already exists")
	else:
		if(key.isalpha()):
			if len(d)<(1024*1024*1024) and values<=(16*1024*1024):
				if timeout==0:
					l = [values,timeout]
				else:
					l = [values,time.time()+timeout]	
				if len(key)<=32:
					print("Data stored in the dictionary with time limit",timeout,"seconds!!!")
					d[key]= l
					
			else:
				print("Error: Memory limits exceed")
		else:
			print("Error: Key name must be alphabets")    	
def read(key):
	if key in d.keys():
		b = d[key]
		if b[1]!=0:
			if time.time()<b[1]:
				stri=str(key)+":"+str(b[0])
				return stri
			else:
				print("Error: Time to live exceeds removed from the dictionary")
		else:
			stri = str(key)+":"+str(b[0])
			return stri
	else:
		print("Key not exists")
def delete(key):
	if key in d.keys():
		b = d[key]
		if b[1]!=0:
			if time.time()<b[1]:
				del d[key]
				print("key is deleted successfully")
			else:
				print("Error: Time to live property is expired no data found in the dictionary")
		else:
			del d[key]
			print("key Delected successfully")	
	else:
		print("Key is not exist")
if __name__ == "__main__": 
	createthread = threading.Thread(target=create,args=[keys,values,timeout])
	deletethread = threading.Thread(target=delete,args=[key])
	readthread = threading.Thread(target= read,args=[Key])

	createthread.start()
	deletethread.start()
	readthread.start()

