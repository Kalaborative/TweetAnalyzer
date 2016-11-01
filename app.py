from flask import Flask, render_template, request
from flask_tweepy import Tweepy
from pi import MyStreamListener, Steann
from textblob import TextBlob
import sqlite3

c_key = "1Va9E6ca4zb43q9JWf8mfZafc"
c_secret = "9tg89S9VcKf9AzfZh9CeMrsT8TjnbJN43RyTOxUX6uuddduE4W"

a_token = "114579331-oJa6oT6dKmciwyCcAGs0JjkY783ylyS3RJXPFocK"
a_secret = "vw7qWTONxEidKZnw3mVEKHD58uPF8NsyB19o2hCkX6jyN"
app = Flask(__name__)
app.config.setdefault('TWEEPY_CONSUMER_KEY', c_key)
app.config.setdefault('TWEEPY_CONSUMER_SECRET', c_secret)
app.config.setdefault('TWEEPY_ACCESS_TOKEN_KEY', a_token)
app.config.setdefault('TWEEPY_ACCESS_TOKEN_SECRET', a_secret)

tweepy = Tweepy(app)

topix = []
with sqlite3.connect("Twitter_data.db") as connection:
	c = connection.cursor()
	c.execute("CREATE TABLE IF NOT EXISTS TrackData (Username TEXT, Sent TEXT, Message TEXT)")


@app.route("/", methods=['POST', 'GET'])
def hello():
    return render_template('index.html')


@app.route("/result", methods=["POST", "GET"])
def show_result():
	names = []
	blobase = []
	polars = []
	if request.method == "POST":
		result = request.form['topic']
		tweetl = tweepy.api.search(q=result, lang='en', show_user=True)
		for o in tweetl:
			names.append(o.user.screen_name)
			blobase.append(o.text)
			polars.append(TextBlob(o.text).sentiment.polarity)
		linkval = zip(names, blobase, polars)
		return render_template('result.html', topics=linkval)


@app.route('/tweets', methods=['POST', 'GET'])
def show_tweets():
	topix = request.form['qtops'].encode('utf-8').split()
	if request.method == "POST":
		mms = MyStreamListener()
		mystream = Steann(auth=tweepy.api.auth, listener=mms)
		mystream.filter(track=topix)
		moom = mystream.disconnect()
	return render_template('tweets.html', user=moom)


@app.route('/id-finder', methods=["GET", "POST"])
def id_finder():
	found_ID = None
	error_message = None
	if request.method == "POST":
		try:
			found_name = request.form['inputSmall']
			gotten_user = tweepy.api.get_user(found_name)
			found_ID = gotten_user.id
		except Exception as e:
			error_message = e
	return render_template('finder.html', twitID=found_ID, errno=error_message)


if __name__ == "__main__":
    app.run()
