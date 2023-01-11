from text_filter import TextFilter
from dictionary import Dictionary

class Finder(TextFilter, Dictionary):
    def __init__(self, dict_name, text_name):
        Dictionary.__init__(self, dict_name)
        TextFilter.__init__(self, text_name)
        self.new_words = []

        dic = self.get_dictionary()
        words = self.get_words()

        for x in words:
            if x not in dic:
                self.new_words.append(x)
    
    def get_new_words(self):
        return self.new_words
