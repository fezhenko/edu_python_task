import yaml


def read_yaml(filepath):
    with open(filepath, "r") as f:
        data = yaml.safe_load(f)
        return data


def add_to_yaml(filepath, data):
    with open(filepath, "a") as file:
        yaml.dump(data, file)


def create_new_synonym(key, value):
    dict = {}
    dict[key] = value
    return dict


def delete(filepath, key):
    with open(filepath, 'r') as file:
        content = yaml.safe_load(file)
        list_of_keys = list(content.keys())
        print(list(content.keys()))
        if key in list_of_keys:
            del content[key]
            with open(filepath, 'w') as new_file:
                yaml.dump(content, new_file)
        else:
            print(f"{key} is not in 'synonyms.yaml'")


path = "synonyms.yaml"
delete(path, 'bing')

# def create_synonym(self, key, value):
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


# data2 = {'sword': 'https://google.com'}
#
# synonyms = read_yaml(path)
# synonyms_keys = [i for i in synonyms.keys()]
#
# new_dict = create_new_synonym('hello', 'https://www.youtube.com/')
# add_to_yaml(path, new_dict)
