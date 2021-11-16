import requests
from bs4 import BeautifulSoup
import pickle_the_data
import backend_db

HOST = "https://google.by/"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
    "content-type": "text/html"}

r = requests.get(HOST, headers=headers)
data = r.content
soup = BeautifulSoup(data, "html.parser")


def total_amount_of_tags():
    return len(soup.find_all())


def define_all_tags_names():
    tags_list = [tag.name for tag in soup.find_all(True)]
    dict_with_tags_names_and_values = {i: tags_list.count(i) for i in sorted(set(tags_list))}
    print("All tags have been successfully saved as dictionary")
    return dict_with_tags_names_and_values


pickling_dict = pickle_the_data.pickling_the_dictionary(define_all_tags_names())
backend_db.add_pickled_dict_to_db(pickling_dict)
print(backend_db.view())


