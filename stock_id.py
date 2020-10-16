import requests
import json
import re
from bs4 import BeautifulSoup

base_url = 'https://isin.twse.com.tw/isin/C_public.jsp?strMode=2'


def get_id():
    id_list = []
    r = requests.get(base_url)
    web_html = BeautifulSoup(r.text, 'lxml')
    table_list = web_html.findAll('td')
    table_list = table_list[8:]
    rule = re.compile('(\d+)(\s)(\S+)')
    for td in table_list:
        if rule.match(td.text) is not None:
            id_list.append(td.text.split('　')[0])

    r.close()
    return id_list


if __name__ == '__main__':
    get_id()
