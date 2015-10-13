#!flask/bin/python
from celery import Celery
from celery import group
from flask import Flask, jsonify
import subprocess
import sys
import os
import swiftclient.client
import json
import time
from collections import Counter

app = Flask(__name__)

@app.route("/", methods=['GET'])
def start():
	#return "hello world", 200
	print "start"
	print "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
	primes = getTweets.delay()
	print primes
	print "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
	print primes.ready()
	print "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
	while primes.ready() == False:
		time.delay(5)
	print primes.get()
	print "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"


if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)
