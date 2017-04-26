# -*- coding: utf-8 -*-
from peewee import *

db = SqliteDatabase("data.db")
class BaseModel(Model):
    uuid = CharField()

    class Meta:
        database = db
