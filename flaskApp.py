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
	print "Starting..."
	print "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
	urlRequest = urllib2.Request("http://smog.uppmax.uu.se:8080/swift/v1/tweets/")
	print 1
	tweetFileList = urllib2.urlopen(urlRequest).read().split()
	print 2
	#primes = getTweets.delay(tweetFileList)
	responseList = []
	print 3
	for tweetFile in tweetFileList:
		print 4
		responseList.append(getTweets.delay([tweetFile]))
		print 5
	n = 0
	print responseList
	print 6

	get = [t.get() for t in responseList]
	print 7

	total_dictionary = Counter({})
	print 8
	for t in get:
		total_dictionary.update(t)

	return total_dictionary
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
	print "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
	print "... ending"
	#return "hej pa dig", 200
	#return "hello world", 200


if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True )