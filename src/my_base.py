# -*- coding: utf-8 -*-
import os
import hashlib

class MyBase(object):
    def __init__(self):
        pass

    def get_file_md5(self, fp):
        with open(fp, "r") as f:
            m = hashlib.md5()
            while True:
                data = f.read(10240)
                if not data:
                    break
                m.update(data)
        return m.hexdigest()


