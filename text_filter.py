import re

class TextFilter:
    def __init__(self, file):
        self.data = []
        with open(file, "r", encoding="utf-8") as dict:
            # using a dict because we need unique words
            dict_buff = {}
            for line in dict:
                buffer_line = line
                # that's filtering text from everything but not
                # from letters and symbols "'" and '-'
                buffer_line = re.sub(r"[^A-Za-z'-]", ' ', buffer_line.casefold())

                # splits line on parts by the whitespace
                buffer = buffer_line.split()
                if len(buffer) > 1:
                    for word in buffer:
                        buff = word.strip("-")
                        dict_buff[buff] = None
                elif len(buffer) == 1:
                    buff = buffer[0]
                    dict_buff[buff] = None
            self.data = dict_buff.keys()

    def get_words(self):
        return self.data