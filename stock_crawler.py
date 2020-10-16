import requests
from bs4 import BeautifulSoup
import json

base_url = 'https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=csv&date=20201015&stockNo='


def get_web_data(serial):
    text = '股票代號: ' + str(serial) + '\n'
    web_url = base_url + str(serial)
    print(web_url)
    try:
        r = requests.get(web_url)
        try:
            web_j = r.json()
            list_data = web_j['data']
            list_date = []
            for date in list_data:
                text = text + date + '\n'
            print(text)
            r.close()
        except:
            return
    except:
        print("Get url timeout")
        return


if __name__ == '__main__':
    get_web_data(1101)
