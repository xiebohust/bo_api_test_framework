import jsonpath
import pymysql
from pymysql.cursors import DictCursor
from config import *


class DBHandle:

    def __init__(self,host=DB_HOST,user=DB_USER,password=DB_PASSWORD,db=DB_NAME,port=DB_PORT):
        self.conn = pymysql.Connect(host=host,user=user,password=password,db=db,port=port,charset="utf8")
        self.cur = self.conn.cursor(cursor=DictCursor)

    def select_one(self, sql):
        self.cur.execute(sql)
        return self.cur.fetchone()

    def select_all(self, sql):
        self.cur.execute(sql)
        return self.cur.fetchall()

    def modify(self, sql):
        result = self.cur.execute(sql)
        self.conn.commit()
        return result

    def execute_sql(self,sql):
        '''
        执行sql
        :param sql: 增删改查
        :return:
        '''
        try:
            result = self.cur.execute(sql)
            if sql.lower().startswith("select"):
                return self.cur.fetchone()
            else:
                self.conn.commit()
                return result
        except Exception as e:
            print(e)
            return

    def __del__(self):
        print('del=========')
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()


if __name__ == '__main__':
   pass
    # r = {'aaa':'bb'}
    # # r = [1,2]
    # print(jsonpath.jsonpath(r,'$..*'))
    # print(jsonpath.jsonpath(r,'$.aaa'))


    # class BB:
    #     def func(self):
    #         return 55
    # a = getattr(BB(),'func')
    # print(a())



