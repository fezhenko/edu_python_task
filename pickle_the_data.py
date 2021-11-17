import pickle
from random import randint


def pickling_the_dictionary(x):
    filename = f"{randint(0, 10000)}_pickle"
    with open(filename, 'wb') as file:
        pickle.dump(x, file)
        file.close()
    print("Dictionary with tags is pickled")
    return filename


def unpickling_the_dictionary(x):
    content = open(x, 'rb')
    pickled_out = pickle.load(content)
    return pickled_out
