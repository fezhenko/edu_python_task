import yaml
import re
from datetime import datetime
import logging
import requests


class Synonyms:
    def __init__(self):
        logging.basicConfig(format='%(asctime)s,%(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                            level=logging.INFO, filename=f'tag_counter.log')
        self.logger = logging.getLogger(__name__)
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/95.0.4638.69 Safari/537.36",
            "content-type": "text/html"}
        self.filepath = "synonyms.yaml"
        with open(self.filepath, "r") as f:
            self.data = yaml.safe_load(f)

    def check_synonym(self, sname):
        """Check for a value in list of synonyms. Return synonym value or None if synonym doesn't exist"""
        if sname in self.data:
            self.logger.info(
                f"{self.data[sname]['synonym_name']} in the list of synonyms with value: {self.data[sname]['synonym_value']}")
            return self.data[sname]['synonym_value']
        else:
            self.logger.info(f"Value for synonym name: {sname} has not exist")
            return None

    def add_synonym(self, key, value):
        """Check the key not in the synonyms list. Then add key as synonym_name,value as synonym_value to synonyms.yaml. If value does not match with 'http(s)://example.example' structure we will try to do request and adjust user's input"""
        global updated_url
        if key in self.data and self.data[key]['synonym_value'] == value:
            logging.info(f"URL:'{value}' already in the list of synonyms with Key:'{key}'")
            return self.data[key]['synonym_value']
        elif key in self.data and self.data[key]['synonym_value'] != value:
            logging.info(f"URL:'{value}'")
            logging.info(f"Key:'{key}' already in the list, but with another value:'{self.data[key]['synonym_value']}'")
            return self.data[key]['synonym_value']
        else:
            domens = ('.com', '.ru', '.by', '.net', '.org', '.io', '.info', '.gov', '.biz')
            if not re.search(r"^https?://[a-zA-Z0-9_.-]+", value) and re.search(
                    r"\.[a-zA-Z][a-zA-Z][a-zA-Z][a-zA-Z]?/?$", value):
                try:
                    self.updated_url = f"https://{value}"
                    requests.get(self.updated_url, headers=self.headers)
                    self.data[key] = {'synonym_name': key, 'synonym_value': self.updated_url,
                                      'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                    logging.info(f"URL:'{self.updated_url}' will be added with key:'{key}' to the list")
                except:
                    self.logger.info(f"{self.updated_url} cannot be reached")
                    try:
                        self.updated_url = f"http://{value}"
                        requests.get(self.updated_url, headers=self.headers)
                    except:
                        self.logger.info(f"{self.updated_url} cannot be reached")
                self.data[key] = {'synonym_name': key, 'synonym_value': self.updated_url,
                                  'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                with open(self.filepath, "w") as file:
                    yaml.dump(self.data, file)
                    logging.info(f"URL:'{self.updated_url}' has been added with key:'{key}' to the list")
                return
            elif not re.search(r"\.[a-zA-Z][a-zA-Z][a-zA-Z][a-zA-Z]?/?$", value) and re.search(
                    r"^https?://[a-zA-Z0-9_.-]+", value):
                try:
                    updated_url = f"{value}.com"
                    request = requests.get(updated_url, headers=self.headers)
                    if request.status_code == 200:
                        logging.info(f"URL:'{updated_url}' will be added with key:'{key}' to the list")
                        self.data[key] = {'synonym_name': key, 'synonym_value': updated_url,
                                          'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                        with open(self.filepath, "w") as file:
                            yaml.dump(self.data, file)
                        logging.info(f"URL:'{updated_url}' has been added with key:'{key}' to the list")
                        return
                except:
                    for i in domens:
                        try:
                            updated_url = requests.get(f'{value}.{i}')
                            self.logger.info(f"try to get response from {updated_url} ...")
                            request = requests.get(updated_url, headers=self.headers)
                            if request.status_code == 200:
                                self.data[key] = {'synonym_name': key, 'synonym_value': updated_url,
                                                  'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                                with open(self.filepath, "w") as file:
                                    yaml.dump(self.data, file)
                                logging.info(f"URL:'{updated_url}' has been added with key:'{key}' to the list")
                                return
                        except:
                            self.logger.info(f'{updated_url} cannot be reached')
                            return
            elif not re.search(r'https?://[a-zA-Z0-9_.-]+\.[a-zA-Z][a-zA-Z][a-zA-Z][a-zA-Z]?/?', value):
                try:
                    updated_url = str('https://{}.com'.format(value))
                    request = requests.get(updated_url, headers=self.headers)
                    if request.status_code == 200:
                        self.data[key] = {'synonym_name': key, 'synonym_value': updated_url,
                                          'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                        with open(self.filepath, "w") as file:
                            yaml.dump(self.data, file)
                        logging.info(f"URL:'{updated_url}' has been added with key:'{key}' to the list")
                        return
                except:
                    self.logger.info(f"{updated_url} cannot be reached")
                    for i in domens:
                        try:
                            self.logger.info(f"try to get response from {updated_url} ...")
                            updated_url = f"https://{value}{i}"
                            request = requests.get(updated_url, headers=self.headers)
                            if request.status_code == 200:
                                self.data[key] = {'synonym_name': key, 'synonym_value': updated_url,
                                                  'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                                with open(self.filepath, "w") as file:
                                    yaml.dump(self.data, file)
                                logging.info(f"URL:'{updated_url}' has been added with key:'{key}' to the list")
                                return
                        except:
                            self.logger.info(f"{updated_url} cannot be reached")
                            return
            else:
                self.data[key] = {'synonym_name': key, 'synonym_value': value,
                                  'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                with open(self.filepath, "w") as file:
                    yaml.dump(self.data, file)
                logging.info(f"URL:'{value}' has been added to the list of synonyms with Key:'{key}'")
                return

    def update_synonym(self, key, new_value, new_key=None):
        """update the synonym key, value in the synonyms.yaml"""
        domens = ('.com', '.ru', '.by', '.net', '.org', '.io', '.info', '.gov', '.biz')
        if key in self.data:
            if new_key is None and new_value is not None:
                if re.search(r"https?://[a-zA-Z0-9_.-]+\.[a-zA-Z][a-zA-Z][a-zA-Z][a-zA-Z]?/?", new_value):
                    self.data[key] = {'synonym_name': key, 'synonym_value': new_value,
                                      'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                    with open(self.filepath, 'w') as file:
                        yaml.dump(self.data, file)
                        return
                elif re.search(r"^https?://[a-zA-z0-9_.-]+", new_value):
                    self.logger.info(
                        f"Change the value:'{new_value}' and try again, URL should be ended with .com or smth like this")
                    print(
                        f"Change the value:'{new_value}' and try again, URL should be ended with .com or smth like this")
                elif re.search(r"[a-zA-Z0-9._-]+\.[a-zA-Z][a-zA-Z][a-zA-Z][a-zA-Z]?/?$", new_value):
                    try:
                        requests.get(f"https://{new_value}", headers=self.headers)
                        self.data[key] = {'synonym_name': key, 'synonym_value': f"http://{new_value}",
                                          'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                        with open(self.filepath, 'w') as file:
                            yaml.dump(self.data, file)
                            return
                    except:
                        requests.get(f"http://{new_value}", headers=self.headers)
                        self.data[key] = {'synonym_name': key, 'synonym_value': f"https://{new_value}",
                                          'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                        with open(self.filepath, 'w') as file:
                            yaml.dump(self.data, file)
                            return
                else:
                    logging.info(f"new_value only: Change the value:'{new_value}' and try again")
            elif new_key is not None and new_value is not None:
                if re.search(r"https?://[a-zA-Z0-9_.-]+\.[a-zA-Z][a-zA-Z][a-zA-Z][a-zA-Z]?/?", new_value):
                    self.data[key] = {'synonym_name': new_key, 'synonym_value': new_value,
                                      'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                    with open(self.filepath, 'w') as file:
                        yaml.dump(self.data, file)
                        return
                elif re.search(r"^https?://[a-zA-z0-9_.-]+", new_value):
                    self.logger.info(
                        f"Change the URL:'{new_value}' and try again, URL should be in format https://example.com")
                    print(
                        f"Change the URL:'{new_value}' and try again, URL should be in format https://example.com")
                elif re.search(r"\.[a-zA-Z][a-zA-Z][a-zA-Z][a-zA-Z]?/?$", new_value):
                    try:
                        requests.get(f"https://{new_value}", headers=self.headers)
                        self.data[key] = {'synonym_name': new_key, 'synonym_value': f"http://{new_value}",
                                          'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                        with open(self.filepath, 'w') as file:
                            yaml.dump(self.data, file)
                            return
                    except:
                        requests.get(f"http://{new_value}", headers=self.headers)
                        self.data[key] = {'synonym_name': new_key, 'synonym_value': f"https://{new_value}",
                                          'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                        with open(self.filepath, 'w') as file:
                            yaml.dump(self.data, file)
                            return
                else:
                    try:
                        requests.get(f"https://{new_value}.com", headers=self.headers)
                        self.data[key] = {'synonym_name': new_key, 'synonym_value': f"https://{new_value}.com",
                                          'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                        with open(self.filepath, 'w') as file:
                            yaml.dump(self.data, file)
                            return
                    except:
                        for i in domens:
                            try:
                                try_url = f"https://{new_value}{i}"
                                request = requests.get(try_url, headers=self.headers)
                                if request.status_code == 200:
                                    with open(self.filepath, 'w') as file:
                                        yaml.dump(self.data, file)
                                        return
                            except:
                                logging.info(
                                    f"new_key+new_value: Change the value:'{new_value}' and try again. Use described format https://example.com")
            elif new_key is None and new_value is None:
                logging.info(f"At least Synonym name and URL should be filled. Please try again")
            else:
                logging.info(f"URL is necessary field, fill it and try again")
        else:
            logging.info(f"Synonym with name:{key} doesn't exist")

    def delete_synonym(self, synonym_name):
        with open(self.filepath, 'r') as file:
            content = yaml.safe_load(file)
            list_of_keys = list(content.keys())
            if synonym_name[0] in list_of_keys:
                del content[synonym_name[0]]
                logging.info(f"'{synonym_name[0]}' is deleted from 'synonyms.yaml'")
                with open(self.filepath, 'w') as new_file:
                    yaml.dump(content, new_file)
            else:
                logging.info(f"'{synonym_name[0]}' is not in 'synonyms.yaml'")

    def view_synonyms(self):
        """Return values from synonyms.yaml to use them at the frontend"""
        with open(self.filepath, 'r') as file:
            content = yaml.safe_load(file)
            return content.values()


if __name__ == '__main__':
    y = Synonyms()
    # y.add_synonym('avtomalinovka', 'av')
    # y.update_synonym('avtomalinovka', 'av.by', 'av.by')
    # y.delete_synonym('avtomalinovka')
    # print(y.view_synonyms())
    # for row in y.view_synonyms():
    #     print(f"'{row['synonym_name']}': {row['synonym_value']}")
