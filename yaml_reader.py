import yaml
import re


class yaml_reader:
    def __init__(self):
        self.filepath = "synonyms.yaml"
        with open(self.filepath, "r") as f:
            self.data = yaml.safe_load(f)

    def check_synonym(self, value):
        if value in list(self.data.values()):
            return value
        else:
            if not re.match('(?:http|ftp|https)://', value):
                updated_url = str('https://{}'.format(value))
                return updated_url
                
    def create_synonym(self, key, value):
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

# y = yaml_reader()
# y.check_synonym('https://bing.com')
# y.create_synonym('bing', 'bing.com')

# # (ru|com|by|net$)
