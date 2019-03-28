from orm import *

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

a = Author.objects.get(id=4)
print(a)