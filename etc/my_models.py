from peewee import *

# database = SqliteDatabase('etc/data.db', **{})
database = MySQLDatabase(host="127.0.0.1", user="root", passwd="123456",
                         database="collector", charset="utf-8")

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class TFile(BaseModel):
    dirty = BooleanField(null=True)
    ext = TextField(null=True)
    file_create_time = DateTimeField(null=True)
    invalid = BooleanField(null=True)
    last_check_time = DateTimeField(null=True)
    last_modify_time = DateTimeField(null=True)
    md5 = TextField(null=True, unique=True)
    name = TextField()
    path = TextField(index=True, null=True)
    size = IntegerField(null=True)
    uid = CharField(primary_key=True)

    class Meta:
        db_table = 't_file'

class TEbook(BaseModel):
    author = TextField(null=True)
    book_name = TextField(null=True)
    file = ForeignKeyField(db_column='file_id', rel_model=TFile, to_field='uid')
    pub_time = DateField(null=True)
    publisher = TextField(null=True)
    translator = TextField(null=True)
    uid = CharField(primary_key=True)

    class Meta:
        db_table = 't_ebook'

