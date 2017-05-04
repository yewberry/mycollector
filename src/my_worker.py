# -*- coding: utf-8 -*-
import os
import my_models as Model

def sync_files_info(pth):
    files = [os.path.join(root, name)
             for root, dirs, files in os.walk(pth)
             for name in files]
    for fp in files:
        Model.File.checkAndCreate(fp)

def scan_files(pth):
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
                e = arr[len(arr) - 1].lower()
                if e not in r.keys():
                    r[e] = 1
                else:
                    r[e] += 1
            else:
                b.append(e)
    for p in r:
        print p
