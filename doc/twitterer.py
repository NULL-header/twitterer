# encoding:utf-8
from logging import getLogger

import tweepy

logger = getLogger("bot").getChild(__name__)


class Mytwitterer():
    counter = 0

    def __init__(self, CK, CS, AT, AS):
        if not (Mytwitterer.counter):
            self.__CK = CK
            self.__CS = CS
            self.__AT = AT
            self.__AS = AS
            self.get_oauth()
            Mytwitterer.counter += 1

    def get_oauth(self):
        auth = tweepy.OAuthHandler(self.__CK, self.__CS)
        auth.set_access_token(self.__AT, self.__AS)
        self.__api = tweepy.API(auth)

    @property
    def api(self):
        return self.__api

    def search_list(self, id: str) -> list:
        try:
            return self.api.lists_all(id)
        except Exception:
            logger.warning("cannot read list from twitter id.")

    @classmethod
    def instance
