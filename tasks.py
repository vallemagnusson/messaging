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

app = Celery('tasks', backend='amqp', broker='amqp://mava:orkarinte@130.238.29.120:5672/app2')

@app.task
def getTweets(tweetFileList):
	start_time_getTweets = time.time()
	print "getTweets started"
	dictionary_all = Counter({"han": 0, "hon": 0, "den": 0, "det": 0, "denna": 0, "denne": 0, "hen": 0, "tweet_count": 0})
	for tweetFile in tweetFileList:
		if tweetFile == "tweets_19.txt" or tweetFile == "tweets_18.txt":
			print "- - - - - - - - - " + tweetFile + " - - - - - - - - -"
			start_time_download_file = time.time()
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
	return dictionary_all

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