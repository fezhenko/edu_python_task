import yaml


def read_yaml(filepath):
    with open(filepath, "r") as f:
        data = yaml.safe_load(f)
        return data


def add_to_yaml(filepath, data): #пока что перезаписывает файл.
    with open(filepath, "w") as file:
        yaml.dump(data, file)


path = "synonyms.yaml"
data2 = {"sword": 100, "qweerty": 5565}

q = read_yaml(path)
qwe = [i for i in q.keys()]
new_item = [i for i in data2.keys() if i not in qwe]

add_to_yaml(path,new_item)
print(q)
