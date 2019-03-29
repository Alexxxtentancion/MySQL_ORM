import cymysql

from fields import *



class ModelMeta(type):
    def __new__(mcs, name, bases, namespace):
        if name == 'Model':
            return super().__new__(mcs, name, bases, namespace)
        # print(namespace)
        meta = namespace.get('Meta')
        if meta is None:
            raise ValueError('meta is none')
        if not hasattr(meta, 'table_name'):
            raise ValueError('table_name is empty')

        # todo mro
        # print(bases[0] != Model)
        if bases[0] != Model:
            fields = {**bases[0]._fields, **{k: v for k, v in namespace.items()
                                             if isinstance(v, Field)}}
        else:
            fields = {k: v for k, v in namespace.items()
                      if isinstance(v, Field)}

        namespace['_fields'] = fields
        namespace['_table_name'] = meta.table_name
        return super().__new__(mcs, name, bases, namespace)


class Manage:
    def __init__(self):
        self.conn = cymysql.connect(host='127.0.0.1',
                                    port=3306,
                                    user='root',
                                    passwd='12345',
                                    db='library')
        self.cur = self.conn.cursor()
        self.model_cls = None

    def __get__(self, instance, owner):
        if self.model_cls is None:
            self.model_cls = owner
        print(owner)
        setattr(self, '_table_name', owner._table_name)
        return self

    def all(self):
        query = 'SELECT * FROM {}'.format(self._table_name)
        print(query)
        self.cur.execute(query)
        tuple = self.cur.fetchall()
        res = [dict(zip([i[0] for i in self.cur.description], tuple[i])) for i in range(len(tuple))]
        a = [1, 2, 3, 4, 5]
        if len(tuple) == 0:
            raise DoesNotExist("Object does not exist in {}".format(self._table_name))
        else:
            return [self.model_cls(**dict(zip([i[0] for i in self.cur.description], tuple[i]))) for i in range(len(tuple))]

    def get(self, **kwargs):
        query = 'SELECT * FROM {} WHERE {}'.format(self._table_name,
                                                   (" AND ".join(['{}="{}"'.format(x, y) for x, y in kwargs.items()])))
        print(query)
        self.cur.execute(query)
        tuple = self.cur.fetchall()
        if len(tuple) > 1:
            raise MultyplyObjectReturn('The query respons Multyply object')
        elif len(tuple) == 0:
            raise DoesNotExist('No data match your query')
        else:
            res = dict(zip([i[0] for i in self.cur.description], tuple[0]))
            print(res)

        return self.model_cls(**res)

    def filter(self, **kwargs):
        query = 'SELECT * FROM {} WHERE {}'.format(self._table_name,
                                                   (" AND ".join(['{}="{}"'.format(x, y) for x, y in kwargs.items()])))
        self.cur.execute(query)
        tuple = self.cur.fetchall()
        print(query)
        res = [dict(zip([i[0] for i in self.cur.description], tuple[i])) for i in range(len(tuple))]
        print(res)
        # return res
        return [self.model_cls(**dict(zip([i[0] for i in self.cur.description], tuple[i]))) for i in range(len(tuple))]

    def create(self, **kwargs):
        query = 'INSERT INTO {} ({}) VALUES ({})'.format(self._table_name, (",".join([x for x in kwargs.keys()])),
                                                         str([y for y in kwargs.values()])[1:-1])

        print(query)
        self.cur.execute(query)
        # print(self.cur.description)
        self.conn.commit()
        return self.cur.fetchall()

    def delete(self, id):
        query = 'DELETE FROM {} WHERE id="{}"'.format(self._table_name, id)
        print(query)
        self.cur.execute(query)
        self.conn.commit()
        return "OK"


class Model(metaclass=ModelMeta):
    class Meta:
        table_name = ''

    objects = Manage()

    # todo DoesNotExist

    def __init__(self, *_, **kwargs):
        self.conn = cymysql.connect(host='127.0.0.1',
                                    port=3306,
                                    user='root',
                                    passwd='12345',
                                    db='library')
        self.cur = self.conn.cursor()
        self.model_cls = None
        setattr(self, 'id', kwargs.get('id'))
        for field_name, field in self._fields.items():
            value = field.validate(kwargs.get(field_name))
            setattr(self, field_name, value)

    def delete(self):
        query = 'DELETE FROM {} WHERE id={}'.format(self._table_name, self.id)
        print(query)
        self.cur.execute(query)
        self.conn.commit()

    def save(self):
        dict_t = {}
        for field_name, field in self._fields.items():
            if getattr(self, field_name) is not None:
                dict_t[field_name] = getattr(self, field_name)
        print(dict_t)
        if self.__dict__.get('id'):
            query = 'UPDATE {} SET {} WHERE id={};' \
                .format(self._table_name, (",".join(["{}='{}'".format(x, y) for x, y in dict_t.items()])), self.id
                        )
            print(query)
            self.cur.execute(query)
            self.conn.commit()
            self.cur.execute('select last_insert_id();')
            self.id = self.cur.fetchone()[0]
        else:
            query = 'INSERT INTO {} ({}) VALUES ({});' \
                .format(self._table_name, (",".join([x for x in dict_t.keys()])),
                        str([y for y in dict_t.values()])[1:-1])
            print(query)
            self.cur.execute(query)
            self.conn.commit()
            self.cur.execute('select last_insert_id();')
            self.id = self.cur.fetchone()[0]

