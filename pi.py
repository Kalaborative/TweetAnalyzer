import tweepy
import sqlite3


c_key = "1Va9E6ca4zb43q9JWf8mfZafc"
c_secret = "9tg89S9VcKf9AzfZh9CeMrsT8TjnbJN43RyTOxUX6uuddduE4W"

a_token = "114579331-oJa6oT6dKmciwyCcAGs0JjkY783ylyS3RJXPFocK"
a_secret = "vw7qWTONxEidKZnw3mVEKHD58uPF8NsyB19o2hCkX6jyN"

auth = tweepy.OAuthHandler(c_key, c_secret)
auth.set_access_token(a_token, a_secret)
Dumpdata = []
max_tweets = 10
topics = ["funny", "LOL", "Yeah", "think",
          "allow", "woman", "why", "dog", "kitty"]

api = tweepy.API(auth)
with sqlite3.connect("Twitter_data.db") as connection:
    c = connection.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS TrackData (Username TEXT, Sent TEXT, Message TEXT)")


def dump_my_data(dataset):
    with sqlite3.connect("Twitter_data.db") as connection:
        c = connection.cursor()
        connection.text_factory = str
        c.executemany("INSERT INTO TrackData VALUES(?, ?, ?)", dataset)


class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api=None):
        super(MyStreamListener, self).__init__()
        self.num_tweets = 0
        global Dumpdata
        del Dumpdata[:]

    def on_status(self, status):
        global Dumpdata
        json_str = status._json
        tweet_user = json_str["user"]["screen_name"]
        tweet_date = json_str["created_at"]
        tweet_text = status.text.encode('utf-8')
        print
        print "New status from @%s!" % tweet_user
        print tweet_text
        print tweet_date
        response_load = (tweet_user, tweet_date, tweet_text)
        Dumpdata.append(response_load)
        self.num_tweets += 1
        if self.num_tweets < max_tweets:
            return True
        else:
            return False


class Steann(tweepy.Stream):
    def disconnect(self):
        return Dumpdata
