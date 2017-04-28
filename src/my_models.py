from peewee import *
import os

DB_NAME = "data.db"
database = SqliteDatabase(DB_NAME, **{})
def create_all_tables():
    if not os.path.exists(DB_NAME):
        database.connect()
        database.create_tables([File, Ebook])

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class File(BaseModel):
    ext = TextField(null=True)
    file_create_time = DateTimeField(null=True)
    last_check_time = DateTimeField(null=True)
    last_modify_time = DateTimeField(null=True)
    md5 = TextField(null=True, unique=True, index=True)
    name = TextField()
    path = TextField(null=True)
    size = IntegerField(null=True)
    uid = CharField(primary_key=True)

    class Meta:
        db_table = 't_file'

class Ebook(BaseModel):
    author = TextField(null=True)
    book_name = TextField(null=True)
    file = ForeignKeyField(File, related_name='ebooks')
    pub_time = DateField(null=True)
    publisher = TextField(null=True)
    translator = TextField(null=True)
    uid = CharField(primary_key=True)

    class Meta:
        db_table = 't_ebook'

