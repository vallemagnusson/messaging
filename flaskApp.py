#!flask/bin/python
from celery import Celery
from celery import group
from flask import Flask, jsonify
from tasks import getTweets
import subprocess
import sys
import os
import swiftclient.client
import json
import time
from collections import Counter
import urllib2
from celery.task.control import inspect

app = Flask(__name__)

@app.route("/messaging", methods=['GET'])
def start():
	start_time = time.time()
	print 1, "Starting..."
	print 2, "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
	urlRequest = urllib2.Request("http://smog.uppmax.uu.se:8080/swift/v1/tweets/")
	tweetFileList = urllib2.urlopen(urlRequest).read().split()
	#primes = getTweets.delay(tweetFileList)
	#responseList = []
	#for tweetFile in tweetFileList:

	#print 1, tweetFileList
	response = group(getTweets.s([tweetFile]) for tweetFile in tweetFileList)
	#print 2, response
	result = response.apply_async()
	i = inspect()
	if result.ready() == False:
		print 3, i
		print 4, i.scheduled()
		print 5, i.active()
	#print 3, response.apply_async()
	#n = 0
	#print responseList
	#print response.ready()
	#while response.ready() == False:
	#	time.sleep(1)
	#get = [t.get() for t in responseList]
	result.get()
	#print 2, result.get()
	#print 3, result
	total_dictionary = Counter()
	#for t in get:
	for t in result.get():
		total_dictionary = total_dictionary + Counter(t)
	stop_time = time.time()
	print 6, "Time used: " + str(stop_time - start_time)
	print 7, "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
	print 8, "... ending"
	return jsonify(total_dictionary), 200
	#print responseList
	
	#for test in responseList:
	#	total_dictionary = Counter(test)

	#while primes.ready() == False:
	#	print "Waited " + str(n) + " seconds"
	#	#print primes.ready()
	#	time.sleep(5)
	#	n += 5
	#return jsonify(total_dictionary), 200
	#print primes.state
	#print primes.ready()
	#print primes.get()
	
	#return "hej pa dig", 200
	#return "hello world", 200


if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True )