import sqlite3
import logging
from datetime import datetime
import pickle


class Database:
    def __init__(self):
        """Create connect to the database if exists, if not the sqlite database will be created as 'tag_counter.db'
        file"""
        logging.basicConfig(format='%(asctime)s,%(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                            level=logging.INFO, filename=f'tag_counter.log')
        self.conn = sqlite3.connect('tag_counter.db')
        self.curs = self.conn.cursor()
        self.curs.execute('''CREATE TABLE IF NOT EXISTS tags (id INTEGER PRIMARY KEY, tag_data text, Site_name text, 
        url text, check_date timestamp)''')
        self.conn.commit()

    def view(self):
        self.curs.execute("SELECT * FROM tags")
        rows = self.curs.fetchall()
        return rows

    def insert(self, tag_data, site_name="", url="", check_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S')):
        """Serialize the dict and put it into database as tag_data, site_name and URL as well, check_date is the date
        when you use insert function """
        serialized = pickle.dumps(tag_data)
        self.curs.execute(f'SELECT url FROM tags WHERE url=?', (url,))
        if self.curs.fetchone() is None:
            self.curs.execute('''INSERT INTO tags (id,tag_data, Site_name, url, check_date) VALUES(NULL,?,?,?,?)''',
                              (serialized, site_name, url, check_date))
            logging.info("Dictionary with tags has been serialized and added to DB")
            logging.info(f"tag_data={serialized}, site_name={site_name}, url={url}, check_date={check_date}")
        else:
            logging.info(f"The serialized_dict related to {url} has been already added to warehouse :)")
        self.conn.commit()
        return serialized

    def get_from_db(self, url):
        """Get serialized item from db, deserialize via 'pickle.loads' and return as dict"""
        self.curs.execute(f"SELECT tag_data FROM tags WHERE url=?", (url,))
        row = self.curs.fetchone()
        if row is None:
            logging.info(f"No data related to {url} has been stored in DB")
        else:
            deserialized = pickle.loads(row[0])
            logging.info(f"Blob {row} has been loaded as {deserialized}")
            return deserialized

    def view_urls(self):
        """Get all existed in DB URLs"""
        self.curs.execute("SELECT url FROM tags WHERE url IS NOT NULL")
        rows = self.curs.fetchall()
        return rows

    def __del__(self):
        self.conn.close()


if __name__ == '__main__':
    pass
