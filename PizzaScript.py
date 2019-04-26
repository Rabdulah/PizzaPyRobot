import json
import requests
import tweepy
import logging
import re
import datetime
import os

from slackclient import SlackClient

logging.basicConfig(level=logging.DEBUG)

os.environ['CONSUMER_KEY']
consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET'] 
access_token = os.environ['ACCESS_TOKEN']
access_token_secret = os.environ['ACCESS_TOKEN_SECRET']

slack_client = SlackClient(os.environ['MOBIALS_BOT_KEY'])

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

congrats_msg = "Congrats! Your name is one of Stobie's free pizza names today!"
now = datetime.datetime.now()

def getTweet():
    stobies_last_tweet = api.user_timeline(id = 'Stobiespizza', count = 1, tweet_mode='extended')
    if stobies_last_tweet[0].created_at.day == now.day:
        return stobies_last_tweet

def getUsers():
    users = []
    getUsers = slack_client.api_call(
        "users.list"
    )
    if getUsers['ok'] is not True:
        logging.error(getUsers)
    else:
        for user in getUsers['members']:
            name_and_id = [user['profile']['real_name'].split()[0], user['id']] # save user ID so we can DM the user later
            users.append(name_and_id)
    return users

def checkMatch(users, tweet):
    matches = []
    for name in users:
        if re.search(r'\b' + name[0] + r'\b', tweet, re.IGNORECASE):
            matches.append(name)       
    return matches

# The bot needs to open a new channel to dm a user. We supply a userId and are returned a channelId to dm that user
def getDirectMessageChannel(user_id):
    return slack_client.api_call(
        "im.open",
        user=user_id
    )['channel']['id']

def sendMessage(users, msg):
    for user in users:
        dm_channel = getDirectMessageChannel(user[1])
        updateMsg = slack_client.api_call(
            "chat.postMessage",
            channel=dm_channel,
            text=msg
        )
        if updateMsg['ok'] is not True:
            logging.error(updateMsg)
    
if __name__ == "__main__":
    stobies_last_tweet = getTweet()
    if stobies_last_tweet is not None:
        users = getUsers()
        matches = checkMatch(users, stobies_last_tweet[0].full_text) 
        sendMessage(matches, congrats_msg)
    else:
        print "Set step function for 15 min"
