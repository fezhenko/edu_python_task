import requests
from bs4 import BeautifulSoup
import logging
import yaml
import re


class Tag_counter:
    def __init__(self, url="https://google.by/"):
        logging.basicConfig(format='%(asctime)s,%(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                            level=logging.INFO, filename=f'tag_counter.log')
        logging.getLogger('urllib3').setLevel('WARNING')
        self.logger = logging.getLogger(__name__)
        self.filepath = "synonyms.yaml"

        with open(self.filepath, "r") as f:
            self.data = yaml.safe_load(f)
        if url in self.data:
            self.HOST = self.data[url]['synonym_value']
            self.logger.info(f"Synonym {self.data[url]['synonym_value']} is applied instead of {url}")
        else:
            if not re.match('(?:http|ftp|https)://', url):
                new_url = str('https://{}'.format(url))
                self.logger.info(f"Updated url: {new_url} is applied instead of {url}")
                self.HOST = new_url
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/95.0.4638.69 Safari/537.36",
            "content-type": "text/html"}
        self.r = requests.get(self.HOST, headers=self.headers)
        self.data = self.r.content
        self.soup = BeautifulSoup(self.data, "html.parser")


    def tags_to_dict(self, url):
        self.logger.info("All tags have been successfully saved as dictionary")
        tags_list = [tag.name for tag in self.soup.find_all(True)]
        dict_with_tags_names_and_values = {i: tags_list.count(i) for i in sorted(set(tags_list))}
        return dict_with_tags_names_and_values

    def site_name(self):
        name = self.soup.find('title').text
        self.logger.info(f"Site name is '{name}'")
        return name

    def total_amount_of_tags(self):
        self.logger.info(f"Number of tags on the page is '{len(self.soup.find_all())}'")
        return len(self.soup.find_all())

    # def define_all_tags_names():
    #     tags_list = [tag.name for tag in soup.find_all(True)]
    #     dict_with_tags_names_and_values = {i: tags_list.count(i) for i in sorted(set(tags_list))}
    #     print("All tags have been successfully saved as dictionary")
    #     return dict_with_tags_names_and_values

t=Tag_counter('vk.com')