import yaml
import re


class yaml_reader:
    def __init__(self):
        self.filepath = "synonyms.YAML"
        with open(self.filepath, "r") as f:
            self.data = yaml.safe_load(f)
        self.items = self.data.get()

    def synonym_value(self, url):
        if url in self.data:
            return self.data[url]
        print(f"no synonyms exist for {url}")
        if not re.match('(?:http|ftp|https)://', url):
            return str('https://{}.by'.format(url))
        else:
            return f"{url}"

    def add_to_yaml(self, data):
        with open(self.filepath, "w") as file:
            yaml.safe_dump(data, file)


data2 = {"sword": 100, "qweerty": 5565}
y = yaml_reader()
# print(y.synonym_value("ydx"))
y.add_to_yaml(data2)
# # (ru|com|by|net$)
