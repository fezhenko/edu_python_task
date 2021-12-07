import yaml
import re


class yaml_reader:
    def __init__(self):
        filepath = "synonyms.YAML"
        with open(filepath, "r") as f:
            self.data = yaml.safe_load(f)

    def synonym_value(self, url):
        if url in self.data:
            return self.data[url]
        print(f"no synonyms exist for {url}")
        if not re.match('(?:http|ftp|https)://', url):
            return print('https://{}.by'.format(url))
        else:
            return f"{url}"


# y = yaml_reader()
# print(y.synonym_value("ydx"))
# # (ru|com|by|net$)