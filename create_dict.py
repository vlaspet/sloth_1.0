from random import shuffle
from dict_extractor import DictExtractor

class CreateDict:
    def __init__(self):
        self.prefixes = ["n:", "v:", "vv:", "adj:", "adv:", "pre:",
            "con:", "pro:", "exc:", "int:", "pref:", "s:"]

    def set_dict(self, index, list):
        """Creates new dict with dividing symbols with
            blocks by 25 words, and by 200 a bigger block"""
        list_index = 0
        # index = 1
        self.buffer = []

        for x in range(len(list)):
            self.buffer.append("%s\n" % index)
            index += 1
            for i in range(2, 10):
                for j in range(25):
                    self.buffer.append("%s\n" % list[list_index])
                    list_index += 1
                    if list_index >= len(list):
                        return self.buffer
                if i != 9:
                    self.buffer.append("*_%s_*\n" % i)
        return self.buffer

    def get_list_words_by_prefix(self, list, prefix, with_prefix):
        """Gets words by a prefix
            with_prefix - with or withou prefixes"""
        self.buffer = []
        index = len(prefix)
        start = index + 1
        for x in list:
            if x[:index].find(prefix) != -1:
                self.buffer.append(x if with_prefix else x[start:])
            elif prefix == "all:":
                start = x.find(":") + 2
                self.buffer.append(x if with_prefix else x[start:])
        return self.buffer

    def shuffle_dict(self, list):
        """Shuffles a dict"""
        self.buffer = list
        shuffle(self.buffer)
        return self.buffer

    def shuffle_in_order(self, list, list_of_prefixes, with_prefix):
        """Shuffles in order by a prefix list that you gave it.
            And shuffles elements inside a choosen prefix.
            list - a dictionary
            list_of_prefixes - a list of prefixes in order
            that you want.
            with_prefix - with or without prefixes"""
        self.buffer = []
        for x in list_of_prefixes:
            self.buffer += self.shuffle_dict(
                self.get_list_words_by_prefix(list, x, with_prefix))
        return self.buffer

    def shuffle_by_25_words(self, list):
        buffer = []
        first = 0
        last = 25
        size = len(list)

        while 1:
            if size < last:
                last = size

            buffer.extend(self.shuffle_in_order(list[first:last],
                self.prefixes, True))

            if size == last:
                return buffer

            first += 25
            last += 25
        return buffer
        
    def create_dict(self, dict, name):
        with open(name, "w") as file:
            for x in dict:
                file.write(x)

# cd = CreateDict()
# d_e = DictExtractor("dict.txt")
# dictt = d_e.get_data()
# new_dict = cd.shuffle_by_25_words(dictt[3000:3200], cd.prefixes)
# dictionary = cd.set_dict(new_dict)

# cd.create_dict(dictionary, "16.txt")