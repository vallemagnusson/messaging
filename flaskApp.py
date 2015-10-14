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
#from collections import Counter
#appC = Celery('tasks', backend='amqp', broker='amqp://')
app = Flask(__name__)

config = {'user':os.environ['OS_USERNAME'], 
          'key':os.environ['OS_PASSWORD'],
          'tenant_name':os.environ['OS_TENANT_NAME'],
          'authurl':os.environ['OS_AUTH_URL']}

@app.route("/messaging", methods=['GET'])
def start():
	print "start"
	print "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
	#primes = 1
	tweets = group(getTweets.s(), getTweets.s())
	primes = tweets.apply_async()
	print "primes"
	print primes
	print "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
	#print primes.ready()
	print "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
	n = 0
	while primes.ready() == False:
		print "Waited " + str(n) + " seconds"
		time.sleep(1)
	#	n += 1
	#return primes.get()
	print "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
	return "hej pa dig"
	#return "hello world", 200


if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True )