# This is a module dedicated to gathering, organizing and preparing tweets for sentiment analysis. 

from __future__ import unicode_literals
from utils import Utils
import os
import tweepy
import json
import re
import spacy
import pandas as pd
import numpy as np 

ROOT_PATH = Utils().globals.get('ROOT_PATH')


class Twitter_Searcher:
    """
    Module for Winston. 

    Searches twitter via tweepy in a multitude of ways, gathers tweets and saves them as json.
    Access tweet texts via Twitter_Searcher().tweets or full tweets via .tweets_full
    """

    CONSUMER_KEY = os.environ['TWITTER_CONSUMER_KEY']
    CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
    ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
    ACCESS_TOKEN_SECRET = os.environ['TWITTER_ACCESS_TOKEN_SECRET']


    def __init__(self, query, count):
        self.__setup_auth__()
        self.__search__(query, count)
        self.__clean_texts__()
        self.__lemmatize__texts__()
        self.__create_set__()
        
        
    def __setup_auth__(self):
        self.auth = tweepy.OAuthHandler(Twitter_Searcher.CONSUMER_KEY, Twitter_Searcher.CONSUMER_SECRET)
        self.auth.set_access_token(Twitter_Searcher.ACCESS_TOKEN, Twitter_Searcher.ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(self.auth)

    def __search__(self, query, count):
        """
        Gathers a given number of tweets related to the given query

        query: The search term "Tesla", "#art" etc.
        count: Number of tweets to be returned.
        """
        self.tweets_full = self.api.search(query, show_user=True, tweet_mode='extended', count=count, lang='en')
        self.tweets_full = [tweet._json for tweet in self.tweets_full]

        texts = [self.__check_if_retweet__(tweet) for tweet in self.tweets_full]
        ids = [self.__get_id__(tweet) for tweet in self.tweets_full]
        tweets = {'id': ids, 'text': texts}
        self.tweets = pd.DataFrame(data=tweets)

    def __clean_texts__(self):
        # Remove http links from texts
        self.tweets['text'] = self.tweets['text'].apply(lambda text: re.sub(r'http\S+', '', text, flags=re.MULTILINE)) 

        # Remove newlines
        self.tweets['text'] = self.tweets['text'].apply(lambda text: text.replace('\n', '. '))

        # Remove emojis etc
        emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"
                           "]+", flags=re.UNICODE)
        emoji_pattern_2 = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)
        def emoji_remover(text):
            text = emoji_pattern.sub(r'', text)
            return  emoji_pattern_2.sub(r'', text)

        self.tweets['text'] = self.tweets['text'].apply(emoji_remover)

        #Remove @ and names
        self.tweets['text'] = self.tweets['text'].apply(lambda text: re.sub(r'@\S+', '', text, flags=re.MULTILINE))

    def __lemmatize__texts__(self):
        nlp = spacy.load('en_core_web_sm')

        def lemma(text):
            doc = nlp(text)
            sent = []
            for word in doc:
                if word.lemma_ == '-PRON-':
                    sent.append(word.text)
                elif word.shape_[0] == 'X':
                    sent.append(word.text)
                elif word.text[0] == '@':
                    sent.append(word.text)
                else:
                    sent.append(word.lemma_)
            return ' '.join(sent)

        self.lemmatized_tweets = self.tweets
        self.lemmatized_tweets['text'] = self.lemmatized_tweets['text'].apply(lemma)

    def __create_set__(self):
        self.unique_tweets = self.tweets.drop_duplicates()
        self.lemmatized_unique_tweets = self.lemmatized_tweets.drop_duplicates()

    def __check_if_retweet__(self, tweet):
        text = ''
        if tweet['full_text'].split()[0].lower() == 'rt':
            try:
                text = tweet['retweeted_status']['full_text']
            except:
                pass
        else:
            text = tweet['full_text']

        return text
    
    def __get_id__(self, tweet):
        id_nr = ''
        if tweet['full_text'].split()[0].lower() == 'rt':
            try:
                id_nr = tweet['retweeted_status']['id']
            except:
                pass
        else:
            id_nr = tweet['id']

        return id_nr

    def __get_test_tweets__(self):
        self.tweets_full = json.load(open(ROOT_PATH + 'abilities\\finance\\tweet_examples.json'))
        return self.tweets_full
    
    def __save_tweets_to_file__(self, file_name='output.json'):
        with open(ROOT_PATH + 'abilities\\finance\\twitter_searcher_files\\' + file_name, 'w') as file:
            json.dump(self.tweets_full, fp=file)

    def print_texts(self):
        index = 1
        for text in self.tweets['text']:
            print(f'=================== {index} ======================')
            print(text)
            print('')
            index += 1

    def print_unique_texts(self):
        index = 1
        for text in self.unique_tweets:
            print(f'=================== {index} ======================')
            print(text)
            print('')
            index += 1

