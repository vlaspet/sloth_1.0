class DictExtractor:
    def __init__(self, file):
        self.data = []
        self.buffer = []
        self.data_dict = {}

        with open(file, "r") as dict:
            for line in dict:
                if line.find(":") != -1 and line.find(";") != -1:
                    self.data.append(line.strip())
        
        for x in self.data:
            transc_index = x.find(" [")
            transl_index = x.find(" - ")
            prefix_index = x.find(":") + 1
            start_0 = prefix_index + 1
            # start_0 - starts after index
            start_1 = transc_index + 1
            # start_1 - starts from transcription
            end_1 = x.find("]") + 1
            # end_1 - the end of transcription
            start_2 = transl_index + 3
            # start_2 - the begening of a russion word

            if transc_index != -1 and transl_index != -1:
                self.data_dict[x[start_0:transc_index]] = [x[start_1:end_1],
                    x[start_2:-1], x[:prefix_index]]
            elif transc_index != -1:
                self.data_dict[x[start_0:transc_index]] = [x[start_1:end_1],
                    "None", x[:prefix_index]]
            elif transl_index != -1:
                self.data_dict[x[start_0:transl_index]] = ["None",
                    x[start_2:-1], x[:prefix_index]]

    
    def get_data(self):
        return self.data
    def get_dict_data(self):
        """Gets dictionary of words"""
        return self.data_dict

    def get_words_by_prefix(self, prefix, with_prefix):
        """Gets words by a prefix
            with_prefix - with or withou prefixes"""
        self.buffer = []
        index = len(prefix)
        start = index + 1
        for x in self.data:
            if x[:index].find(prefix) != -1:
                self.buffer.append(x if with_prefix else x[start:])
            elif prefix == "all:":
                start = x.find(":") + 2
                self.buffer.append(x if with_prefix else x[start:])
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

    def get_clear_words_by_prefix(self, prefix):
        """Gets words by a prefix
            with_prefix - with or withou prefixes"""
        self.buffer = []
        index = len(prefix)
        start = index + 1
        for x in self.data:
            if x[:index].find(prefix) != -1:
                end = x.find(" [")
                if end != -1:
                    self.buffer.append(x[start:end])
                else:
                    end = x.find(" - ")
                    if end != -1:
                        self.buffer.append(x[start:end])
                    else:
                        self.buffer.append(x[start:-1])
            elif prefix == "all:":
                start = x.find(":") + 2
                end = x.find(" [")
                if end != -1:
                    self.buffer.append(x[start:end])
                else:
                    end = x.find(" - ")
                    if end != -1:
                        self.buffer.append(x[start:end])
                    else:
                        self.buffer.append(x[start:-1])
        return self.buffer

    def get_word_inf(self, word, index):
        """It gets information about a word that you wrote.
            First it's create a dict then get an information
            from that dict.
            index - of a list in dict with 3 values
            of a transcription, a translation and a prefix
            If you write greater than or less than a number
            of a index. It returns all three items"""
        list = self.data_dict[word]
        buffer_str = ""
        if index >= 0 and index < 3:
            buffer_str += list[index]
            return buffer_str
        else:
            for x in list:
                buffer_str += x + " "
            return buffer_str.strip()

    def show_data(self):
        length = len(self.data)
        for x in range(length):
            print(self.data[x])
        print(length)
    def show_all_prefixes(self):
        """Shows all prefixes and them meaning"""
        lst = ["n: nouns", "v: verbs", "vv: irregular verbs",
            "adj: adjectives", "adv: adverbs", "pre: prepositions",
            "con: conjunctions", "pro: pronouns", "exc: exclamations",
            "int: interjections", "pref: prefixes", "s: sentences",
            "all: all words"]
        for x in lst:
            print(x)

    def find_word(self, line):
        buffer = ""
        prefix_index = line.find(":")
        start = prefix_index + 2

        end = line.find(" [")
        if end != -1:
            buffer = line[start:end]
        else:
            end = line.find(" - ")
            if end != -1:
                buffer = line[start:end]
            else:
                buffer = line[start:-1]
        return buffer
    def find_transc(self, line):
        buffer = ""
        transc_index = line.find(" [")
        start = transc_index + 1
        end = line.find("]") + 1

        if transc_index != -1:
            buffer = line[start:end]
        return buffer
    def find_transl(self, line):
        buffer = ""
        transl_index = line.find(" - ")
        start = transl_index + 3

        if transl_index != -1:
            buffer = line[start:-1]
        return buffer
    def find_prefix(self, line):
        buffer = ""
        prefix_index = line.find(":")
        end = prefix_index + 1

        if prefix_index != -1:
            buffer = line[:end]
        return buffer

d = DictExtractor("dict.txt")

l = d.get_data()
for x in l:
    print(d.find_transc(x))