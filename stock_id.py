import requests
import json
import re
from bs4 import BeautifulSoup

base_url = 'https://isin.twse.com.tw/isin/C_public.jsp?strMode=2'


def get_id():
    print("Getting id")
    id_list = {'id': []}
    r = requests.get(base_url)
    web_html = BeautifulSoup(r.text)
    table_list = web_html.findAll('td')
    rule = re.compile('(\d+)(\w*)(\s)(\S+)')
    for td in table_list:
        if rule.match(td.text) is not None:
            id_list['id'].append(td.text.split('　')[0])

    r.close()
    print("Getting id done")
    return id_list


if __name__ == '__main__':
    list = get_id()
    with open('id_list.json', 'w') as json_file:
        json.dump(list, json_file)
