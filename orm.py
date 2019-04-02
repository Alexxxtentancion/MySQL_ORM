import warnings

from db import Database
from fields import *

db = Database(name='library')


class ModelMeta(type):
    def __new__(mcs, name, bases, namespace):
        if name == 'Model':
            return super().__new__(mcs, name, bases, namespace)
        meta = namespace.get('Meta')
        if meta is None:
            namespace['_table_name'] = namespace['__qualname__']
            warnings.warn("Meta is None", Warning)
        else:
            namespace['_table_name'] = meta.table_name

        if bases[0] != Model:
            fields = {**bases[0]._fields, **{k: v for k, v in namespace.items()
                                             if isinstance(v, Field)}}
        else:
            fields = {k: v for k, v in namespace.items()
                      if isinstance(v, Field)}

        namespace['_fields'] = fields
        return super().__new__(mcs, name, bases, namespace)


class Manage:
    def __init__(self):
        self.model_cls = None

    def __get__(self, instance, owner):
        if self.model_cls is None:
            self.model_cls = owner
        setattr(self, '_table_name', owner._table_name)
        return self

    def all(self):
        all_query = 'SELECT * FROM {}'.format(self._table_name)
        print(all_query)
        res = db.parse(all_query, self.model_cls)
        if len(res) == 0:
            raise DoesNotExist("Object does not exist in {}".format(self._table_name))
        else:
            return res

    def get(self, **kwargs):
        query = 'SELECT * FROM {} WHERE {}'
        get_query = db.query_constructor(query, self._table_name, kwargs)
        print(get_query)
        res = db.parse(get_query, self.model_cls)
        if len(res) > 1:
            raise MultyplyObjectReturn('The query respons Multyply object')
        elif len(res) == 0:
            raise DoesNotExist('No data match your query')
        else:
            return res[0]

    def filter(self, **kwargs):
        query = 'SELECT * FROM {} WHERE {}'
        filter_query = db.query_constructor(query, self._table_name, kwargs)
        res = db.parse(filter_query, self.model_cls)
        return res

    def create(self, **kwargs):
        query = 'INSERT INTO {} ({}) VALUES ({})'
        create_query = db.query_constructor(query, self._table_name, kwargs)
        db.execute(create_query)
        db.commit()
        return db.fetchone()

    def delete(self, id):
        query = 'DELETE FROM {} WHERE id="{}"'
        delete_query = db.query_constructor(query, self._table_name, id)
        db.execute(delete_query)
        db.commit()
        return "OK"


class Model(metaclass=ModelMeta):
    class Meta:
        table_name = ''

    objects = Manage()

    def __init__(self, *_, **kwargs):
        self.model_cls = None
        setattr(self, 'id', kwargs.get('id'))
        for field_name, field in self._fields.items():
            value = field.validate(kwargs.get(field_name))
            setattr(self, field_name, value)

    @classmethod
    def create_table(cls):
        sql_types = {}
        for x, y in cls._fields.items():
            if isinstance(y, Field):
                sql_types[x] = y.dbtype
                if y.blank:
                    sql_types[x] += " NULL"
                else:
                    sql_types[x] += "NOT NULL"
        query = "CREATE TABLE IF NOT EXISTS {} (id INT AUTO_INCREMENT, {}, PRIMARY KEY (id));"
        create_table_query = db.query_constructor(query, cls, sql_types)
        print(create_table_query)
        db.execute(create_table_query)
        db.commit()

    def delete(self):
        query = 'DELETE FROM {} WHERE id={}'.format(self._table_name, self.id)
        print(query)
        db.execute(query)
        db.commit()

    def save(self):
        dict_t = {}
        for field_name, field in self._fields.items():
            if getattr(self, field_name) is not None:
                dict_t[field_name] = getattr(self, field_name)
        if self.__dict__.get('id'):
            query = 'UPDATE {} SET {} WHERE id={};'
            update_query = db.query_constructor(query, self._table_name, dict_t, self.id)
            print(update_query)
            db.execute(update_query)
            db.commit()
        else:
            query = 'INSERT INTO {} ({}) VALUES ({});'
            create_query = db.query_constructor(query, self._table_name, dict_t)
            db.execute(create_query)
            db.commit()
            db.execute('select last_insert_id();')
            self.id = db.fetchone()[0]
