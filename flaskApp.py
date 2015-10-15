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
#appC = Celery('tasks', backend='amqp', broker='amqp://')
app = Flask(__name__)

@app.route("/messaging", methods=['GET'])
def start():
	print "start"
	print "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
	urlRequest = urllib2.Request("http://smog.uppmax.uu.se:8080/swift/v1/tweets/")
	tweetFileList = urllib2.urlopen(urlRequest).read().split()
	#primes = 1
	#tweets = group(getTweets.s())
	primes = getTweets.delay(tweetFileList)
	print "primes"
	print primes
	print "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
	#print primes.ready()
	print "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
	n = 0
	while primes.ready() == False:
		print "Waited " + str(n) + " seconds"
		#print primes.ready()
		time.sleep(1)
		n += 1
	return jsonify(primes.get()), 200
	print primes.state
	print primes.ready()
	#print primes.get()
	print "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
	#return "hej pa dig", 200
	#return "hello world", 200


if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True )