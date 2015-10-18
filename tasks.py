#!flask/bin/python

import os
import json
import time
#import swiftclient.client
import sys
import time
from celery import Celery
from collections import Counter
import urllib2

app = Celery('tasks', backend='amqp', broker='amqp://mava:orkarinte@130.238.29.120:5672/app2')

@app.task
def getTweets(tweetFileList):
	dictionary_all = {}
	for tweetFile in tweetFileList:
		print "getTweets started with tweetfile: " + str(tweetFile)
		urlRequest = urllib2.Request("http://smog.uppmax.uu.se:8080/swift/v1/tweets/" + tweetFile)
		urlResponse = urllib2.urlopen(urlRequest).read()
		new_file = open(tweetFile, "w")
		new_file.write(urlResponse)
		new_file.close()
		dictionary_all = readJSON(tweetFile)
		os.remove(tweetFile)
	return dictionary_all

@app.task
def readJSON(tweet_file):
	start_time = time.time()
	JSONFile = open(tweet_file, "r")
	tweet_count = 0
	dictionary = {"han": 0, "hon": 0, "den": 0, "det": 0, "denna": 0, "denne": 0, "hen": 0}
	for line in JSONFile:
		try:
			data = json.loads(line)
			if data["retweet_count"] == 0:
				tweet_count += 1
				word_list = data["text"].lower().split()
				for i in dictionary.keys():
					if i in word_list:
						dictionary[i] += 1
		except:
			pass
	stop_time = time.time()
	dictionary.update({"tweet_count": tweet_count})
	return dictionary
