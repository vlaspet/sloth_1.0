from dict_extractor import DictExtractor
from re import split
from re import findall

class Dictionary(DictExtractor):
    def __init__(self, file):
        DictExtractor.__init__(self, file)
        self.dictionary = {}

        clear_words = self.get_clear_words_by_prefix("all:")
        for y in clear_words:
            splited_words = split(" |/|-", y)
            for z in splited_words:
                buff = z.strip(",!?").casefold()
                self.dictionary[buff] = None
        verbs = self.get_words_by_prefix("v:", True)
        for x in verbs:
            self.dictionary[self.adding_ed_v(x)] = None
            self.dictionary[self.adding_es_v(x)] = None
            self.dictionary[self.adding_ing_v(x)] = None
        verbs = self.get_words_by_prefix("vv:", True)
        for x in verbs:
            self.dictionary[self.adding_es_v(x)] = None
            self.dictionary[self.adding_ing_v(x)] = None

    def is_double_consonant_v(self, line):
        """for one or two syllable words that end in
            vowel-consonant (except x and w) or the stress
            is on the end syllable double the last letter
            and add -ing"""
        consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm',
            'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x']
        vowels = ['i', 'o', 'u', 'e', 'a']
        two_charact = ["ch", "sh", "th", "sc"]
        # two characters letters
        ratio_of_letters = {'c' : ['k', 's'], 's' : ['s', 'z'], 't' : ['t', 'd'],
            'j' : ['dj', 'j'], 'g' : ['dj', 'g'], 'ch' : ['ch'],
            'sh' : ['sh'], 'th' : ['th', '-th'],
            'sc' : ['sk', 'sh', 's'], 'q' : ['kw']}
        # the ratio of letters and their sounds in transcription

        words_buffer = self.find_word(line).split(" ")
        word = words_buffer[0]
        transc = self.find_transc(line)
        if len(words_buffer) > 1:
            # if words of a verb is more than one
            if word[-1] in consonants[:-2] and (
                word[-3:][1] in vowels and word[-3:][0] in consonants):
                # if a word ends in consonant-vowel-consonant
                if len(findall(r"[iouea]", word)) > 1:
                    # if vowels more than 1
                    if word[-4:-2] in two_charact:
                        # checking if it's a two characters letter
                        # if true than cons_word = 2 symbols
                        # we are checking second consonant from
                        # the end
                        cons_word = word[-4:-2]
                    else:
                        # if false than cons_word = 1 symbol
                        cons_word = word[-3:][0]
                    index = transc.find("'")
                    if index != -1 and index != 1:
                        # if the index was not found than the stress is
                        # on the first syllable this word doesn't fit
                        # and if "'" not on the first syllable
                        cons_transc = transc[index+1:]
                        if cons_word in ratio_of_letters:
                            # if a consonant in the ration
                            for x in ratio_of_letters[cons_word]:
                                # than go through every variant
                                if cons_transc[:len(x)] == x:
                                    # if a symbol of a transcription
                                    # corresponds to the ratio variant
                                    return True
                        else:
                            if cons_word == cons_transc[0]:
                                # checks out one letter consonant
                                return True
                else:
                    return True
        else:
            if word[-1] in consonants[:-2] and (
                word[-3:][1] in vowels and word[-3:][0] in consonants):
                # if a word ends in consonant-vowel-consonant
                if len(findall(r"[iouea]", word)) > 1:
                    # if vowels more than 1
                    if word[-4:-2] in two_charact:
                        # checking if it's a two characters letter
                        # if true than cons_word = 2 symbols
                        # we are checking second consonant from
                        # the end
                        cons_word = word[-4:-2]
                    else:
                        # if false than cons_word = 1 symbol
                        cons_word = word[-3:][0]
                    index = transc.find("'")
                    if index != -1 and index != 1:
                        # if the index was not found than the stress is
                        # on the first syllable this word doesn't fit
                        # and if "'" not on the first syllable
                        cons_transc = transc[index+1:]
                        if cons_word in ratio_of_letters:
                            # if a consonant in the ration
                            for x in ratio_of_letters[cons_word]:
                                # than go through every variant
                                if cons_transc[:len(x)] == x:
                                    # if a symbol of a transcription
                                    # corresponds to the ratio variant
                                    return True
                        else:
                            if cons_word == cons_transc[0]:
                                # checks out one letter consonant
                                return True
                else:
                    return True
        return False
        
    def adding_ing_v(self, line):
        consonants = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm',
            'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x']
        words_buffer = self.find_word(line).split(" ")
        word = words_buffer[0]

        if self.is_double_consonant_v(line):
                # for one or two syllable words that end in
                # vowel-consonant (except x and w) or the stress
                # is on the end syllable double the last letter
                # and add -ing
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
        words_buffer = self.find_word(line).split(" ")
        word = words_buffer[0]

        if self.is_double_consonant_v(line):
                # for one or two syllable words that end in
                # vowel-consonant (except x and w) or the stress
                # is on the end syllable double the last letter
                # and add -ed
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

        words_buffer = self.find_word(line).split(" ")
        word = words_buffer[0]

        if word[-2:] in ends_es:
            # if words end in any ends_es than add -es
            word += "es"
        elif word[-1] == "y" and word[-2:][0] in consonants[:-2]:
            # words end in -y we change the y to -ies
            word = word[:-1] + "ies"
        else:
            word += "s"
        return word

    def get_dictionary(self):
        return self.dictionary.keys()
