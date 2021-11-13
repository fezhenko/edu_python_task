import requests
from random import randint
import pickle
from bs4 import BeautifulSoup
import db

HOST = "https://google.by/"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
    "content-type": "text/html"}

r = requests.get(HOST, headers=headers)
data = r.content
soup = BeautifulSoup(data, "html.parser")


def pickling_the_dictionary(x):
    filename = f"{randint(0, 10000)}_pickle"
    with open(filename, 'wb') as file:
        pickle.dump(x, file)
        file.close()
    print("Your file is pickled")
    return filename


def unpickling_the_dictionary(x):
    content = open(x, 'rb')
    pickled_out = pickle.load(content)
    return pickled_out


def total_amount_of_tags():
    return len(soup.find_all())


def define_all_tags_names():
    tags_list = [tag.name for tag in soup.find_all(True)]
    dict_with_tags_names_and_values = {i: tags_list.count(i) for i in sorted(set(tags_list))}
    print("Indicator of success")
    return dict_with_tags_names_and_values


db.create_pickle_warehouse()
pickling_dict = pickling_the_dictionary(define_all_tags_names())
db.add_pickled_dict_to_db(pickling_dict)
#unpickled_dict = unpickling_the_dictionary(pickling_dict)


#print(define_all_tags_names())
#print(len(pickling_dict))
print(db.view())
