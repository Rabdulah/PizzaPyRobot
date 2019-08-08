import json
import requests
import tweepy
import logging
import re
import datetime
import os

from slackclient import SlackClient

logging.basicConfig(level=logging.DEBUG)

consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET'] 
access_token = os.environ['ACCESS_TOKEN']
access_token_secret = os.environ['ACCESS_TOKEN_SECRET']

slack_client = SlackClient(os.environ['MOBIALS_BOT_KEY'])

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

congrats_msg = 'Congrats! Your name is one of Stobie\'s free pizza names today!'
now = datetime.datetime.now()

def getTweet():
    stobies_last_tweet = api.user_timeline(id = 'Stobiespizza', count = 1, tweet_mode='extended')
    print(stobies_last_tweet[0].full_text)
    if stobies_last_tweet[0].created_at.day == now.day:
        return stobies_last_tweet

def getUsers():
    users = []
    getUsers = slack_client.api_call(
        'users.list'
    )
    if getUsers['ok'] is not True:
        logging.error(getUsers)
    else:
        for user in getUsers['members']:
            name_and_id = [user['profile']['real_name'], user['id']] # save user ID so we can DM the user later
            users.append(name_and_id)
    return users

def checkMatch(users, tweet):
    matches = []
    for name in users:
        if re.search(r'\b' + name[0].split()[0] + r'\b', tweet, re.IGNORECASE):
            matches.append(name)       
    return matches

# The bot needs to open a new channel to dm a user. We supply a userId and are returned a channelId to dm that user
def getDirectMessageChannel(user_id):
    return slack_client.api_call(
        'im.open',
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
    
def lambda_handler(event, context):
    stobies_last_tweet = getTweet()
    if stobies_last_tweet is not None:
        users = getUsers()
        matches = checkMatch(users, stobies_last_tweet[0].full_text)
        winners = {}

        if (len(matches)):
            sendMessage(matches, congrats_msg)
            print 'Free pizza for someone!'
            for index, match in enumerate(matches, start=1):
                winners[index] = match[0] # It would be nice to know the full names of the people who won (especially if they have the same first name)
        else:
            print 'No free pizza today'

        return {
            'Number of winners': len(matches),
            'winners': winners
        }

    else:
        return('No new tweet found today')

if __name__ == "__main__":
    stobies_last_tweet = getTweet()
    if stobies_last_tweet is not None:
        users = getUsers()
        matches = checkMatch(users, stobies_last_tweet[0].full_text)

        if (len(matches)):
            sendMessage(matches, congrats_msg)
            print 'Number of matches: {}'.format(len(matches))
            for index, match in enumerate(matches, start=1):
                print '{}. {}'.format(index, match[0])
        else:
            print 'No pizza winners today'

    else:
        print 'No new tweet found today'