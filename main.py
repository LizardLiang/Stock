import stock_crawler
import stock_id
from time import sleep


def main():
    id_list = stock_id.get_id()
    sleep(5)
    for id in id_list:
        print('id: ' + str(id))
        stock_crawler.get_web_data(id)
        sleep(5)


if __name__ == "__main__":
    main()
