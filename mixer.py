from re import findall
from random import shuffle

whole_words = []
only_words = []
only_russian_words = []
dict_idx = 0
bool_first = True

with open("dict.txt", "r", encoding="utf-8") as file:
    for line in file:
        if bool_first and findall(r"[1-9]*\n", line):
            dict_idx = int(findall(r"[1-9]*\n", line)[0])
            bool_first = False
        if line.find(":") != -1 and line.find(";") != -1:
            whole_words.append(line.strip())

def get_list_words_by_prefix(list, prefix, with_prefix):
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

def shuffle_dict(list):
    """Shuffles a dict"""
    buffer = list
    # shuffle with a random shuffle
    shuffle(buffer)
    return buffer

def shuffle_in_order(list, list_of_prefixes, with_prefix):
    """Shuffles in order by a prefix list that you gave it.
        And shuffles elements inside a choosen prefix.
        list - a dictionary
        list_of_prefixes - a list of prefixes in order
        that you want.
        with_prefix - with or without prefixes"""
    buffer = []
    for x in list_of_prefixes:
        buffer += shuffle_dict(
            get_list_words_by_prefix(list, x, with_prefix))
    return buffer

def shuffle_by_25_words(list):
    """Shuffles by 25 words in the current index order."""

    prefixes = ["n:", "v:", "vv:", "adj:", "adv:", "pre:",
            "con:", "pro:", "exc:", "int:", "pref:", "s:"]

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

        buffer.extend(shuffle_in_order(list[first:last],
            prefixes, True))

        # if the last index equals size we return the whole buffer
        if size == last:
            return buffer

        # shifting indexes on 25
        first += 25
        last += 25
    return buffer

def set_dict(index, list):
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

whole_words = shuffle_by_25_words(whole_words)

for line in whole_words:
    end = line.find(" - ")

    if end != -1:
        only_russian_words.append(line[end + 3 :])
    else:
        only_russian_words.append(line)

    # if it has translation to that place
    if end != -1:
        only_words.append(line[: end] + ";")
    else:
        end = line.find("]")
        # if it hasn't translation but has
        # transcription, to the end of the transcription
        if end != -1:
            only_words.append(line[: end+1] + ";")
        else:
            # if that is just a word without anything
            only_words.append(line)

whole_words = set_dict(dict_idx, whole_words)
only_words = set_dict(dict_idx, only_words)
only_russian_words = set_dict(dict_idx, only_russian_words)

# whole words
with open("dict.txt", "w", encoding="utf-8") as file:
    file.writelines(whole_words)

# just words
with open("words.txt", "w", encoding="utf-8") as file:
    file.writelines(only_words)

# just russian words
with open("russian_words.txt", "w", encoding="utf-8") as file:
    file.writelines(only_russian_words)