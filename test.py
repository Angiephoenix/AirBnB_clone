#!/usr/bin/python3


class Test:
    # my_dict = {
    #     "name": "Alpha",
    #     "age": 28,
    #     "sex": "female"
    # }

    def __init__(self):
        n = self.__class__.__name__
        print(type(n))
        print(n)
        print(type(self).__name__)


test = {'one': 1, 'two': 2, 'three': 3}

new_dict = {
    "country": "Lesotho",
    "population": 125000
}

# for k, v in new_dict.items():
#     x = test[v["__class__"]]
#     print(x)

x = Test()
