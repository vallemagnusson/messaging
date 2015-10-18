#!flask/bin/python

import os
import json
import time
import sys
import time
import shutil
from celery import Celery
from collections import Counter
import urllib2
import subprocess

app = Celery('proj', backend='amqp', broker='amqp://mava:orkarinte@130.238.29.120:5672/app2')

@app.task
def convertFile(fileName, mshFile):
	print "Started to process file: " + str(fileName)
	##########################################
	##### Conver file from *msh to *.xml #####
	##########################################
	if fileName == "r0a0n200.msh":
		newFile = open(fileName, "w")
		newFile.write(mshFile)
		newFile = open(fileName, "r")
		newFile.close()
		fileNameWithoutExtension = os.path.splitext(fileName)[0]
		xmlFileName = fileNameWithoutExtension + ".xml"
		print fileNameWithoutExtension
		#print newFile
		os.system("dolfin-convert " + fileName + " " + xmlFileName)
		#print newFile.read()
		##########################################
		########## Cleaning up dir ###########
		##########################################
		os.mkdir(fileNameWithoutExtension)
		os.copyfile("airfoil", fileNameWithoutExtension+"/airfoil")
		#os.rename(fileName, fileNameWithoutExtension+"/"+fileName)
		#os.rename(xmlFileName, fileNameWithoutExtension+"/"+xmlFileName)

		##########################################
		########## Run airfoil on file ###########
		##########################################
		num = 10
		visc = 0.0001
		speed = 10.
		T = 1
		args = ['mkdir ' + fileNameWithoutExtension,
				'cp -a airfoil ' + fileNameWithoutExtension + '/airfoil',
				'cd ' + fileNameWithoutExtension,
				"./airfoil " + str(num) + " " + str(visc) + " " + str(speed) + " " + str(T) + " " + xmlFileName,
				'cd ..']
		subprocess.Popen(args)
		#os.system("./"+ fileNameWithoutExtension +"/airfoil " + str(num) + " " + str(visc) + " " + str(speed) + " " + str(T) + " " + xmlFileName)
		##########################################
		######### Get drag_ligt.m values #########
		##########################################
		resultLists = readFile(fileNameWithoutExtension+"/results/drag_ligt.m")
		shutil.rmtree(fileNameWithoutExtension)
		return resultLists

@app.task
def readFile(fileName):
	theFile = open(fileName, "r").read()
	timeColumn = []
	liftColumn = []
	dragColumn = []
	lines = open(fileName, "r").readlines()
	for x in range(1, len(lines)):
		time = lines[x].strip().split()[0]
		timeColumn.append(time)
		lift = lines[x].strip().split()[1]
		liftColumn.append(lift)
		drag = lines[x].strip().split()[2]
		dragColumn.append(drag)
	resultList = []
	resultList.append(timeColumn)
	resultList.append(liftColumn)
	resultList.append(dragColumn)
	return resultList








