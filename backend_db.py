import sqlite3
import logging
from tag_counter import Tag_counter
from datetime import datetime
import yaml_reader
import pickle


class Database:
    def __init__(self):
        logging.basicConfig(format='%(asctime)s,%(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                            level=logging.INFO, filename=f'tag_counter.log')
        self.conn = sqlite3.connect('tag_counter.db')
        self.curs = self.conn.cursor()
        logging.info("connected to DB")
        self.curs.execute(
            "CREATE TABLE IF NOT EXISTS tags (id INTEGER PRIMARY KEY, Site_name text, url text, check_date timestamp, "
            "tag_data text)")
        self.conn.commit()

    def view(self):
        self.curs.execute("SELECT * FROM tags")
        rows = self.curs.fetchall()
        return rows

    def insert(self, tag_data, site_name="", url="", check_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S')):
        serialized = pickle.dumps(tag_data)
        self.curs.execute(f'SELECT tag_data FROM tags WHERE tag_data=?', (serialized,))
        if self.curs.fetchone() is None:
            self.curs.execute("""INSERT INTO tags (id,tag_data, Site_name, url, check_date) VALUES(NULL,?,?,?,?)""",
                              (serialized, site_name, url, check_date))
            logging.info("Pickled dictionary with tags has been added to tag_counter.db")
            logging.info(f"tag_data={serialized}, site_name={site_name}, url={url}, check_date={check_date}")
        else:
            logging.info("The serialized_dict has been already added to warehouse :)")
        self.conn.commit()
        return serialized

    def get_from_db(self, blob):
        self.curs.execute(f"SELECT tag_data FROM tags WHERE tag_data=?", (blob,))
        deserialized = pickle.loads(blob)
        logging.info(f"Blob {blob} has been loaded as {deserialized}")
        return deserialized

    def view_urls(self):
        self.curs.execute("SELECT * FROM tags WHERE url!=?", ('',))
        rows = self.curs.fetchall()
        return rows

    def insert_url(self, url):
        self.curs.execute(f"SELECT url FROM tags WHERE url=?", (url,))
        if self.curs.fetchone() is None:
            self.curs.execute("""INSERT INTO tags (id,tag_data, Site_name, url, check_date) VALUES(NULL,NULL,NULL,?,NULL)""", (url,))
        else:
            logging.info("This URL has been already added to the list")
        self.conn.commit()

    def __del__(self):
        self.conn.close()


y = yaml_reader.yaml_reader()
website = y.check_synonym('youtube')
t = Tag_counter(website)
s_tags = t.tags_to_dict()

d = Database()

w = d.insert(s_tags, t.site_name(), website)
d.get_from_db(w)
