# -*- coding: utf-8 -*-

__author__ = "zhangzd"

import fofa
import pymysql
from settings import KEY, EMAIL, mysql_conn
import sys


class Save_data:
    def __init__(self, mysql_conn):
        self.db = pymysql.connect(**mysql_conn)
        self.cursor = self.db.cursor()

    def save(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()

    def close(self):
        self.db.close()


class Fofa:
    def __init__(self, email, key, query_str ):
        self.client = fofa.Client(email, key)
        self.query_str = 'domain="{}" && after="2015" && before="2019-10-01"'.format(query_str)

    def get_query_result(self):
        save_data = Save_data(mysql_conn)
        for page in range(1, 101):
            data = self.client.get_data(self.query_str, page=page, fields="host, title, ip, domain, port, country, city")
            for host, title, ip, domain, port, country, city in data["results"]:
               # print("ip:%s port:%s country:%s city:%s host:%s title:%s" % (ip, port, country, city, host, title))
                sql = "insert into fofa(host, title, ip, domain, port, country, city) values\
                 ('%s', '%s', '%s', '%s', '%s', '%s', '%s')"%\
                 (host, title, ip, domain, port, country, city)
                save_data.save(sql)
        save_data.close()


if __name__ == "__main__":
    try:
        query_str = sys.argv[1]
    except:
        sys.exit()
    fofa = Fofa(EMAIL, KEY, query_str)
    fofa.get_query_result()
