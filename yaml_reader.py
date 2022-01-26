import yaml
import re
from datetime import datetime
import logging
import tag_counter
import requests


class yaml_reader:
    def __init__(self):
        logging.basicConfig(format='%(asctime)s,%(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                            level=logging.INFO, filename=f'tag_counter.log')
        self.logger = logging.getLogger(__name__)
        self.filepath = "synonyms.yaml"
        with open(self.filepath, "r") as f:
            self.data = yaml.safe_load(f)

    def check_synonym(self, sname):
        if sname in self.data:
            self.logger.info(
                f"{self.data[sname]['synonym_name']} in the list of synonyms with value: {self.data[sname]['synonym_value']}")
            return self.data[sname]['synonym_value']
        else:
            self.logger.info(f"Value for synonym name: {sname} has not exist")
            return sname

    def add_synonym(self, key, value):
        """добавляет ключ и значение синонима в ямл файл"""
        global updated_url
        if key in self.data and self.data[key]['synonym_value'] == value:
            logging.info(f"URL:'{value}' already in the list of synonyms with Key:'{key}'")
            return self.data[key]['synonym_value']
        elif key in self.data and self.data[key]['synonym_value'] != value:
            logging.info(f"URL:'{value}'")
            logging.info(f"Key:'{key}' already in the list, but with another value:'{self.data[key]['synonym_value']}'")
            return self.data[key]['synonym_value']
        else:
            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/95.0.4638.69 Safari/537.36",
                "content-type": "text/html"}
            domens = ('.com', '.ru', '.by', '.net', '.org', '.io', '.info', '.gov', '.biz')
            if not re.search(r"^https?://[a-zA-Z0-9_.-]+", value) and re.search(r"\.[a-zA-Z]+/?$", value):
                try:
                    updated_url = f"http://{value}"
                    requests.get(updated_url, headers=headers)
                    self.data[key] = {'synonym_name': key, 'synonym_value': updated_url,
                                      'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                    with open(self.filepath, "w") as file:
                        yaml.dump(self.data, file)
                    logging.info(f"{value} is updated {updated_url}")
                    logging.info(f"URL:'{updated_url}' has been added with key:'{key}' to the list")
                except:
                    self.logger.info(f"{updated_url} cannot be reached")
                    try:
                        updated_url = f"https://{value}"
                        requests.get(updated_url, headers=headers)
                        self.data[key] = {'synonym_name': key, 'synonym_value': updated_url,
                                          'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                        with open(self.filepath, "w") as file:
                            yaml.dump(self.data, file)
                        logging.info(f"{value} is updated {updated_url}")
                        logging.info(f"URL:'{updated_url}' has been added with key:'{key}' to the list")
                    except:
                        self.logger.info(f"{updated_url} cannot be reached")
                return updated_url
            elif not re.search(r"\.[a-zA-Z]+/?$", value) and re.search(r"^https?://[a-zA-Z0-9_.-]+", value):
                try:
                    updated_url = f"{value}.com"
                    requests.get(updated_url, headers=headers)
                    self.data[key] = {'synonym_name': key, 'synonym_value': updated_url,
                                      'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                    with open(self.filepath, "w") as file:
                        yaml.dump(self.data, file)
                    logging.info(f"{value} is updated {updated_url}")
                    logging.info(f"URL:'{updated_url}' has been added with key:'{key}' to the list")
                except:
                    for i in domens:
                        try:
                            updated_url = requests.get(f'{value}.{i}')
                            requests.get(updated_url, headers=headers)
                            self.data[key] = {'synonym_name': key, 'synonym_value': updated_url,
                                              'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                            with open(self.filepath, "w") as file:
                                yaml.dump(self.data, file)
                            logging.info(f"{value} is updated {updated_url}")
                            logging.info(f"URL:'{updated_url}' has been added with key:'{key}' to the list")
                        except:
                            self.logger.info(f'{updated_url} cannot be reached')
                return updated_url
            elif not re.search(r'https?://[a-zA-Z0-9_.-]+\.[a-zA-Z]+/?', value):
                try:
                    updated_url = str('http://{}.com'.format(value))
                    requests.get(updated_url, headers=headers)
                    self.data[key] = {'synonym_name': key, 'synonym_value': updated_url,
                                      'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                    with open(self.filepath, "w") as file:
                        yaml.dump(self.data, file)
                    logging.info(f"{value} is updated {updated_url}")
                    logging.info(f"URL:'{updated_url}' has been added with key:'{key}' to the list")
                except:
                    self.logger.info(f"{updated_url} cannot be reached")
                    for i in domens:
                        try:
                            updated_url = f"https://{value}{i}"
                            requests.get(updated_url, headers=headers)
                            self.data[key] = {'synonym_name': key, 'synonym_value': updated_url,
                                              'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                            with open(self.filepath, "w") as file:
                                yaml.dump(self.data, file)
                            logging.info(f"{value} is updated {updated_url}")
                            logging.info(f"URL:'{updated_url}' has been added with key:'{key}' to the list")
                        except:
                            self.logger.info(f"{updated_url} cannot be reached")
                return updated_url
            else:
                self.data[key] = {'synonym_name': key, 'synonym_value': value,
                                  'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                with open(self.filepath, "w") as file:
                    yaml.dump(self.data, file)
                logging.info(f"URL: '{value}' is fine")
                logging.info(f"URL:'{value}' has been added to the list of synonyms with Key:'{key}'")
                return value

    def update_synonym(self, key, value):
        if re.search(r"https?://[a-zA-Z0-9_.-]+\.[a-zA-z]+/?", value):
            self.data[key] = {'synonym_name': key, 'synonym_value': value,
                              'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            with open(self.filepath, 'w') as file:
                yaml.dump(self.data, file)
                return
        elif re.search():
            pass
        else:
            with open(self.filepath, 'w') as file:
                yaml.dump(self.data, file)
                return

    def delete_synonym(self, key):
        with open(self.filepath, 'r') as file:
            content = yaml.safe_load(file)
            list_of_keys = list(content.keys())
            if key in list_of_keys:
                del content[key]
                logging.info(f"'{key}' is deleted from 'synonyms.yaml'")
                with open(self.filepath, 'w') as new_file:
                    yaml.dump(content, new_file)
            else:
                logging.info(f"'{key}' is not in 'synonyms.yaml'")

    def view_synonyms(self):
        with open(self.filepath, 'r') as file:
            content = yaml.safe_load(file)
            return content


if __name__ == '__main__':
    y = yaml_reader()
    y.add_synonym('avtomalinovka', 'av')
