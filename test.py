import os

import urllib2


fileList = urllib2.Request("http://smog.uppmax.uu.se:8080/swift/v1/tweets/" + tweetFile)

for tweetFile in fileList:
	urlRequest = urllib2.Request("http://smog.uppmax.uu.se:8080/swift/v1/tweets/" + tweetFile)
	urlResponse = urllib2.urlopen(urlRequest).read()
	new_file = open(tweetFile, "w")
	new_file.write(urlResponse)
	new_file.close()
##i = 0
##tweetFileList = []
##content = os.listdir("./")
##new_file = open("large_tweets", "w")
##new_file.close()
##for x in content:
##	old_file = open(x, "r").read()
##	with open("large_tweets.txt", "a") as add_new_file:
##		add_new_file.write(old_file)
#fileName = "tweets_2.txt"
#fil = open(fileName, "r")
##numb_line = sum(1 for _ in fil)
#langd= len(fil.readlines()) -1
#fil.close()
#
##print numb_line
##print langd
#fil = open(fileName, "r")
#filLines = fil.readlines()
##print fil.readlines()
##for x in range(numb_line):
##	fileName = x % 100
##
##	new_file = open("new_tweet_file_" + str(fileName) + ".txt", "a")
#count = 0
##print filLines[0]
#fileVar = 0
#while langd != count:
##for line in fil:
#	#print line
#	fileVar += 1
#	count += 1
#	if count > langd:
#		break
#	fileName = fileVar % 12
#	new_file = open("new_tweet_file_" + str(fileName) + ".txt", "a")
#	new_file.write(filLines[count])
#	count += 1
#	if count > langd:
#		break
#	new_file.write(filLines[count])
#	#print line#