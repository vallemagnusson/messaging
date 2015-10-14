#!flask/bin/python
from celery import Celery
from flask import Flask
import subprocess
import sys
import os
import swiftclient.client
import time

app = Flask(__name__)

@app.route("/", methods=['GET'])
def start():
	return "hello world", 200
	print "start"
	print "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
	#primes = 1
	#primes = getTweets.delay()
	print "primes"
	#print primes
	print "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
	#print primes.ready()
	print "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
	#while primes.ready() == False:
	#	time.delay(5)
	#print primes.get()
	print "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
	#return "hej pa dig"


if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)