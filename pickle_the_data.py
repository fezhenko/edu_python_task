import pickle
from random import randint

a = {"ss": 123}


def qwe123():
    with open('data.pickle', 'wb') as file:
        pickle.dump(a, file)

    with open('data.pickle', 'rb') as file_2:
        pickled_data = pickle.load(file_2)

    return pickled_data


print(type(qwe123()))


def pickling_the_dictionary(x):
    filename = f'{randint(0, 10000)}.pickle'
    with open(filename, 'wb') as file:
        pickle.dump(x, file)
        file.close()
    print("Your file is pickled")
    return filename


def unpickling_the_dictionary(x):
    content = open(x, 'rb')
    pickled_out = pickle.load(content)
    return pickled_out


print(type(pickling_the_dictionary(a)))
print(type(unpickling_the_dictionary(pickling_the_dictionary(a))))
