import pymysql as mysql
import datetime, csv
from time import sleep

db_setting = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "password",
    "db": "mysql_test",
    "charset": "utf8",
}


def connect_to_sql():
    try:
        conn = mysql.connect(**db_setting)
        return conn
    except Exception as ex:
        print(ex)
    while conn == None:
        sleep(1)
        try:
            conn = mysql.connect(**db_setting)
            return conn
        except Exception as ex:
            print(ex)


def insert_id(conn, id_list):
    with conn.cursor() as cursor:
        for id in id_list:
            command = "INSERT INTO stock_id(id) VALUES (%s)"

            try:
                cursor.execute(command, id)
                conn.commit()
                conn.close()
            except Exception as ex:
                print(ex)


def StringToDate(date):
    d_list = date.split("/")
    year = int(d_list[0])
    d_list[0] = str(year + 1911) if year < 1911 else str(year)
    return "-".join(d_list)


def insert_data(id, date, amount, value, openp, highest, lowest, closep, diff, offer):
    conn = connect_to_sql()
    with conn.cursor() as cursor:
        date = StringToDate(date)
        command = (
            "INSERT INTO stock"
            + str(id)
            + "(日期 ,成交股數 ,成交金額 , 開盤價 , 最高價 , 最低價 , 收盤價 , 漲跌價差 , 成交筆數 ) VALUES("
            + '"%s"'
            + ", "
            + '"%s"'
            + ","
            + '"%s"'
            + ","
            + '"%s"'
            + ","
            + '"%s"'
            + ","
            + '"%s"'
            + ","
            + '"%s"'
            + ","
            + '"%s"'
            + ","
            + '"%s"'
            + ")"
        )

        cursor.execute(
            command % (date, amount, value, openp, highest, lowest, closep, diff, offer)
        )
        conn.commit()
        conn.close()


def receive_id(conn):
    with conn.cursor() as cursor:
        command = "SELECT * FROM stock_id"

        try:
            cursor.execute(command)
            results = cursor.fetchall()
            for res in results:
                create_stock_table(conn, res[1])
        except Exception as ex:
            print(ex)


def create_stock_table(conn, id):
    with conn.cursor() as cursor:
        print("Create table", id)
        command = (
            "CREATE TABLE IF NOT EXISTS stock"
            + str(id)
            + " (日期 DATE NOT NULL, 成交股數 VARCHAR(50),成交金額 VARCHAR(50), 開盤價 VARCHAR(50), 最高價 VARCHAR(50), 最低價 VARCHAR(50), 收盤價 VARCHAR(50), 漲跌價差 VARCHAR(50), 成交筆數 VARCHAR(50), "
            + " CONSTRAINT stock_pk PRIMARY KEY(日期))"
        )

        try:
            cursor.execute(command)
            conn.close()
        except Exception as ex:
            print(ex)


def delete_stock_table(conn, id):
    print("Delete table", id)
    with conn.cursor() as cursor:
        command = "DROP TABLE IF EXISTS stock%s"

        cursor.execute(command % id)
        conn.close()


def check_date(id, year, month):
    m = str(month) if month > 9 else "0" + str(month)
    date = str(year) + "/" + m
    date = StringToDate(date)
    d_list = []
    conn = connect_to_sql()
    with conn.cursor() as cursor:
        command = "SELECT * FROM stock" + str(id) + " WHERE 日期 regexp '^%s'"

        cursor.execute(command % date)
        res = cursor.fetchone()
        conn.close()
        if res == None:
            return 0
        return 1


def query_id(id):
    conn = connect_to_sql()
    with conn.cursor() as cursor:
        cmd = "SELECT 日期, 收盤價, 開盤價, 最高價, 最低價 FROM stock" + str(id) + " WHERE 日期 > '%s'"
        date = StringToDate("2010/01/01")
        cursor.execute(cmd % date)
        res = cursor.fetchall()
        conn.close()
        create_csv(res)


def create_csv(datas):
    with open("stock.csv", "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["日期", "收盤價", "開盤價", "最高價", "最低價"])
        for d in datas:
            writer.writerow(d)
        file.close()


if __name__ == "__main__":
    query_id(1101)