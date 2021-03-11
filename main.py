import stock_crawler as s_c
import stock_id
import stock_analyze as s_a
import main_view as mv
import FreeProxy as myproxy
import json
import datetime, calendar
import sql_connector as sql
import threading
import queue
from time import sleep

loop_year = False
month = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
# fail_list = []
# fail_key = {}


# class my_thread(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)

#     def run(self):
#         while 1:
#             if len(fail_list) == 0:
#                 sleep(1)
#             else:
#                 con = fail_list.pop()
#                 d_ls = con.split("-")
#                 res = s_c.get_web_data(d_ls[0], "0", d_ls[1], d_ls[2])
#                 if res == 1:
#                     fail_list.append(con)
#                 sleep(5)


class print_thread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while 1:
            msg = self.queue.get()
            print(msg)
            sleep(0.1)


def get_last_day_in_week_day(y, m):
    to_d = int(datetime.datetime.today().strftime("%d"))
    to_m = int(datetime.datetime.today().strftime("%m"))
    to_y = int(datetime.datetime.today().strftime("%Y"))
    to_d = to_d if to_m == m and y == to_y else calendar.monthrange(y, m)[1]

    # find first weekday from today
    born = 100
    while born > 4:
        born = calendar.weekday(y, m, to_d)
        if born > 4:
            to_d -= 1
            if to_d < 1:
                m -= 1
                if m < 1:
                    y -= 1
                    m = 12
                to_d = calendar.monthrange(y, m)
        elif to_m == m and to_y == y:
            to_d -= 1

    return to_d


class stock_thread(threading.Thread):
    def __init__(self, queue, ip, serial, p_queue, proxy):
        # initial class
        threading.Thread.__init__(self)
        self.queue = queue
        self.p_q = p_queue
        self.ip = ip
        self.serial = serial
        self.year = 2020
        self.proxy = proxy
        time_str = datetime.date.today().strftime("%m/%d/%Y")
        month_list = time_str.split("/")
        self.month = int(month_list[0])
        # print("Create Thread", serial)

    def run(self):
        # print("Start thread", self.serial)
        self.ip = myproxy.get_a_ip()
        # Continue to run if id queue is still exists
        while self.queue.qsize() > 0:
            # Get a id from queue
            id = self.queue.get()
            self.year = 2021

            if loop_year == True:
                # Get every data since 2000
                while self.year >= 2010:
                    # Use copy instead of assign to prevent original list be modified
                    m_list = month.copy()
                    res = 0
                    msg = (
                        "Thread "
                        + str(self.serial)
                        + " id "
                        + id
                        + " Start fetching year "
                        + str(self.year)
                        + " left "
                        + str(self.queue.qsize())
                    )
                    self.p_q.put(msg)
                    while len(m_list) > 0:
                        m = m_list.pop()
                        d = get_last_day_in_week_day(self.year, m)
                        is_exist = sql.check_date(id, self.year, m, d)
                        # Don't need future data
                        if (self.year == 2021 and m > self.month) or (is_exist == 1):
                            pass
                        else:
                            res = s_c.get_web_data(id, self.ip, self.year, m)
                            if res == 0:
                                sleep(5)
                                pass
                            elif res == 1:
                                # If current IP fail, get a new one
                                m_list.append(m)
                                self.ip = myproxy.get_a_ip()
                    # If every month in a year is gotten, move to previous year
                    msg = (
                        "Thread "
                        + str(self.serial)
                        + " id "
                        + id
                        + " Finish fetching year "
                        + str(self.year)
                        + " left "
                        + str(self.queue.qsize())
                    )
                    self.p_q.put(msg)
                    self.year -= 1
            else:
                msg = (
                    "Thread "
                    + str(self.serial)
                    + " id "
                    + id
                    + " Start fetching year "
                    + str(self.year)
                    + " left "
                    + str(self.queue.qsize())
                )
                self.p_q.put(msg)
                d = get_last_day_in_week_day(self.year, self.month)
                is_exist = sql.check_date(id, self.year, self.month, d)
                # Don't need future data
                if is_exist == 1:
                    pass
                else:
                    res = 1
                    while res > 0:
                        res = s_c.get_web_data(id, self.ip, self.year, self.month)
                        if res == 0:
                            msg = (
                                "Thread "
                                + str(self.serial)
                                + " id "
                                + id
                                + " Finish fetching year "
                                + str(self.year)
                                + " left "
                                + str(self.queue.qsize())
                            )
                            self.p_q.put(msg)
                            sleep(5)
                            pass
                        elif res == 1:
                            # If current IP fail, get a new one
                            self.ip = myproxy.get_a_ip()


def main():
    # id_list = stock_id.get_id()
    # sleep(5)
    with open("id_list.json") as json_file:
        id_json = json.load(json_file)
        id_list = id_json["id"]
        for id in id_list:
            print("id: " + str(id))
            s_c.get_web_data(id)
            sleep(5)


def read_id():
    with open("id_list.json") as json_file:
        id_json = json.load(json_file)
        id_list = id_json["id"]
        return id_list


# assign stock id to each ip
# assign another id when it's done
# use queue to assign stock id?
def test_ip():
    proxy = myproxy.FreeProxy()
    p_queue = queue.Queue()
    id_queue = queue.Queue()
    id_list = read_id()
    for id in id_list:
        id_queue.put(id)
    while not id_queue.empty():
        # Create a list to store thread class
        stock_th = []

        # Create 20 thread
        for i in range(40):
            # When creating thread get a ip on the way
            stock_th.append(stock_thread(id_queue, "", i, p_queue, proxy))
        stock_th.append(print_thread(p_queue))

        for th in stock_th:
            th.start()

        for th in stock_th:
            th.join()


def demo_func():
    print("hello")


if __name__ == "__main__":
    # main()
    test_ip()
    # print(get_last_day_in_week_day(2019, 12))
