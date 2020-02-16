# encoding:utf-8
import os
from logging import getLogger

import tweepy

logger = getLogger("bot").getChild(__name__)


class Mytwitterer(object):
    counter = 0
    path_ram = "..\\.data\\"

    def __init__(self, CK, CS, AT, AS):
        if not (Mytwitterer.counter):
            self.__CK = CK
            self.__CS = CS
            self.__AT = AT
            self.__AS = AS
            self.get_oauth()
            Mytwitterer.counter += 1

    def __eq__(self, other):
        return self.__class__.__name__ == other.__class__.__name__

    def get_oauth(self):
        auth = tweepy.OAuthHandler(self.__CK, self.__CS)
        auth.set_access_token(self.__AT, self.__AS)
        self.__api = tweepy.API(auth)

    @property
    def api(self):
        return self.__api

    def search_list(self, id: str) -> list:
        try:
            listlist = []
            for i in self.api.lists_all(id):
                listlist.append(i.name)
            return listlist
        except Exception:
            logger.warning("cannot read list from twitter id.")
            return None

    def get_list(self, id, slug):
        list_tweets = []
        dict_kwd = {
            "owner_screen_name": id,
            "slug": slug,
            "include_rts": "True",
            "count": self.__kazu,
            "tweet_mode": "extended",
        }
        for tweet in self.api.list_timeline(**dict_kwd):
            list_tweets.append(tweet)
        return list_tweets[::-1]

    def get_images(self):
        list_images = []
        for tweet in self.get_list():
            ram = []
            if tweet.entities["urls"]:
                ram.append("urls")
            if hasattr(tweet, "extended_entities"):
                type_tweet = tweet.extended_entities["media"][0]["type"]
                if(type_tweet == "photo"):
                    ram.append("photo")
                if(type_tweet == "video"):
                    ram.append("video")
                if(type_tweet == "animated_gif"):
                    ram.append("gif")
            if ram:
                ram.append(tweet)
                list_images.append(ram)
        return list_images
