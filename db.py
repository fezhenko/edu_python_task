import sqlite3
from random import randint

global conn
global curs

conn = sqlite3.connect('tag_counter.db')
curs = conn.cursor()


# # create a table
# curs.execute('''CREATE TABLE IF NOT EXISTS tags (
#             tag_name VARCHAR(20) PRIMARY KEY,
#             tag_value INT)''')
# # подтвердили создание таблицы в базе
# conn.commit()
#
#
# def add_tag_and_value_to_the_db(tag_name, tag_value):
#     curs.execute(f"SELECT tag_name FROM tags WHERE tag_name='{tag_name}'")
#     if curs.fetchone() is None:
#         curs.execute("INSERT INTO tags VALUES(?,?)", (tag_name, tag_value))
#         conn.commit()
#         print("Value has been added successfully!")
#     else:
#         print('This tag is already exist')
#
#     # for i in curs.execute("""SELECT * FROM tags"""):
#     #     print(i)
#
#
# def add_dict_items_to_db_separately():
#     a = {"c": 3, "d": 4}
#     for x, y in a.items():
#         add_tag_and_value_to_the_db(x, y)

def create_pickle_warehouse():
    conn = sqlite3.connect('pickling_dict.db')
    curs = conn.cursor()
    curs.execute("""CREATE TABLE IF NOT EXISTS 'pickle_warehouse' (
                "pickled_dict" VARCHAR(1000000) PRIMARY KEY)
                """)
    conn.commit()


def add_pickled_dict_to_db(d):
    conn = sqlite3.connect('pickling_dict.db')
    curs = conn.cursor()
    curs.execute(f"SELECT 'pickled_dict' FROM 'pickle_warehouse' WHERE pickled_dict='{d}'")
    if curs.fetchone() is None:
        curs.execute("""INSERT INTO 'pickle_warehouse' VALUES(?)""", (d,))
        print("Your pickle in warehouse now. Enjoy!")
    else:
        print("Pickled_dict has been already added to warehouse :)")
    conn.commit()
