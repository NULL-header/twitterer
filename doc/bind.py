# encoding:utf-8
import os
import pickle
from logging import NullHandler, getLogger

from twitterer import Mytwitterer

logger = getLogger(__name__)
logger.addHandler(NullHandler())


class Bind(object):
    def __init__(self):
        self.data = {}

    def read_data(self):
        result = 0
        try:
            with open(self.path_data, "rb")as f:
                self.data = pickle.load(f)
            result = 100
            logger.info("[read_data] Done successfully.")
        except Exception:
            logger.info("[read_data] Done without to read picklefile.")
            result = 302
        return result

    def set_bind(self, gid, cid):
        d = self.data
        if not d.get(gid):
            d[gid] = {}
        if d[gid].get(cid):
            logger.info("[set_bind] The guild is not in data.")
            return None
        d[gid][cid] = self._childer()
        logger.info("[set_bind] Done successfully.")
        return 100

    def _childer(self):
        return{
            "tw": Mytwitterer(self.CK, self.CS, self.AT, self.AS),
            "id": None,
            "slug": None
        }

    def check_bind(self, gid, cid):
        if not self.data.get(gid):
            logger.info("[check_bind] The id of guild is not in data.")
            return [False, 303]
        if not self.data[gid].get(cid):
            logger.info("[check_bind] The channel is not binded.")
            return [False, 304]
        logger.info("[check_bind] Done successfully.")
        return [True, 100]

    def _dumper(self):
        with open(self.path_data, "wb")as f:
            pickle.dump(self.data, f)

    def clean_bind(self):
        result = 0
        try:
            os.remove(self.path_data)
            logger.info("[clean_bind] Done successfully.")
            result = 100
        except Exception:
            logger.info("[clean_bind] Done without to delete save-file.")
            result = 305
        self.data = {}
        return result

    def set_id(self, gid, cid, id):
        if not id:
            logger.info("[set_id] The id, a argment, is nothing.")
            return 306
        if id.startswith("@"):
            id = id[1:]
        self.data[gid][cid]["id"] = id
        logger.info("[set_id] Done successfully.")
        return 100

    def setter(self, d: dict):
        self.path_data = d["pd"]
        self.path_err = d["pe"]
        self.CK = d["ck"]
        self.CS = d["cs"]
        self.AT = d["at"]
        self.AS = d["as"]
        logger.info("[set_id] Done successfully.")
        return 100

    def set_list(self, gid, cid, listname):
        if not self.data[gid][cid]["id"]:
            logger.info(
                "[set_list] Nothing there is the id in the internal data.")
            return 307
        self.data[gid][cid]["slug"] = listname
        logger.info("[set_list] Done successfully.")
        return 100
