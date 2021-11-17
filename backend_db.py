import sqlite3
import tag_counter
import pickle_the_data


def connect():
    conn = sqlite3.connect('tag_counter.db')
    curs = conn.cursor()
    curs.execute("CREATE TABLE IF NOT EXISTS tags (id INTEGER PRIMARY KEY, Site_name text, url text, check_date "
                 "timestamp, 'tag_data' VARCHAR)")
    conn.commit()
    conn.close()


def view():
    conn = sqlite3.connect('tag_counter.db')
    curs = conn.cursor()
    curs.execute("SELECT * FROM tags")
    rows = curs.fetchall()
    conn.close()
    return rows


def insert(tag_data, site_name="", url="", check_date=""):
    conn = sqlite3.connect('tag_counter.db')
    curs = conn.cursor()
    curs.execute(f"SELECT tag_data FROM tags WHERE tag_data='{tag_data}'")
    if curs.fetchone() is None:
        curs.execute("""INSERT INTO tags VALUES(NULL,?,?,?,?)""", (tag_data, site_name, url, check_date))
        print("Pickled dictionary with tags has been added to tag_counter.db")
    else:
        print("Pickled_dict has been already added to warehouse :)")
    conn.commit()
    conn.close()


def show_dict_from_db(tag_data):
    conn = sqlite3.connect('tag_counter.db')
    curs = conn.cursor()
    curs.execute("SELECT tag_data FROM tags WHERE tag_data=?", (tag_data,))
    rows = curs.fetchall()
    conn.close()
    return rows


def view_urls():
    conn = sqlite3.connect('tag_counter.db')
    curs = conn.cursor()
    curs.execute("SELECT * FROM tags WHERE url!=?", ('',))
    rows = curs.fetchall()
    conn.close()
    return rows


def insert_url(url):
    conn = sqlite3.connect('tag_counter.db')
    curs = conn.cursor()
    curs.execute("SELECT url FROM tags WHERE url=?", (url,))
    if curs.fetchone() is None:
        curs.execute("""INSERT INTO tags VALUES(NULL,NULL,?,NULL,NULL)""", (url,))
    else:
        print("This URL has been already added to the list")
    conn.commit()
    conn.close()


connect()









# pickling_dict = pickle_the_data.pickling_the_dictionary(tag_counter.parse())
# insert(pickling_dict, url='newtext')
# insert_url('newtext')
#
# def urls():
#     return [row[2] for row in view_urls()]
#
# rint(urls())
