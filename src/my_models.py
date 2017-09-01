from peewee import *
import os
import uuid
from datetime import datetime

DB_NAME = "data.db"
# database = SqliteDatabase(DB_NAME, **{})
database = MySQLDatabase(host="127.0.0.1", user="root", passwd="123456",
                         database="collector", charset="utf8")

def create_all_tables():
    tables = [File]
    if type(database) == SqliteDatabase:
        if not os.path.exists(DB_NAME):
            database.create_tables(tables)
        # else:
        #     database.connect()
    elif type(database) == MySQLDatabase:
        if len(database.get_tables()) == 0:
            database.create_tables(tables)
        # else:
        #     database.connect()

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

    @classmethod
    def getItems(cls):
        fs = []
        for f in cls.select():
            fs.append(f)
        return fs

    @classmethod
    def get_by_md5(cls, md5):
        try:
            f = File.select().where(File.md5 == md5).get()
        except File.DoesNotExist:
            f = None
        return f

    @classmethod
    def get_by_path(cls, pth):
        try:
            f = File.select().where(File.path == pth).get()
        except File.DoesNotExist:
            f = None
        return f

class File(BaseModel):
    class Meta:
        db_table = 't_file'

    uid = FixedCharField(max_length=36, primary_key=True)
    name = CharField(max_length=512)
    path = CharField(max_length=2048, null=True)
    size = IntegerField(null=True)
    ext = CharField(max_length=12, null=True)
    md5 = FixedCharField(max_length=32, null=True, unique=True, index=True)
    file_create_time = DateTimeField(null=True)
    file_modify_time = DateTimeField(null=True)
    create_time = DateTimeField(default=datetime.now)
    modify_time = DateTimeField(default=datetime.now)
    last_check_time = DateTimeField(null=True)
    dirty = BooleanField(default=True)
    delete_flag = BooleanField(default=False)

    @staticmethod
    def add(pth, md5str):
        fname = os.path.basename(pth)
        fpath = os.path.abspath(pth)
        fsize = os.path.getsize(pth)
        fn, fext = os.path.splitext(fname)
        ctime = datetime.fromtimestamp(os.path.getctime(pth))
        mtime = datetime.fromtimestamp(os.path.getmtime(pth))
        f = File.create(uid=uuid.uuid4(), name=fname, path=fpath, size=fsize, ext=fext,
                        md5=md5str, file_create_time=ctime, file_modify_time=mtime)
        # if f.ext in Ebook.exts:
        #     Ebook.create(uid=uuid.uuid4(), file=f, book_name=fn)
        return f

    def remove(self):
        self.delete_flag = True
        self.save()

class Ebook(BaseModel):
    exts = [".pdf", ".mobi", ".epub", ".txt", ".azw3"]
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
