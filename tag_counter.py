import requests
from bs4 import BeautifulSoup

HOST = "https://google.by/"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
    "content-type": "text/html"}

r = requests.get(HOST, headers=headers)
data = r.content
soup = BeautifulSoup(data, "html.parser")


def define_all_tags_names():
    # tags_list = []
    # for tag in soup.find_all(True):
    #     tags_list += [tag.name]

    # dict_with_tags_names_and_values = {}
    # for i in sorted(set(tags_list)):
    #     dict_with_tags_names_and_values[i] = tags_list.count(i)
    #     print(f"Number of {i} tags: {str(tags_list.count(i))}")

    tags_list = [tag.name for tag in soup.find_all(True)]
    dict_with_tags_names_and_values = {i: tags_list.count(i) for i in sorted(set(tags_list))}
    # print(f"List of all tags: {str(tags_list)}")
    # print(f"Sorted list of distinct values: {str(sorted(set(tags_list)))}")
    # print(f"Dict with tags and numbers: {dict_with_tags_names_and_values}")

    return dict_with_tags_names_and_values


def total_amount_of_tags():
    return len(soup.find_all())


print(define_all_tags_names())
