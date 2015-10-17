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
import pika

app = Flask(__name__)

@app.route("/messaging", methods=['GET'])
def start():
	connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
	channel = connection.channel()

	channel.queue_declare(queue='task_queue', durable=True)
	print ' [*] Waiting for messages. To exit press CTRL+C'

	def callback(ch, method, properties, body):
	    print " [x] Received %r" % (body,)
	    time.sleep( body.count('.') )
	    print " [x] Done"
	    ch.basic_ack(delivery_tag = method.delivery_tag)

	channel.basic_qos(prefetch_count=1)
	channel.basic_consume(callback, queue='task_queue')

	channel.start_consuming()

	start_time = time.time()
	print 1, "Starting..."
	print 2,"- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
	urlRequest = urllib2.Request("http://smog.uppmax.uu.se:8080/swift/v1/tweets/")
	tweetFileList = urllib2.urlopen(urlRequest).read().split()
	#primes = getTweets.delay(tweetFileList)
	#responseList = []
	#for tweetFile in tweetFileList:

	#print 1, tweetFileList
	response = group(getTweets.s([tweetFile]) for tweetFile in tweetFileList)
	#print 2, response
	result = response.apply_async()
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
	print 4, "Time used: " + str(stop_time - start_time)
	print 5, "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
	print 6, "... ending"
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