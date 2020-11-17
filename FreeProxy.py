import requests
import re

FP_url = "https://free-proxy-list.net/"


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