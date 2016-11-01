from collections import Counter
from nltk.corpus import stopwords
import sqlite3
bank = []
stop = set(stopwords.words('english'))
flattenedBank = []
filter1 = ["I", "I'm", "like"]

with sqlite3.connect('Twitter_data.db') as connection:
    c = connection.cursor()

    c.execute("SELECT Message FROM TrackData")

    messages = c.fetchall()

    for message in messages:
        bank.append((message[0].split()))

    for data in bank:
        for d in data:
            flattenedBank.append(d.encode('utf-8'))

bankNoStop = [f for f in flattenedBank if f.lower() not in stop]
bank1 = [b for b in bankNoStop if b not in filter1 and b.isalpha() and len(b) >= 4]
bank_accounts = Counter(bank1)
top_words = bank_accounts.most_common(10)

print "Top ten words used in tweets:"
for tw in top_words:
	print
	print "Word: ", tw[0]
	print "Times seen: ", tw[1]
