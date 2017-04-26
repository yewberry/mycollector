# -*- coding: utf-8 -*-
import os
import json
import ConfigParser
from my_glob import LOG
from my_glob import Singleton

# ---------------
# CRITICAL 	50
# ERROR 	40
# WARNING 	30
# INFO 	    20
# DEBUG 	10
# ---------------

CFG_INI = """[GENERAL]
version=1.0.0
"""
CFG_JSON = {
    "version": "1.0.0",
    "logLevel": 10
}

class MyConf(object):
    __metaclass__ = Singleton

    def __init__(self, file_path=None, file_type="json"):
        LOG.info(u"cfg path:{}".format(file_path))
        self.path = file_path
        self.type = file_type
        if self.path is None:
            LOG.error("cfg file path is None which shouldn't happen")
        elif not os.path.isfile(self.path):
            with open(self.path, "w") as f:
                if "json" == file_type:
                    json.dump(CFG_JSON, f, sort_keys=True, indent=4, separators=(',', ': '))
                elif "ini" == file_type:
                    f.write(CFG_INI)

    # TODO yew thread-safe
    def get(self, key):
        with open(self.path, "r") as f:
            rtn = json.load(f)[key]
        return rtn

    def set(self, key, val):
        with open(self.path, "r") as f:
            ctn = json.load(f)
            ctn[key] = val
        with open(self.path, "w") as f:
            json.dump(ctn, f, sort_keys=True, indent=4, separators=(',', ': '))

    def get_ini(self, sect, name):
        config = ConfigParser.ConfigParser()
        config.read(self.path)
        if not config.has_option(sect, name):
            return None
        return config.get(sect, name)

    def set_ini(self, sect, name, value):
        config = ConfigParser.ConfigParser()
        config.read(self.path)
        if not config.has_section(sect):
            config.add_section(sect)
        config.set(sect, name, value)
        config.write(open(self.path, "r+"))

