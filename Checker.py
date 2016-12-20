import os
import sys
import hashlib
import random
import time
import datetime
#Arguments: Directory Interval Offset
#Checks all files with the given Interval from the given Offset. Default is every 10th file with random offset.

try:

	top=sys.argv[1]
	print top
except:
	print "Bad args. Normal usage is python Checker.py Directory (Interval) (Offset)"
	sys.exit()
index=False
try:
	if(sys.argv[2][0]!='o'):
		maxcount=int(sys.argv[2])
	else:
		maxcount=10
		try:
			index=int(sys.argv[2][1:])
		except:
			index==False
			pass
except:
	if(len(sys.argv)<3):
		maxcount=10
	else:
		print "Bad Interval. Normal usage is python Checker.py Directory (Interval) (Offset)"
		print "Checks all files with the given Interval from the given Offset. Default is every 10th file with random offset."
		sys.exit()
try:
	if(index==False):
		index=int(sys.argv[3])
except:
	if(index==False and len(sys.argv)<4):
		index=random.randint(0,maxcount-1)
	else:
		print "Bad Offset. Normal usage is python Checker.py Directory (Interval) (Offset)"
		print "Checks all files with the given Interval from the given Offset. Default is every 10th file with random offset."
		sys.exit()
manifests =[]
path=os.path.abspath(sys.argv[0])

path=path.replace("Checker.py","")
try:
	os.chdir(path+"logs")
	os.chdir(path)
except:
	os.mkdir(path+"logs")

#Load exceptions from exceptions.txt
exceptions=[]
try:
	exceptionfile=open(path+"exceptions.txt","r")
	for exception in exceptionfile:
		if(exception[-1]!="\n"):
			exceptions.append(exception)
		else:
			exceptions.append(exception[:-1])
except:
	pass

#Open timestamped errorlog
out=open(path+"logs/errors"+datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d_%H:%M:%S")+".txt","w")
try:
	for dirpath,dirnames,filenames in os.walk(top):
		if "manifest-md5.txt" in filenames:
			for name in filenames:
				if("manifest-md5.txt" == name):
					manifests.append((dirpath+"/",name))
except:
	print "Failed to generate manifest list from start directory given"
	sys.exit()
count =0
valid=0
invalid=0
total=0
for temp in manifests:
	startpath=temp[0]
	print ("\nChecking manifest "+startpath+temp[1])
	manifest=open(startpath+temp[1],"rb")
	for line in manifest:
		line= line[:-1]
		line= line.partition(" ")
		if(line[2][0]==" "):
			filename=line[2][1:]
		else:			
			filename=line[2]
		exit=False
		for exceptionname in exceptions:
			if(exceptionname.lower() in filename.lower()):
				exit=True
		if(exit):
			continue
		count=(count+1)%maxcount
		if(count==index):

			total+=1
			if(filename[-1]=='\r'):
				filename=filename[:-1]
				out.write("Warning: "+startpath+temp[1]+" has Windows formatting\n")
			try:
				f=open(startpath+filename,"rb")
				h=hashlib.md5()		
				while True:
					block=f.read(1048576)
					if not block:
						break
					h.update(block)
				f.close()
				a=""
				for i in h.digest():
					a+=format(ord(i),'02x')
				if a==line[0]:
					valid+=1
				else:
					print(filename+" is invalid")
					invalid+=1
					out.write("Verification failed for "+startpath+filename+": Checksum does not match the manifest \n")
			except:
				print(filename+" is invalid\n")
				invalid+=1
				out.write("Verification failed for "+startpath+filename+": Error opening file \n")
out.write(str(valid)+" out of "+str(total)+" files valid\n")
out.write(str(invalid)+" out of "+str(total)+" files invalid\n")
print str(valid)+" out of "+str(total)+" files valid"
print str(invalid)+" out of "+str(total)+" files invalid"
out.close()
