from text_filter import TextFilter
from dictionary import Dictionary

class Finder:
    def __init__(self, dict_names, text_name):
        self.new_words = []

        dict_f = []
        for x in dict_names:
            dict_f.extend(Dictionary(x).get_dictionary())

        words_f = TextFilter(text_name).get_words()

        for x in words_f:
            if x not in dict_f:
                self.new_words.append(x)

    def get_new_words_from_lists(dict, words):
        buffer = []
        for x in words:
            if x not in dict:
                buffer.append(x)
        return buffer

    def get_new_words(self):
        return self.new_words