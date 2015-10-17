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

app = Flask(__name__)

@app.route("/messaging", methods=['GET'])
def start():
	start_time = time.time()
	print "Starting..."
	print "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
	urlRequest = urllib2.Request("http://smog.uppmax.uu.se:8080/swift/v1/tweets/")
	tweetFileList = urllib2.urlopen(urlRequest).read().split()
	#primes = getTweets.delay(tweetFileList)
	#responseList = []
	#for tweetFile in tweetFileList:
	#	responseList.append(getTweets.delay([tweetFile]))
	response = group(getTweets.subtask(tweetFile) for tweetFile in tweetFileList).apply_async()
	n = 0
	#print responseList
	while response.ready() == False:
		time.sleep(1)
	#get = [t.get() for t in responseList]
	response.get()
	total_dictionary = Counter({})
	#for t in get:
	for t in response:
		total_dictionary.update(t)
	stop_time = time.time()
	print "Time used: " + str(stop_time - start_time)
	print "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
	print "... ending"
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