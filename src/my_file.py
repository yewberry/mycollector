# -*- coding: utf-8 -*-
import os
import uuid
from datetime import datetime

from my_glob import LOG
from my_base import MyBase
import my_models as models

class MyFile(MyBase):
    def __init__(self, pth):
        super(MyFile, self).__init__()
        self.file = None
        self.init(pth)

    def init(self, p):
        if p is None:
            return
        pth = os.path.abspath(p)
        md5str = self.get_file_md5(pth)
        mf = models.File
        try:
            f = mf.select().where((mf.md5 == md5str) | (mf.path == pth)).get()
            if f.md5 != md5str:
                LOG.debug(u"{}: md5 diff, db:{}, cur:{}".format(f.name, f.md5, md5str))
            elif f.path != pth:
                LOG.debug(u"{}: path diff, db:{}, cur:{}".format(f.name, f.path, pth))
        except mf.DoesNotExist:
            fsize = os.path.getsize(pth)
            fname = os.path.basename(pth)
            fpath = os.path.abspath(pth)
            ltime = datetime.fromtimestamp(os.path.getmtime(pth))
            ctime = datetime.fromtimestamp(os.path.getctime(pth))
            fext = fname.split(".")
            fext = fext[len(fext) - 1].lower()
            self.file = mf.create(uid=uuid.uuid4(), size=fsize, path=fpath, name=fname,
                                  md5=md5str, last_modify_time=ltime, file_create_time=ctime,
                                  last_check_time=datetime.now(), ext=fext, dirty=True)
