import pickle
from random import randint
from tag_counter import Tag_counter

class Pickle:

    def __init__(self, x):
        self.filename = f"{randint(0, 10000)}_pickle"
        with open(self.filename, 'wb') as self.file:
            pickle.dump(x, self.file)
            self.file.close()
        print("Dictionary with tags is pickled")

    def unpickling_the_dictionary(self,x):
        content = open(x, 'rb')
        pickled_out = pickle.load(content)
        return pickled_out

p=Tag_counter()
print(type(p))
# pickling_dict = Pickle(p)

# p=Pickle()
# print(p.unpickling_the_dictionary())