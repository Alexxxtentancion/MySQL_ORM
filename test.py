from orm import *
from time import time
class Author(Model):
    # id = IntField()
    first_name = StringField()
    patronymic = StringField()
    last_name = StringField()
    country = StringField()
    date_of_birth = DateField()

    class Meta:
        table_name = 'core_user'


class Man(Author):
    sex = StringField()

    class Meta:
        table_name = 'core_user'
#
# a = Author.objects.get(id=237)
# print(a)
# print(a.__dict__)
# #

#
# objg = Author.objects.get(first_name='Фёдор',patronymic = 'Михайлович')
# print(objg)
#
# cr = Author.objects.create(first_name='Афанасий',last_name='Павлов')
# obj = Author.objects.get(id=3)
# obj.date_of_birth=[1998,3,3]
# print(getattr(Author,'table_name'))
# obj.save()
# print(Author.objects.all())
objx = Author(first_name='Илья',date_of_birth='1997-05-5')
objx.save()
