import re
import sys
import tweepy
import pandas as pd 
from htmlentitydefs import name2codepoint as n2c
from local_settings import *
from datetime import datetime


# Connect to twitter using tweepy
def tweepyconnect():
    auth = tweepy.OAuthHandler(consumer_key=MY_CONSUMER_KEY, consumer_secret=MY_CONSUMER_SECRET)
    auth.set_access_token(MY_ACCESS_TOKEN_KEY, MY_ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    return api

#Analyze a tweet
def entity(text):
    if text[:2] == "&#":
        try:
            if text[:3] == "&#x":
                return unichr(int(text[3:-1], 16))
            else:
                return unichr(int(text[2:-1]))
        except ValueError:
            pass
    else:
        guess = text[1:-1]
        numero = n2c[guess]
        try:
            text = unichr(numero)
        except KeyError:
            pass    
    return text

#Filter tweet. Not currently used - gets rid of RTs
def filter_tweet(tweet):
    tweet.text = re.sub(r'\b(RT|MT) .+','',tweet.text) #take out anything after RT or MT
    tweet.text = re.sub(r'(\#|@|(h\/t)|(http))\S+','',tweet.text) #Take out URLs, hashtags, hts, etc.
    tweet.text = re.sub(r'\n','', tweet.text) #take out new lines.
    tweet.text = re.sub(r'\"|\(|\)', '', tweet.text) #take out quotes.
    htmlsents = re.findall(r'&\w+;', tweet.text)
    if len(htmlsents) > 0 :
        for item in htmlsents:
            tweet.text = re.sub(item, entity(item), tweet.text)    
    tweet.text = re.sub(r'\xe9', 'e', tweet.text) #take out accented e
    return tweet.text

#Sanitize -- look for a specific term - eventually make this user submitted
def sanitize_tweet(tweet):
    findMe = re.findall(SEARCHTERM, tweet.text)
    if len(findMe) > 0 :
        return tweet.text
    return ''              
          
#Get a set of tweets to work with                                          
def grab_tweets(api, max_id=None):
    source_tweets=[]
    #user_tweets = api.GetUserTimeline(screen_name=user, count=200, max_id=max_id, include_rts=True, trim_user=True, exclude_replies=True)
    user_tweets = api.user_timeline(screen_name=user, max_id=max_id, count=200)
    max_id = user_tweets[len(user_tweets)-1].id-1
    for tweet in user_tweets:
        #tweet.text = filter_tweet(tweet)
        tweet.text = sanitize_tweet(tweet)
        if len(tweet.text) != 0:
            source_tweets.append(datetime.strftime(tweet.created_at,'%a %b %d %H:%M:%S %z %Y') + ' ' + tweet.text)
    return source_tweets, max_id


#Main procedure
if __name__=="__main__":
    source_tweets = []
    for handle in SOURCE_ACCOUNTS:
        user=handle
        api=tweepyconnect()
        #handle_stats = api.GetUser(screen_name=user)
        #handle_stats = api.get_user(screen_name=user)
        #status_count = handle_stats.statuses_count
        max_id=None
        #if status_count<3200:
        #    my_range = (status_count/200) + 1
        #else:
        my_range = 17
        for x in range(my_range)[1:]:
            source_tweets_iter, max_id = grab_tweets(api,max_id)
            source_tweets += source_tweets_iter
        print "{0} tweets found in {1}".format(len(source_tweets), handle)
        if len(source_tweets) == 0:
            print "Error fetching tweets from Twitter. Aborting."
            sys.exit()

    tweet_list = []
    for tweet in source_tweets:
        if re.search('([\.\!\?\"\']$)', tweet):
            pass
        else:
            tweet+="."
        tweet_list.append(tweet)

    df = pd.DataFrame(tweet_list, columns=['tweet'])
    print df
    sys.exit();
    