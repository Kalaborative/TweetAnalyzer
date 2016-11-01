import tweepy
from textblob import TextBlob
c_key = "1Va9E6ca4zb43q9JWf8mfZafc"
c_secret = "9tg89S9VcKf9AzfZh9CeMrsT8TjnbJN43RyTOxUX6uuddduE4W"

a_token = "114579331-oJa6oT6dKmciwyCcAGs0JjkY783ylyS3RJXPFocK"
a_secret = "vw7qWTONxEidKZnw3mVEKHD58uPF8NsyB19o2hCkX6jyN"

auth = tweepy.OAuthHandler(c_key, c_secret)
auth.set_access_token(a_token, a_secret)
api = tweepy.API(auth)
names = []
blobase = []
polars = []
pyaon = raw_input("choose a: my timeline, b: random timeline> ")
if pyaon == 'a':
	own_search = api.home_timeline()
	for o in own_search:
		names.append(o.user.screen_name)
		blobase.append(o.text)
		polars.append(TextBlob(o.text).sentiment.polarity)
	strblob = ' '.join(blobase)
	blob = TextBlob(strblob)
	linkval = zip(names, blobase, polars)
	print linkval
	for l in linkval:
		print
		print "@" + l[0]
		print l[1]
		if l[2] < 0.0:
			print "Negative sentiment"
		elif l[2] >= 0.0 and l[2] <= 0.5:
			print "Neutral sentiment"
		else:
			print "Positive sentiment"
	feed = blob.sentiment.polarity
	if feed < 0:
		print "Ooh.. your feed is looking pretty negative."
	elif feed > 0.1 and feed <= 0.3:
		print "Your feed looks neutral!"
	else:
		print "Your feed looks great!"
elif pyaon == 'b':
	uname = raw_input("enter a username: ")
	my_search = api.user_timeline(screen_name=uname)
	for m in my_search:
		blobase.append(m.text)
	strblob = ' '.join(blobase)
	blob = TextBlob(strblob)
	feed = blob.sentiment.polarity
	if feed < 0:
		print "Ooh.. your feed is looking pretty negative."
	elif feed > 0.1 and feed <= 0.3:
		print "Your feed looks neutral!"
	else:
		print "Your feed looks great!"
