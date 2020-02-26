from logging import getLogger, NullHandler
import tweepy

logger = getLogger("twitter")
logger.addHandler(NullHandler())


class Mytwitter(object):
    counter = 1
    api = None
    # counter=0
    # this value stop using twitter api.
    # If you run this app, change value to 0.

    def __init__(self, Ck=None, Cs=None, At=None, As=None):
        self.__switch = "OFFED"
        if not (Mytwitter.counter):
            self.__CK = Ck
            self.__CS = Cs
            self.__AT = At
            self.__AS = As
            self.get_oauth()
        Mytwitter.counter += 1

    def __repr__(self):
        return f"{Mytwitter.counter}th twitter-{self.__switch}"

    def get_oauth(self):
        try:
            auth = tweepy.OAuthHandler(self.__CK, self.__CS)
            auth.set_access_token(self.__AT, self.__AS)
            Mytwitter.api = tweepy.API(auth)
            self.__switch = "AUTHED"
        except Exception:
            self.__switch = "DISAUTHED"

    def search_list(self, id_: str) -> list:
        try:
            listlist = []
            for i in Mytwitter.api.lists_all(id_):
                listlist.append(i.name)
            return listlist
        except Exception:
            logger.warning("cannot read list from twitter id.")
            return None
