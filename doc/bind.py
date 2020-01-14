# encoding:utf-8
import os
import pickle


class Bind(object):
    def __init__(self):
        self.data = {}

    def read_data(self, path_data, path_err):
        self.path_data = path_data
        self.path_err = path_err
        result = 0
        try:
            with open(path_err, "r")as f:
                data = f.readlines()
        except Exception:
            result = 201
            return result
        try:
            with open(path_data, "rb")as f:
                self.data = pickle.load(f)
            result = 100
        except Exception:
            result = 302
        buff = []
        for i in data:
            bu = i.rstrip().split(":")
            buff.append(tuple([int(bu[0]), bu[1]]))
        self.err = dict(buff)
        return result

    def set_bind(self, gid, cid):
        d = self.data
        if not d.get(gid):
            d[gid] = {}
        if d[gid].get(cid):
            return 301
        d[gid][cid] = self._childer()
        return 100

    @staticmethod
    def _childer():
        return{
            "tw": None,
            "id": None,
            "slug": None
        }

    def check_bind(self, gid, cid):
        if not self.data.get(gid):
            return [False, 303]
        if not self.data[gid].get(cid):
            return [False, 304]
        return [True, 100]

    def err_returner(self, code):
        return self.err[code]

    def _dumper(self):
        with open(self.path_data, "wb")as f:
            pickle.dump(self.data, f)

    def clean_bind(self):
        result = 0
        try:
            os.remove(self.path_data)
            result = 100
        except Exception:
            result = 305
        self.data = {}
        return result

    def set_id(self, gid, cid, id):
        if not id:
            return 306
        if id.startswith("@"):
            id = id[1:]
        self.data[gid][cid]["id"] = id
        return 100
