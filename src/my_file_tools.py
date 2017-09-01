# -*- coding: utf-8 -*-
import os
import hashlib
import my_event as EVT
from my_models import File

def get_md5(pth):
    with open(pth, "r") as f:
        m = hashlib.md5()
        while True:
            data = f.read(10240)
            if not data:
                break
            m.update(data)
    return m.hexdigest()

def check_sync_status(fp):
    assert fp is not None
    pth = os.path.abspath(fp)
    sigs = []
    if os.path.exists(pth):
        md5str = get_md5(pth)
        try:
            f = File.select().where((File.md5 == md5str) | (File.path == pth)).get()
            if f.delete_flag:
                sigs.append(EVT.SYNC_LOCAL_REVERT)
            if f.md5 != md5str:
                sigs.append(EVT.SYNC_LOCAL_MODIFIED)
            if f.path != pth:
                sigs.append(EVT.SYNC_LOCAL_MOVED)
        except File.DoesNotExist:
            f = File.add(pth, md5str)
            sigs.append(EVT.SYNC_LOCAL_NEW)
    else:
        f = None
        sigs.append(EVT.SYNC_LOCAL_DELETED)

    return f, sigs
