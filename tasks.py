#!flask/bin/python

import os
import json
import time
import swiftclient.client
import sys
import time
from celery import Celery
from collections import Counter
import urllib2

app = Celery('tasks', backend='amqp', broker='amqp://')

@app.task
def getTweets():
	start_time_getTweets = time.time()
	print "getTweets started"
	#config = {'username':os.environ['OS_USERNAME'], 
    #      'key':os.environ['OS_PASSWORD'],
    #      'tenant_name':os.environ['OS_TENANT_NAME'],
    #      'authurl':os.environ['OS_AUTH_URL']}
	#print "config set"
	#conn = swiftclient.client.Connection(auth_version=2, **config)
	#print "conn set"
	#start = time.time()
	dictionary_all = Counter({"han": 0, "hon": 0, "den": 0, "det": 0, "denna": 0, "denne": 0, "hen": 0, "tweet_count": 0})
	#(response, bucket_list) = conn.get_account()
	urlRequest = urllib2.Request("http://smog.uppmax.uu.se:8080/swift/v1/tweets/")
	tweetFileList = urllib2.urlopen(urlRequest).read().split()
	for tweetFile in tweetFileList:
	#for bucket in bucket_list:
		#if bucket['name'] == "tweets":
			#print bucket['name']
			#print "bucket found"
			#(response, object_list) = conn.get_container(bucket["name"])
			#for obj in object_list:
				#print "object found"
			#	if tweetFile == "tweets_19.txt": # or obj["name"] == "tweets_18.txt":
					print "- - - - - - - - - " + tweetFile + " - - - - - - - - -"
					start_time_download_file = time.time()
					#(response, tweet_file) = conn.get_object(bucket['name'],obj["name"])
					urlRequest = urllib2.Request("http://smog.uppmax.uu.se:8080/swift/v1/tweets/" + tweetFile)
					urlResponse = urllib2.urlopen(urlRequest).read()
					stop_time_download_file = time.time()

					print "Time to download file: " + str(stop_time_download_file - start_time_download_file)

					start_time_write_file = time.time()
					new_file = open(tweetFile, "w")
					new_file.write(urlResponse)
					new_file.close()
					stop_time_write_file = time.time()

					print "Time to write to file: " + str(stop_time_write_file - start_time_write_file)

					#print tweet_file
					start_time_parse_file = time.time()
					dictionary_temp = Counter(readJSON(tweetFile))
					stop_time_parse_file = time.time()
					print "Time to parse file: " + str(stop_time_parse_file - start_time_parse_file)
					dictionary_all = dictionary_all + dictionary_temp
					os.remove(tweetFile)
					print "Total time for file: " + str(stop_time_parse_file - start_time_download_file)

	stop_time_getTweets = time.time()
	print "All done!!!"
	print "Total time was: " + str(stop_time_getTweets - start_time_getTweets)
	print dictionary_all
	return "dictionary_all"

@app.task
def readJSON(tweet_file):
	#print "in readJSON"
	#print tweet_file
	start_time = time.time()
	JSONFile = open(tweet_file, "r")
	tweet_count = 0
	dictionary = {"han": 0, "hon": 0, "den": 0, "det": 0, "denna": 0, "denne": 0, "hen": 0}
	#print "tweet_count set and dictionary"
	for line in JSONFile:
	#for line in new_file:
		try:
			#print line
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
	
	#print "- - - - - - - - - - - - - - - - - - - - - - - - - - -"
	#print "Tweet file: " + str(tweet_file)
	#print "Number of tweets: " + str(tweet_count)
	#print "Time used in readJSON: " + str(stop_time - start_time)
	#print dictionary
	#print "- - - - - - - - - - - - - - - - - - - - - - - - - - -"
	dictionary.update({"tweet_count": tweet_count})
	return dictionary
#getTweets()