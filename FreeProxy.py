import requests
import re
import queue
from time import sleep
import threading

FP_url = "https://free-proxy-list.net/"

dist = []


class ProxyThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            if self.queue.qsize() < 40:
                r = requests.get(FP_url)
                ip_re = re.compile(r"\d+\.\d+\.\d+\.\d+:\d+")
                valid_ip = []
                # check if ip is usable
                for ip in ip_re.findall(r.text):
                    try:
                        # test up with website https://api.ipify.org?format=json
                        res = requests.get(
                            "https://api.ipify.org?format=json",
                            proxies={"http": ip, "https": ip},
                            timeout=1,
                        )
                        if ip not in dist:
                            # append approved ip
                            self.queue.put(ip)
                            dist.append(ip)
                    except:
                        pass
                sleep(0.5)
            else:
                sleep(1)


using_sl = {}


class FreeProxy:
    def __init__(self):
        self.queue = queue.Queue()
        self.queue.put("0")
        proxyThread = ProxyThread(self.queue)
        proxyThread.start()

    def get_ip(self, serial):
        ip = self.queue.get(block=True)
        if serial in using_sl:
            dist.remove(using_sl[serial])
        using_sl[serial] = ip
        print("pop ip", ip)
        return ip


def get_a_ip():
    while True:
        r = requests.get(FP_url)
        ip_re = re.compile(r"\d+\.\d+\.\d+\.\d+:\d+")
        valid_ip = []
        # check if ip is usable
        for ip in ip_re.findall(r.text):
            try:
                # test up with website https://api.ipify.org?format=json
                res = requests.get(
                    "https://api.ipify.org?format=json",
                    proxies={"http": ip, "https": ip},
                    timeout=1,
                )
                # append approved ip
                return ip
            except:
                pass


def get_ip_list():
    print("Start fetching ip list")
    # get ip list
    r = requests.get(FP_url)
    ip_re = re.compile(r"\d+\.\d+\.\d+\.\d+:\d+")
    valid_ip = []
    # check if ip is usable
    for ip in ip_re.findall(r.text):
        try:
            # test up with website https://api.ipify.org?format=json
            res = requests.get(
                "https://api.ipify.org?format=json",
                proxies={"http": ip, "https": ip},
                timeout=1,
            )
            # append approved ip
            valid_ip.append(ip)
            print("Get ip", ip)
            # return when ip number got 20
            if len(valid_ip) >= 20:
                return valid_ip
        except:
            pass
    # return even if ip number less than 20
    return valid_ip


if __name__ == "__main__":
    print(get_ip_list())