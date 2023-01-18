from dict_extractor import DictExtractor
from text_filter import TextFilter
from re import split
from re import findall

class Dictionary:
    def __init__(self, file):
        self.data = []
        
        if self.is_dict(file):
            dict_e = DictExtractor(file)
            buffer = {}

            clear_words = dict_e.get_clear_words_by_prefix("all:")
            for y in clear_words:
                # spliting words by signs " ", "/", "-"
                splited_words = split(" |/|-", y)
                for z in splited_words:
                    # striping from ",", "!", "?" and making small letters
                    buff = z.strip(",!?").casefold()
                    buffer[buff] = None
            
            verbs = dict_e.get_words_by_prefix("v:", True)
            for x in verbs:
                # adding suffixes -ed, -es and -ing
                buffer[self.adding_ed_v(x)] = None
                buffer[self.adding_es_v(x)] = None
                buffer[self.adding_ing_v(x)] = None
            
            # irregular verbs
            verbs = dict_e.get_words_by_prefix("vv:", True)
            for x in verbs:
                buffer[self.adding_es_v(x)] = None
                buffer[self.adding_ing_v(x)] = None
            self.data = buffer.keys()
        else:
            # if it's not a dictionary
            text_f = TextFilter(file)
            self.data = text_f.get_words()


    def is_dict(self, file_name):
        """Checks if it's a dictionary, or just a text for
        a dictionary using. In dictionary must be minimum 3 words"""
        prefixes = ("n:", "v:", "vv:", "adj:", "adv:", "pre:",
            "con:", "pro:", "exc:", "int:", "pref:", "s:")
        matches = 0
        loop_number = 0

        with open(file_name, "r") as dict:
            for line in dict:
                loop_number += 1
                # if it loops more than tens times and not found
                # matches it's not a dictionary
                if loop_number == 10:
                    return False
                # checks the template of dictionary if it matches
                # then we'll check another conditions
                if line.find(":") != -1 and line.find(";") != -1:
                    prefix_index = line.find(":")
                    end = prefix_index + 1

                    if line[:end] in prefixes:
                        matches += 1
                    if matches == 3:
                        return True
            # if it has less than 10 lines and doesn't found 3 matches
            # it's not a dictionary
            return False

    def is_double_consonant_v(self, line):
        """for one or two syllable words that end in
            vowel-consonant (except x and w) or the stress
            is on the end syllable double the last letter
            and add -ing"""
        consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm',
            'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x']
        vowels = ['i', 'o', 'u', 'e', 'a']
        # two characters letters
        two_charact = ["ch", "sh", "th", "sc"]
        # the ratio of letters and their sounds in transcription
        ratio_of_letters = {'c' : ['k', 's'], 's' : ['s', 'z'], 't' : ['t', 'd'],
            'j' : ['dj', 'j'], 'g' : ['dj', 'g'], 'ch' : ['ch'],
            'sh' : ['sh'], 'th' : ['th', '-th'],
            'sc' : ['sk', 'sh', 's'], 'q' : ['kw']}

        # for checking verbs with more than one word
        words_buffer = self.find_word_in_dict(line).split(" ")
        # the base word of the verb
        word = words_buffer[0]
        transc = self.find_transc_in_dict(line)
        
        # if words of a verb is more than one
        if len(words_buffer) > 1:
            # if a word ends in consonant-vowel-consonant
            if word[-1] in consonants[:-2] and (
                word[-3:][1] in vowels and word[-3:][0] in consonants):
                # if vowels more than 1
                if len(findall(r"[iouea]", word)) > 1:
                    # checking if it's a two characters letter
                    # if true than cons_word = 2 symbols
                    # we are checking second consonant from
                    # the end
                    if word[-4:-2] in two_charact:
                        cons_word = word[-4:-2]
                    else:
                        # if false than cons_word = 1 symbol
                        cons_word = word[-3:][0]
                    index = transc.find("'")
                    # if the index was not found than the stress is
                    # on the first syllable this word doesn't fit
                    # and if "'" not on the first syllable
                    if index != -1 and index != 1:
                        cons_transc = transc[index+1:]
                        # if a consonant in the ration
                        if cons_word in ratio_of_letters:
                            # than go through every variant
                            for x in ratio_of_letters[cons_word]:
                                # if a symbol of a transcription
                                # corresponds to the ratio variant
                                if cons_transc[:len(x)] == x:
                                    return True
                        else:
                            # checks out one letter consonant
                            if cons_word == cons_transc[0]:
                                return True
                else:
                    return True
        else:
            # if a word ends in consonant-vowel-consonant
            if word[-1] in consonants[:-2] and (
                word[-3:][1] in vowels and word[-3:][0] in consonants):
                # if vowels more than 1
                if len(findall(r"[iouea]", word)) > 1:
                    # checking if it's a two characters letter
                    # if true than cons_word = 2 symbols
                    # we are checking second consonant from
                    # the end
                    if word[-4:-2] in two_charact:
                        cons_word = word[-4:-2]
                    else:
                        # if false than cons_word = 1 symbol
                        cons_word = word[-3:][0]
                    index = transc.find("'")
                    # if the index was not found than the stress is
                    # on the first syllable this word doesn't fit
                    # and if "'" not on the first syllable
                    if index != -1 and index != 1:
                        cons_transc = transc[index+1:]
                        # if a consonant in the ration
                        if cons_word in ratio_of_letters:
                            # than go through every variant
                            for x in ratio_of_letters[cons_word]:
                                # if a symbol of a transcription
                                # corresponds to the ratio variant
                                if cons_transc[:len(x)] == x:
                                    return True
                        else:
                            # checks out one letter consonant
                            if cons_word == cons_transc[0]:
                                return True
                else:
                    return True
        return False
        
    def adding_ing_v(self, line):
        consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm',
            'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x']
        words_buffer = self.find_word_in_dict(line).split(" ")
        word = words_buffer[0]

        # for one or two syllable words that end in
        # vowel-consonant (except x and w) or the stress
        # is on the end syllable double the last letter
        # and add -ing
        if self.is_double_consonant_v(line):
                word += word[-1] + 'ing'
        elif word[-2:][0] in consonants and word[-1] == 'e':
            # for words that end in a silent -e,
            # drop the -e and add -ing
            word = word[:-1] + 'ing'
        else:
            word += 'ing'
        return word

    def adding_ed_v(self, line):
        consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm',
            'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x']
        words_buffer = self.find_word_in_dict(line).split(" ")
        word = words_buffer[0]

        # for one or two syllable words that end in
        # vowel-consonant (except x and w) or the stress
        # is on the end syllable double the last letter
        # and add -ed
        if self.is_double_consonant_v(line):
            word += word[-1] + 'ed'
        elif word[-1] == "y" and word[-2][0] in consonants:
            # the verb ends in a consonant + -y
            # we change the y to i and add -ed
            word = word[:-1] + "ied"
        elif word[-1] == 'e':
            # for words that end in a -e, add -d
            word += 'd'
        else:
            word += 'ed'
        return word

    def adding_es_v(self, line):
        consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm',
            'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x']
        ends_es = ["zz", "ss", "ch", "sh", "x", "go", "do"]

        words_buffer = self.find_word_in_dict(line).split(" ")
        word = words_buffer[0]

        # if words end in any ends_es than add -es
        if word[-2:] in ends_es:
            word += "es"
        elif word[-1] == "y" and word[-2:][0] in consonants[:-2]:
            # words end in -y we change the y to -ies
            word = word[:-1] + "ies"
        else:
            word += "s"
        return word

    def find_word_in_dict(self, line):
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

    def find_transc_in_dict(self, line):
        buffer = ""
        transc_index = line.find(" [")
        # adding 1 to ignore a whitespace
        start = transc_index + 1
        # adding 1 to add a "]" charecter
        end = line.find("]") + 1

        if transc_index != -1:
            buffer = line[start:end]
        return buffer

    def get_dictionary(self):
        return self.data