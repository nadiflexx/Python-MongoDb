#import files and give access to tokens and keys
import os
import tweepy as tw
import json

#Read json file, requests
import requests

#MogoDB database connection
from pymongo import MongoClient

#Mongodb connection
conn = MongoClient('mongodb://localhost:27017')

#Mongodb database and repository
db = conn.Twitter

#Collections
Barcelona2 =  db.Barcelona2 #Store data in database


access_token=""
access_token_secret=""
consumer_key=""
consumer_secret=""

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

# Define the search term and the date_since date as variables
search_words = "barcelona"
date_since = "2020-01-01"

# Collect tweets
tweets = tw.Cursor(api.search,
              q=search_words,
              since=date_since).items(1000)

json_tweet = []

# Iterate and print tweets
for tweet in tweets:

    #Get _json structure of tweets
    json_tweet.append(tweet._json)
    
    #Or insert data in mongodb database for each tweet (dict)
    Barcelona2.insert_one(tweet._json)

#Create a json file and insert data  https://realpython.com/python-json/
with open('barcelona.json', 'w') as outfile:
    json.dump(json_tweet, outfile)
