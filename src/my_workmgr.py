# -*- coding: utf-8 -*-
import os

class MyWorkMgr(object):

    def __init__(self, num):
        self._num = num

    def scanFiles(self, pth):
        files = [os.path.join(root, name)
                     for root, dirs, files in os.walk(pth)
                     for name in files]
        r = {}
        b = []
        for f in files:
            if os.path.isfile(f):
                _, e = os.path.split(f)
                if u"." in e:
                    arr = e.split(u".")
                    e = arr[len(arr)-1].lower()
                    if e not in r.keys():
                        r[e] = 1
                    else:
                        r[e] += 1
                else:
                    b.append(e)
        for p in r:
            print p

    @property
    def num(self):
        return self._num

    @num.setter
    def num(self, n):
        self._num = n
