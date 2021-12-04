import sqlite3
from tag_counter import Tag_counter
from pickle_the_data import Pickle


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('tag_counter.db')
        self.curs = self.conn.cursor()
        self.curs.execute(
            "CREATE TABLE IF NOT EXISTS tags (id INTEGER PRIMARY KEY, Site_name text, url text, check_date "
            "timestamp, 'tag_data' VARCHAR)")
        self.conn.commit()

    def view(self):
        self.curs.execute("SELECT * FROM tags")
        rows = self.curs.fetchall()
        return rows

    def insert(self, tag_data, site_name="", url="", check_date=""):
        self.curs.execute(f"SELECT tag_data FROM tags WHERE tag_data='{tag_data}'")
        if self.curs.fetchone() is None:
            self.curs.execute("""INSERT INTO tags VALUES(NULL,?,?,?,?)""", (tag_data, site_name, url, check_date))
            print("Pickled dictionary with tags has been added to tag_counter.db")
        else:
            print("Pickled_dict has been already added to warehouse :)")
        self.conn.commit()

    def show_dict_from_db(self, tag_data):
        self.curs.execute("SELECT tag_data FROM tags WHERE tag_data=?", (tag_data,))
        rows = self.curs.fetchall()
        return rows

    def view_urls(self):
        self.curs.execute("SELECT * FROM tags WHERE url!=?", ('',))
        rows = self.curs.fetchall()
        return rows

    def insert_url(self, url):
        self.curs.execute("SELECT url FROM tags WHERE url=?", (url,))
        if self.curs.fetchone() is None:
            self.curs.execute("""INSERT INTO tags VALUES(NULL,NULL,?,NULL,NULL)""", (url,))
        else:
            print("This URL has been already added to the list")
        self.conn.commit()

    def __del__(self):
        self.conn.close()

# pickling_dict = pickle_the_data.pickling_the_dictionary(tag_counter.parse())
# insert(pickling_dict, url='newtext')
# insert_url('newtext')
#
# def urls():
#     return [row[2] for row in view_urls()]
#
# rint(urls())
