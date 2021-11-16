import sqlite3

global conn
global curs


def connect():
    conn = sqlite3.connect('tag_counter.db')
    curs = conn.cursor()
    curs.execute("CREATE TABLE IF NOT EXISTS tags (id INTEGER PRIMARY KEY, Site_name text, URL text, check_date "
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


def add_pickled_dict_to_db(tag_data, Site_name="", URL="", check_date=""):
    conn = sqlite3.connect('tag_counter.db')
    curs = conn.cursor()
    curs.execute(f"SELECT tag_data FROM tags WHERE tag_data='{tag_data}'")
    if curs.fetchone() is None:
        curs.execute("""INSERT INTO tags VALUES(NULL,?,?,?,?)""", (tag_data, Site_name, URL, check_date))
        print("Pickled dictionary with tags has been added to tag_counter.db")
    else:
        print("Pickled_dict has been already added to warehouse :)")
    conn.commit()
    conn.close()

connect()