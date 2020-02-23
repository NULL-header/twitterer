from logging import getLogger, NullHandler
import tweepy

logger = getLogger("twitter")
logger.addHandler(NullHandler())


class Mytwitter(object):
    counter = 0

    def __init__(self, Ck=None, Cs=None, At=None, As=None):
        if not (Mytwitter.counter):
            self.__CK = Ck
            self.__CS = Cs
            self.__AT = At
            self.__AS = As
            self.get_oauth()
        Mytwitter.counter += 1

    def get_oauth(self):
        auth = tweepy.OAuthHandler(self.__CK, self.__CS)
        auth.set_access_token(self.__AT, self.__AS)
        self.__api = tweepy.API(auth)

    @property
    def api(self):
        return self.__api

    def search_list(self, id_: str) -> list:
        try:
            listlist = []
            for i in self.api.lists_all(id_):
                listlist.append(i.name)
            return listlist
        except Exception:
            logger.warning("cannot read list from twitter id.")
            return None
