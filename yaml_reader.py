import yaml
import re
from datetime import datetime


class yaml_reader:
    def __init__(self):
        self.filepath = "synonyms.yaml"
        with open(self.filepath, "r") as f:
            self.data = yaml.safe_load(f)

    def check_synonym(self, sname, svalue):
        if sname in self.data and self.data[sname] == svalue:
            print(self.data[sname])
            return self.data[sname]
        elif sname in self.data and self.data[sname] != svalue:
            print(
                f"'{sname}' in the list of synonyms, but value in the list:{self.data[sname]}, and your value is {svalue}")
        else:
            print(f"'{sname}','{svalue}' are not in the list of synonyms")

    def add_synonym(self, key, value):
        """добавляет ключ и значение синонима в ямл файл"""
        if key in self.data and self.data[key]['synonym_value'] == value:
            print(f"'{value}' as '{key}' is already in the list of synonyms")
            return self.data[key]['synonym_value']
        else:
            if not re.match('(?:http|ftp|https)://', value):
                updated_url = str('https://{}'.format(value))
                self.data[key] = {'synonym_name': key, 'synonym_value': updated_url,
                                  'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                with open(self.filepath, "w") as file:
                    yaml.dump(self.data, file)
                print(f"{value} is updated {updated_url}")
                print(f"synonym '{key}' has been added for {updated_url}")
                return updated_url
            else:
                self.data[key] = {'synonym_name': key, 'synonym_value': value,
                                  'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                with open(self.filepath, "w") as file:
                    yaml.dump(self.data, file)
                print(f"{value} is fine as url")
                print(f"{value} has been added to the list of synonyms as '{key}'")
                return value

    # def check_synonym(self, value):
    #     if value in list(self.data.keys()):
    #         return self.data[value]
    #     else:
    #         if not re.match('(?:http|ftp|https)://', value):
    #             updated_url = str('https://{}'.format(value))
    #             return updated_url

    # def create_synonym(self, key, value):
    #     """Создаёт словарь с синонимом и ссылкой для этого синонима и добавляет его в ямл файл"""
    #     my_dict = {key: value}
    #     url = my_dict[key]
    #     if key in self.data:
    #         print(f"'{key}' already in the list of synonyms")
    #         return url
    #     else:
    #         if not re.match('(?:http|ftp|https)://', my_dict[key]):
    #             updated_url = str('https://{}'.format(my_dict[key]))
    #             print(f"{my_dict[key]} is updated {updated_url}")
    #             my_dict[key] = updated_url
    #             with open(self.filepath, "a") as file:
    #                 yaml.dump(my_dict, file)
    #                 print(f"synonym '{key}' has been added for {my_dict[key]}")
    #             return updated_url
    #         else:
    #             print(f"{my_dict[key]} is fine as url")
    #             return url

    def delete_synonym(self, key):
        with open(self.filepath, 'r') as file:
            content = yaml.safe_load(file)
            list_of_keys = list(content.keys())
            if key in list_of_keys:
                del content[key]
                print(f"'{key}' is deleted from 'synonyms.yaml'")
                with open(self.filepath, 'w') as new_file:
                    yaml.dump(content, new_file)
            else:
                print(f"'{key}' is not in 'synonyms.yaml'")

    def view_synonyms(self):
        with open(self.filepath, 'r') as file:
            content = yaml.safe_load(file)
            return content


y = yaml_reader()
y.add_synonym('bing(correct_url)', 'https://bing.com')
# (ru|com|by|net$)
