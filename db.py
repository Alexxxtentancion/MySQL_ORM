import cymysql


class Database:
    def __init__(self, name):
        self.conn = cymysql.connect(host='127.0.0.1',
                                    port=3306,
                                    user='root',
                                    passwd='12345',
                                    db=name
                                    )
        self.cur = self.conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()

    @property
    def connection(self):
        return self.conn

    @property
    def cursor(self):
        return self.cur

    def commit(self):
        self.conn.commit()

    def execute(self, sql, params=None):
        self.cur.execute(sql, params or ())

    def fetchall(self):
        return self.cur.fetchall()

    def fetchone(self):
        return self.cur.fetchone()

    def parse(self, sql, class_):
        self.cur.execute(sql)
        res_tuple = self.cur.fetchall()
        res_desc = [i[0] for i in self.cur.description]
        res_d = [class_(**dict(zip(res_desc, res_tuple[i]))) for i in range(len(res_tuple))]
        return res_d

    def query_constructor(self, query,table, cond,id=None):
        if query.startswith('SELECT'):
            params = ['{}="{}"'.format(x, y) for x, y in cond.items()]
            params = (" AND ".join(params))
            return query.format(table,params)

        elif query.startswith('INSERT'):
            keys_list = [x for x in cond.keys()]
            values_list = [y for y in cond.values()]
            columns = (",".join(keys_list))
            values = str(values_list)[1:-1]
            return query.format(table,columns,values)
        elif query.startswith('DELETE'):
            return query.format(table,cond)
        elif query.startswith('UPDATE'):
            col_vals = ["{}='{}'".format(x, y) for x, y in cond.items()]
            col_vals = (",".join(col_vals))
            return query.format(table,col_vals,id)
        elif query.startswith('CREATE TABLE'):
            par_type_lst = ["{} {}".format(x, y) for x, y in cond.items()]
            par_type_lst = (",".join(par_type_lst))
            table_name = table.__name__
            return query.format(table_name,par_type_lst )










