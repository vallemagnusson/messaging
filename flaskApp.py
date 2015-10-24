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
	print 1, "Starting..."
	print 2,"- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
	urlRequest = urllib2.Request("http://smog.uppmax.uu.se:8080/swift/v1/tweets/")
	tweetFileList = urllib2.urlopen(urlRequest).read().split()
	response = group(getTweets.s(tweetFile) for tweetFile in tweetFileList)
	result = response.apply_async()
	result.get()
	total_dictionary = Counter()
	for t in result.get():
		total_dictionary = total_dictionary + Counter(t)
	stop_time = time.time()
	print 3, "Time used: " + str(stop_time - start_time)
	print 4, "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
	print 5, "... ending"
	return jsonify(total_dictionary), "Time: " + str(stop_time - start_time), 200

if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True )