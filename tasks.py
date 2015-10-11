#!flask/bin/python

import os
import json
import time
import swiftclient.client
import sys
import time
from celery import Celery
from collections import Counter

app = Celery('tasks', backend='amqp', broker='amqp://')

@app.task
def getTweets():
	print "getTweets started"
	config = {'user':os.environ['OS_USERNAME'], 
          'key':os.environ['OS_PASSWORD'],
          'tenant_name':os.environ['OS_TENANT_NAME'],
          'authurl':os.environ['OS_AUTH_URL']}
	print "config set"
	conn = swiftclient.client.Connection(auth_version=2, **config)
	print "conn set"
	#start = time.time()
	dictionary_all = Counter({"han": 0, "hon": 0, "den": 0, "det": 0, "denna": 0, "denne": 0, "hen": 0, "tweet_count": 0})
	(response, bucket_list) = conn.get_account()
	for bucket in bucket_list:
		if bucket['name'] == "tweets":
			#print bucket['name']
			print "bucket found"
			(response, object_list) = conn.get_container(bucket["name"])
			for obj in object_list:
				print "object found"
				if obj["name"] == "tweets_19.txt":
					(response, tweet_file) = conn.get_object(bucket['name'],obj["name"])
					new_file = open("tweets.txt", "w")
					new_file.write(tweet_file)
					new_file.close()
					tweet_file.write()
					print "start read file"
					#print tweet_file
					dictionary_temp = Counter(readJSON(new_file))
					dictionary_all = dictionary_all + dictionary_temp

	return dictionary_all
	return dictionary_temp


@app.task
def readJSON(tweet_file):
	print "in readJSON"
	#print tweet_file
	start_time = time.time()
	JSONFile = open(new_file, "r")
	tweet_count = 0
	dictionary = {"han": 0, "hon": 0, "den": 0, "det": 0, "denna": 0, "denne": 0, "hen": 0}
	print "tweet_count set and dictionary"
	#for line in JSONFile:
	for line in new_file:
		try:
			print line
			data = json.loads(line)
			#print data
			if data["retweet_count"] == 0:
			#	print "its not an retweet!!!"
				tweet_count += 1
				word_list = data["text"].lower().split()
				for i in dictionary.keys():
					if i in word_list:
				#		print "its in the dictionary!!!"
						dictionary[i] += 1
					#	if i == "denne":
						#	print dictionary[i]
		except:
			pass

	stop_time = time.time()
	
	print "- - - - - - - - - - - - - - - - - - - - - - - - - - -"
	print "Number of tweets: " + str(tweet_count)
	print "Time used: " + str(stop_time - start_time)
	print dictionary
	print "- - - - - - - - - - - - - - - - - - - - - - - - - - -"
	dictionary.update({"tweet_count": tweet_count})
	return dictionary
#readJSON()