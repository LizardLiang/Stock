import requests
import csv
import sql_connector
import json
from decimal import Decimal
from time import sleep
from bs4 import BeautifulSoup

base_url = "https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=csv&date="

num_cal = lambda num: float(num[1:]) if "+" in num else -1 * float(num[1:])


def get_str_month(month):
    if len(str(month)) < 2:
        str_m = "0" + str(month)
    else:
        str_m = str(month)
    return str_m


def get_web_data(serial, ip="0", year=2001, month=9):
    # print("Fetching stock id", serial, "in ", year, "/", month)
    str_m = get_str_month(month)

    web_url = base_url + str(year) + str_m + "01&stockNo=" + str(serial)
    try:
        if ip != "0":
            r = requests.get(web_url, proxies={"http": ip, "https": ip}, timeout=5)
        else:
            r = requests.get(web_url, timeout=5)
        try:
            web_t = r.text
            if "很抱歉，沒有符合條件的資料" in web_t:
                return 1
            rows = web_t.split("\r\n")
            if len(rows) <= 0:
                return 1
            rows = rows[2:]
            rows = rows[:-6]
            for row in rows:
                data = []
                d_list = row.split('","')
                for d in d_list:
                    if '"' in d:
                        d = d.replace('"', "")
                    d = d.replace(",", "")
                    data.append(d)
                try:
                    sql_connector.insert_data(
                        serial,
                        data[0],
                        data[1],
                        data[2],
                        data[3],
                        data[4],
                        data[5],
                        data[6],
                        str(num_cal(data[7])),
                        data[8],
                    )
                except Exception as ex:
                    print(ex)
                    return 0
        except Exception as ex:
            pass
        return 0
    except:
        return 1


if __name__ == "__main__":
    res = get_web_data(1101, "0", 2020, 11)
    print(res)
