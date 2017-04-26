# -*- coding: utf-8 -*-
import os
import cPickle
from my_glob import LOG
from my_glob import Singleton

class MySession(object):
    __metaclass__ = Singleton

    def __init__(self, file_path=""):
        LOG.info(u"session path:{}".format(file_path))
        self.file_path = file_path
        self.session = {}
        if self.file_path == "":
            LOG.error("session file path is empty which shouldn't happen")
        elif os.path.isfile(self.file_path):
            with open(self.file_path, "rb") as f:
                self.session = cPickle.load(f)

    def get(self, key, default=None):
        val = self.session[key] if key in self.session else None
        return val if val is not None else default

    def set(self, key, val):
        self.session[key] = val
        with open(self.file_path, "wb") as f:
            cPickle.dump(self.session, f, cPickle.HIGHEST_PROTOCOL)

