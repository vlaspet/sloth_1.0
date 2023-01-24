from random import shuffle

class CreateDict:
    def __init__(self):
        self.prefixes = ["n:", "v:", "vv:", "adj:", "adv:", "pre:",
            "con:", "pro:", "exc:", "int:", "pref:", "s:"]

    def set_dict(self, index, list):
        """Creates new dict with dividing symbols with
            blocks by 25 words, and by 200 a bigger block"""
        list_index = 0
        buffer = []
        size = len(list)

        # we're going through the all list of words
        for x in range(size):
            buffer.append("%s\n" % index)
            index += 1
            # it goes from 2 inclusive to 10
            for i in range(2, 10):
                for j in range(25):
                    buffer.append("%s\n" % list[list_index])
                    list_index += 1
                    # it's the exit from a loop if a list index is greater
                    # than his size
                    if list_index >= size:
                        return buffer
                # it stops adding divition to words after 8
                if i < 9:
                    buffer.append("*_%s_*\n" % i)
        return buffer

    def get_list_words_by_prefix(self, list, prefix, with_prefix):
        """Gets words by a prefix
            with_prefix - with or withou prefixes"""
        buffer = []
        index = len(prefix)
        start = index + 1
        for x in list:
            if x[:index].find(prefix) != -1:
                buffer.append(x if with_prefix else x[start:])
            elif prefix == "all:":
                start = x.find(":") + 2
                buffer.append(x if with_prefix else x[start:])
        return buffer

    def shuffle_dict(self, list):
        """Shuffles a dict"""
        buffer = list
        # shuffle with a random shuffle
        shuffle(buffer)
        return buffer

    def shuffle_in_order(self, list, list_of_prefixes, with_prefix):
        """Shuffles in order by a prefix list that you gave it.
            And shuffles elements inside a choosen prefix.
            list - a dictionary
            list_of_prefixes - a list of prefixes in order
            that you want.
            with_prefix - with or without prefixes"""
        buffer = []
        for x in list_of_prefixes:
            buffer += self.shuffle_dict(
                self.get_list_words_by_prefix(list, x, with_prefix))
        return buffer

    def shuffle_by_25_words(self, list):
        """Shuffles by 25 words in the current index order."""
        buffer = []
        # first and last indexes than shifts every loop on 25
        first = 0
        last = 25
        # we need to know a size for the valid last index
        size = len(list)

        while 1:
            # make a valid last index
            if size < last:
                last = size

            buffer.extend(self.shuffle_in_order(list[first:last],
                self.prefixes, True))

            # if the last index equals size we return the whole buffer
            if size == last:
                return buffer

            # shifting indexes on 25
            first += 25
            last += 25
        return buffer
        
    def create_dict(self, dict, name):
        """Creating a dictionary with a file name and setted a dict."""
        with open(name, "w") as file:
            for x in dict:
                file.write(x)
