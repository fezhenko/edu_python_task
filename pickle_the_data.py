import pickle
from random import randint
import logging



def deserialization(x):
    deserialized = pickle.loads(x)
    logging.info(f"blob {x} has been loaded as {deserialized}")
    return deserialized


def serialization(x):
    serialized = pickle.dumps(x)
    filename = f"serialized_dict_{randint(0,1000)}"
    with open(filename, 'wb') as file:
        file.write(serialized)
    return serialized

# t = Tag_counter()
# serialization(t.tags_to_dict())
