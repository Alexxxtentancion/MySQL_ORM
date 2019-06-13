from orm import *
from time import time
class Author(Model):
    # id = IntField()
    first_name = StringField(blank=True)
    patronymic = StringField(blank=True)
    last_name = StringField(blank=True)
    country = StringField(blank=True)
    _float = FloatField(blank=True)
    date_of_birth = DateField(blank=True)


Author.create_table()
a = Author(first_name="Иван",last_name="Петров",_float = 3.0,date_of_birth = "2000-03-13")
a.save()


