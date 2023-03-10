class DictExtractor:
    def __init__(self, file):
        self.data = []

        with open(file, "r", encoding="utf-8") as dict:
            for line in dict:
                # adding a word only when two conditions preformed
                if line.find(":") != -1 and line.find(";") != -1:
                    self.data.append(line.strip())
    
    def get_data(self):
        """Getting data from dict."""
        return self.data

    def get_words_by_prefix(self, prefix, with_prefix):
        """Gets words by a prefix
            with_prefix - with or without prefixes"""
        buffer = []
        # it's a location after an index
        index = len(prefix)
        # it's a location after an index and a whitespace. First index
        # of the word
        start = index + 1
        for x in self.data:
            # if a prefix exists then adds a word
            if x[:index].find(prefix) != -1:
                buffer.append(x if with_prefix else x[start:])
            # if a prefix "all:" adds to buffer
            elif prefix == "all:":
                # plus two because ": " and we starts from a first letter
                # of the word
                start = x.find(":") + 2
                buffer.append(x if with_prefix else x[start:])
        return buffer

    def get_list_words_by_prefix(self, list, prefix, with_prefix):
        """Gets words by a prefix from a list
            with_prefix - with or without prefixes"""
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

    def get_clear_words_by_prefix(self, prefix):
        """Gets words by a prefix
            with_prefix - with or without prefixes"""
        buffer = []
        index = len(prefix)
        # plus one because a whitespace between the index and the word
        start = index + 1
        for x in self.data:
            if x[:index].find(prefix) != -1:
                end = x.find(" [")
                # if a transcription exists this end index is valid
                if end != -1:
                    buffer.append(x[start:end])
                else:
                    end = x.find(" - ")
                    # if a translation exists but the transcription is not
                    if end != -1:
                        buffer.append(x[start:end])
                    else:
                        # if only a word and a prefix exists
                        buffer.append(x[start:-1])
            elif prefix == "all:":
                # same thing
                start = x.find(":") + 2
                end = x.find(" [")
                if end != -1:
                    buffer.append(x[start:end])
                else:
                    end = x.find(" - ")
                    if end != -1:
                        buffer.append(x[start:end])
                    else:
                        buffer.append(x[start:-1])
        return buffer

    def show_data(self):
        """Showing data."""
        for x in self.data:
            print(x)
        print(len(self.data))

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
        """Finding a word in a dict line."""
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
        """Finding a transcription in a dict line."""
        buffer = ""
        transc_index = line.find(" [")
        start = transc_index + 1
        end = line.find("]") + 1

        if transc_index != -1:
            buffer = line[start:end]
        return buffer

    def find_transl(self, line):
        """Finding a translation in a dict line."""
        buffer = ""
        transl_index = line.find(" - ")
        start = transl_index + 3

        if transl_index != -1:
            buffer = line[start:-1]
        return buffer

    def find_prefix(self, line):
        """Finding a prefix in a dict line."""
        buffer = ""
        prefix_index = line.find(":")
        end = prefix_index + 1

        if prefix_index != -1:
            buffer = line[:end]
        return buffer