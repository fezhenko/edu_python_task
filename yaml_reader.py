import yaml
import re


class yaml_reader:
    def __init__(self):
        self.filepath = "synonyms.yaml"
        with open(self.filepath, "r") as f:
            self.data = yaml.safe_load(f)

    def check_synonym(self, value):
        if value in list(self.data.keys()):
            return self.data[value]
        else:
            if not re.match('(?:http|ftp|https)://', value):
                updated_url = str('https://{}'.format(value))
                return updated_url

    def create_synonym(self, key, value):
        """Создаёт словарь с синонимом и ссылкой для этого синонима и добавляет его в ямл файл"""
        my_dict = {key: value}
        url = my_dict[key]
        if key in self.data:
            print(f"'{key}' already in the list of synonyms")
            return url
        else:
            if not re.match('(?:http|ftp|https)://', my_dict[key]):
                updated_url = str('https://{}'.format(my_dict[key]))
                print(f"{my_dict[key]} is updated {updated_url}")
                my_dict[key] = updated_url
                with open(self.filepath, "a") as file:
                    yaml.dump(my_dict, file)
                    print(f"synonym '{key}' has been added for {my_dict[key]}")
                return updated_url
            else:
                print(f"{my_dict[key]} is fine as url")
                return url

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
y.create_synonym('bing', 'bing.com')
y.delete_synonym('bing')
y.view_synonyms()

# (ru|com|by|net$)
