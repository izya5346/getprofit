from peewee import *

db = SqliteDatabase('data.db')

class BaseModel(Model):

    class Meta:
        database = db
    
class Item(BaseModel):
    name = CharField(unique = True)
    buy_sum = FloatField()
    current_sum = FloatField()
    count = IntegerField()

Item.create_table()