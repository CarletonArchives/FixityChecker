import os
import sys
import hashlib


try:
	index=int(sys.argv[2])
	maxcount=int(sys.argv[3])
	top=sys.argv[1]
	print top
except:
	print "Bad args"
	sys.exit()
manifests =[]
out=open("CorruptedFiles.txt","w")
try:
	for dirpath,dirnames,filenames in os.walk(top):
		if "manifest-md5.txt" in filenames:
			for name in filenames:
				if("manifest-md5.txt" in name):
					manifests.append((dirpath+"/",name))
except:
	print "Failed to generate manifest list from start directory given"
	sys.exit()
count =0
for temp in manifests:
	startpath=temp[0]
	manifest=open(startpath+temp[1],"rb")
	for line in manifest:
		count=(count+1)%maxcount
		if(count==index):
			line= line[:-1]
			line= line.partition(" ")
			if(line[2][0]==" "):
				filename=line[2][1:]
			else:			
				filename=line[2]
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
					print filename+" is valid"
				else:
					out.write(startpath+filename+"\n")
			except:
				out.write(startpath+filename+"\n")
out.close()
