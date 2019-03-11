# -*- coding: utf-8 -*-

__author__ = "zhangzd"

import fofa
from settings import KEY, EMAIL
import sys

class Fofa:
    def __init__(self, email, key, query_str ):
        self.client = fofa.Client(email, key)
        self.query_str = 'domain="{}"'.format(query_str)
    def get_query_result(self):
        for page in range(1, 101):
            data = self.client.get_data(self.query_str, page=page, fields="ip, port, country, city, host, title")
            for ip, port, country, city, host, title in data["results"]:
                print("ip:%s port:%s country:%s city:%s host:%s title:%s" % (ip, port, country, city, host, title))

if __name__ == "__main__":
    try:
        query_str = sys.argv[1]
    except:
        sys.exit()
    fofa = Fofa(EMAIL, KEY, query_str)
    fofa.get_query_result()
