import time
import threading
import pymongo
from pymongo import MongoClient
import threading 
mydb = MongoClient("mongodb://127.0.0.1:27017/gssapiServiceName=mongodb")
db = mydb["freshworks"]
collection = db["crd"]
def create(key,values,timeout=0):
	cursor=collection.find()
	b=[x for x in cursor]
	if collection.find({key: {"$exists": True}}).count() > 0:
			print("Error: This key is already exists")
	else:
		if(key.isalpha()):
			if len(b)<(1024*1024*1024) and values<=(16*1024*1024):
				if timeout==0:
					l = [values,timeout]
				else:
					l = [values,time.time()+timeout]
						
				if len(key)<=32:
					print("Data stored with time limit",timeout,"seconds!!!")
					collection.insert_one({key:l})
					
			else:
				print("Error: Memory limits exceed")
		else:
			print("Error: Key name must be alphabets")    	
def read(key):
	cursor=collection.find({key: {"$exists": True}})
	if  cursor.count() > 0:
		b= [x for x in cursor][0][key]

		if b[1]!=0:
			if time.time()<b[1]:
				stri=str(key)+":"+str(b[0])
				return stri
			else:
				db.crd.remove({key:b})
				print("Error: Time to live exceeds removed from the database")
		else:
			stri = str(key)+":"+str(b[0])
			return stri
	else:
		print("Key not exists")
def delete(key):
	cursor=collection.find({key: {"$exists": True}})
	if cursor.count()>0:
		b= [x for x in cursor][0][key]
		if b[1]!=0:
			if time.time()<b[1]:
				db.crd.remove({key:b})
				print("key is deleted successfully")
			else:
				print("Error: Time to live property is expired no data found in the database")
		else:
			db.crd.remove({key:b})
			print("key Deleted successfully")
	else:
		print("Key is not exist")

if __name__ == "__main__": 
	createthread = threading.Thread(target=create,args=[keys,values,timeout])
	deletethread = threading.Thread(target=delete,args=[key])
	readthread = threading.Thread(target= read,args=[Key])

	createthread.start()
	deletethread.start()
	readthread.start()

