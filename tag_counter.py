import requests
from bs4 import BeautifulSoup
from yaml_reader import yaml_reader

class Tag_counter:
    def __init__(self, url="https://google.by/"):
        self.HOST = url  # for example: "https://google.by/"
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/95.0.4638.69 Safari/537.36",
            "content-type": "text/html"}
        self.r = requests.get(self.HOST, headers=self.headers)
        self.data = self.r.content
        self.soup = BeautifulSoup(self.data, "html.parser")

    def tags_to_dict(self):
        tags_list = [tag.name for tag in self.soup.find_all(True)]
        dict_with_tags_names_and_values = {i: tags_list.count(i) for i in sorted(set(tags_list))}
        print("All tags have been successfully saved as dictionary")
        return dict_with_tags_names_and_values

    def total_amount_of_tags(self):
        return len(self.soup.find_all())

    # def define_all_tags_names():
    #     tags_list = [tag.name for tag in soup.find_all(True)]
    #     dict_with_tags_names_and_values = {i: tags_list.count(i) for i in sorted(set(tags_list))}
    #     print("All tags have been successfully saved as dictionary")
    #     return dict_with_tags_names_and_values


#
# t=Tag_counter("http://yandex.by")
# print(t.tags_to_dict())



#
# def find_value(filepath, i):
#     with open(filepath, "r") as f:
#         data = yaml.safe_load(f)
#         if i in data:
#             print(data[i])
#
# find_value("synonyms.yaml","ydx")