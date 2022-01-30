import requests
from bs4 import BeautifulSoup
import logging
import yaml
import re
import argparse
from backend_db import Database


class Tag_counter:
    def __init__(self, url='helloworld'):
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
            domens = ('.com', '.ru', '.by', '.net', '.org', '.io', '.info', '.gov', '.biz')
            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/95.0.4638.69 Safari/537.36",
                "content-type": "text/html"}
            if not re.search(r'https?://[a-zA-Z0-9_.-]+\.[a-zA-Z]+/?', url):
                if not re.search(r'^https?://', url) and not re.search(r'\.[a-zA-Z]+/?$', url):
                    try:
                        self.HOST = f"https://{url}.com"
                        requests.get(self.HOST, headers=headers)
                        self.logger.info(f"url that will be used: {self.HOST}")
                    except:
                        for i in domens:
                            try:
                                self.HOST = f"https://{url}{i}"
                                requests.get(self.HOST, headers=headers)
                                self.logger.info(f"url that will be used: {self.HOST}")
                            except:
                                self.logger.info(f"{self.HOST} cannot be opened")
                elif re.search(r'\.[a-zA-Z]+/?$', url) and not re.search(r'^https?://', url):
                    try:
                        self.HOST = f"https://{url}"
                        requests.get(self.HOST, headers=headers)
                        self.logger.info(f"url that will be used: {self.HOST}")
                    except:
                        try:
                            self.HOST = f"http://{url}"
                            requests.get(self.HOST, headers=headers)
                            self.logger.info(f"url that will be used: {self.HOST}")
                        except:
                            self.logger.info(f"{self.HOST} cannot be opened")
                elif re.search(r'^https?://', url) and not re.search(r'\.[a-zA-Z]+/?$', url):
                    try:
                        self.HOST = f"{url}.com"
                        requests.get(self.HOST, headers=headers)
                        self.logger.info(f"url that will be used: {self.HOST}")
                    except:
                        for i in domens:
                            try:
                                self.HOST = f"{url}{i}"
                                requests.get(self.HOST, headers=headers)
                                self.logger.info(f"url that will be used: {self.HOST}")
                            except:
                                self.logger.info(f"{self.HOST} cannot be opened")
                else:
                    self.logger.info("lets look on this trouble")
            else:
                self.HOST = url
                self.logger.info(f"url that will be used: {self.HOST}")
        try:
            self.headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/95.0.4638.69 Safari/537.36",
                "content-type": "text/html"}
            self.r = requests.get(self.HOST, headers=self.headers)
            self.data = self.r.content
            self.soup = BeautifulSoup(self.data, "html.parser")
        except:
            self.logger.info(f"Unreachable website: {self.HOST}")

    def tags_to_dict(self):
        """find all tags in the """
        tags_list = [tag.name for tag in self.soup.find_all(True)]
        dict_with_tags_names_and_values = {i: tags_list.count(i) for i in sorted(set(tags_list))}
        self.logger.info(f"All tags have been successfully saved as dictionary as {dict_with_tags_names_and_values}")
        return dict_with_tags_names_and_values

    def site_name(self):
        try:
            name = self.soup.find('title').text
            self.logger.info(f"Site name is '{name}'")
            return name
        except:
            return None

    def total_amount_of_tags(self):
        self.logger.info(f"Number of tags on the page is '{len(self.soup.find_all())}'")
        return len(self.soup.find_all())

    # def define_all_tags_names():
    #     tags_list = [tag.name for tag in soup.find_all(True)]
    #     dict_with_tags_names_and_values = {i: tags_list.count(i) for i in sorted(set(tags_list))}
    #     print("All tags have been successfully saved as dictionary")
    #     return dict_with_tags_names_and_values


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="get the dict with existed website's tags")
    parser.add_argument('-g', '--get', type=str, help="get an amount of tags from the website")
    parser.add_argument('-v', '--view', type=str, help="get an amount of tags from the DB")
    args = parser.parse_args()

    if args.get:
        t = Tag_counter(args.get)
        tags = t.tags_to_dict()
        print(tags)
    elif args.view:
        t = Tag_counter(args.view)
        d = Database()
        tags = d.get_from_db(t.HOST)
        print(tags)
    else:
        t = Tag_counter()
        # d = Database()
        # tags = t.tags_to_dict()
        # sitename = t.site_name()
        # a=d.insert(tags,sitename,t.HOST)
