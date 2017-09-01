# -*- coding: utf-8 -*-
import os
import my_file_tools as filetools
import my_event as EVT
import my_models as MOD

def sync_local_dir(pth, queue):
    files = [os.path.join(root, name)
             for root, dirs, files in os.walk(pth)
             for name in files]
    for fp in files:
        sync_local_file(fp, queue)

def sync_local_file(pth, queue):
    f, sigs = filetools.check_sync_status(pth)
    f = {"md5": ""} if f is None else f
    for sig in sigs:
        dat = {
            "path": pth,
            "md5": f.md5
        }
        _update_db(sig, dat)
        queue.put({"signal": sig, "data": dat})

def _update_db(sig, dat):
    pth = dat["path"]
    md5 = dat["md5"]
    if sig == EVT.SYNC_LOCAL_MODIFIED:
        f = MOD.File.get_by_path(pth)
        f.md5 = md5
        f.save()
    elif sig == EVT.SYNC_LOCAL_DELETED:
        f = MOD.File.get_by_path(pth)
        f.delete_flag = True
        f.save()

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



