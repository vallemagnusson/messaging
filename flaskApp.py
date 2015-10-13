#!flask/bin/python
from flask import Flask
from tasks import getTweets

app = Flask(__name__)

@app.route("/")
def start():
	#return "hello world", 200
	primes = getTweets.delay()
	while getTweets.ready() == False:
		time.delay(5)
	print getTweets.get()


if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)

