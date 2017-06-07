from peewee import *
import os
import hashlib
import uuid
from datetime import datetime

from my_glob import LOG

DB_NAME = "data.db"
database = SqliteDatabase(DB_NAME, **{})

def create_all_tables():
    if not os.path.exists(DB_NAME):
        database.create_tables([File, Ebook])
    else:
        database.connect()

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    @staticmethod
    def getFileMd5(fp):
        with open(fp, "r") as f:
            m = hashlib.md5()
            while True:
                data = f.read(10240)
                if not data:
                    break
                m.update(data)
        return m.hexdigest()

    @classmethod
    def getItems(cls):
        fs = []
        for f in cls.select():
            fs.append(f)
        return fs

    class Meta:
        database = database

class File(BaseModel):
    invalid = BooleanField(default=False)
    dirty = BooleanField(default=False)
    ext = TextField(null=True)
    file_create_time = DateTimeField(null=True)
    last_check_time = DateTimeField(null=True)
    last_modify_time = DateTimeField(null=True)
    md5 = TextField(null=True, unique=True, index=True)
    name = TextField()
    path = TextField(null=True, index=True)
    size = IntegerField(null=True)
    uid = CharField(primary_key=True)

    class Meta:
        db_table = 't_file'

    @staticmethod
    def add(pth, md5str):
        dirty = True
        fsize = os.path.getsize(pth)
        fname = os.path.basename(pth)
        fpath = os.path.abspath(pth)
        ltime = datetime.fromtimestamp(os.path.getmtime(pth))
        ctime = datetime.fromtimestamp(os.path.getctime(pth))
        fext = fname.split(".")
        fext = fext[len(fext) - 1].lower()
        f = File.create(uid=uuid.uuid4(), size=fsize, path=fpath, name=fname,
                        md5=md5str, last_modify_time=ltime, file_create_time=ctime,
                        last_check_time=datetime.now(), ext=fext, dirty=dirty)
        if f.ext in Ebook.exts:
            Ebook.create(uid=uuid.uuid4(), file=f, book_name=fname)
        return f

    @staticmethod
    def check(fp):
        if fp is None:
            return
        pth = os.path.abspath(fp)
        md5str = File.getFileMd5(pth)
        dirty = True
        try:
            f = File.select().where((File.md5 == md5str) | (File.path == pth)).get()
            if f.invalid:
                f.invalid = False
                f.save()

            if f.md5 != md5str:
                LOG.debug(u"{}: md5 diff, db:{}, cur:{}".format(f.name, f.md5, md5str))
            elif f.path != pth:
                LOG.debug(u"{}: path diff, db:{}, cur:{}".format(f.name, f.path, pth))
                f.path = fp
                f.save()
            else:
                dirty = False
        except File.DoesNotExist:
            f = File.add(pth, md5str)
        return f, dirty

    def remove(self):
        self.invalid = True
        self.save()

class Ebook(BaseModel):
    exts = ["pdf", "mobi", "epub", "txt", "azw3"]
    notes = TextField(null=True)
    rate = IntegerField(null=True)
    author = TextField(null=True)
    book_name = TextField(null=True)
    file = ForeignKeyField(File, related_name='ebook')
    pub_time = DateField(null=True)
    publisher = TextField(null=True)
    translator = TextField(null=True)
    uid = CharField(primary_key=True)

    class Meta:
        db_table = 't_ebook'

class Category(BaseModel):
    uid = CharField(primary_key=True)
