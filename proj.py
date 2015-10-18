#!flask/bin/python

import os
import json
import time
#import swiftclient.client
import sys
import time
from celery import Celery
from collections import Counter
import urllib2

app = Celery('proj', backend='amqp', broker='amqp://mava:orkarinte@130.238.29.120:5672/app2')

@app.task
def convertFile(fileName, mshFile):
	print "Started to process file: " + str(fileName)
	#print fileName
	if fileName == "r0a0n200.msh":
		newFile = open(fileName, "w")
		newFile.write(mshFile)
		newFile = open(fileName, "r")
		newFile.close()
		fileNameWithoutExtension = os.path.splitext(fileName)[0]
		xmlFileName = fileNameWithoutExtension + ".xml"
		print fileNameWithoutExtension
		print newFile
		os.system("dolfin-convert " + fileName + " " + xmlFileName)
		#print newFile.read()
		
	return "dictionary_all"

@app.task
def readJSON(tweet_file):
	return "dictionary"


#################################################################
#mshDir = os.listdir("msh")
#for filename in mshDir:
#	filenameNoExtension = os.path.splitext(filename)[0]
#	oldFile = "msh/"+str(filename)
#	newFile = "msh/" + filenameNoExtension + ".xml"
#	os.system("dolfin-convert " + oldFile + " " + newFile)
#


#dolfin-convert cylinder6.msh out.xml