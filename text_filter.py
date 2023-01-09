import re

class TextFilter:
    def __init__(self, file):
        self.data = []
        with open(file, "r") as dict:
            dict_buff = {}
            for line in dict:
                buffer_line = line
                buffer_line = re.sub(r"[^A-Za-z'-]", ' ', buffer_line.casefold())
                buffer = buffer_line.split()
                if len(buffer) > 1:
                    for word in buffer:
                        buff = word.strip("-'")
                        dict_buff[buff] = None
                else:
                    buff = ''.join(filter(str.isalpha, str(buffer)))
                    dict_buff[buff] = None
            self.data = dict_buff.keys()
            dict.close()
    def get_words(self):
        return self.data

t = TextFilter("dict.txt")

w = t.get_words()
for x in w:
    print(x)
print(len(w))