import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox

from dumper import Dumper
from create_dict import CreateDict
from finder import Finder
from dictionary import Dictionary
from windows import Window

class Functionality(Window):
    def __init__(self):
        # initializing Window
        Window.__init__(self)

        self.dump = Dumper("dump.pickle")
        self.create_d = CreateDict()

        # current prefixes in my dictionary
        self.prefixes = ["n:", "v:", "vv:", "adj:", "adv:", "pre:",
            "con:", "pro:", "exc:", "int:", "pref:", "s:"]

        # for finding in text every whole word
        self.text_word_indexes = []
        self.text_next_index = 0
        self.text_find_word = ""

        # for finding in dict every whole word
        self.dict_word_indexes = []
        self.dict_next_index = 0
        self.dict_find_word = ""

        # everything from window
        self.sessions = []
        self.current_session = ""
        self.current_session_index = 0
        self.dicts = []
        self.path_text = ""
        self.path_dict = ""
        self.opened_text = False
        self.opened_dict = False
        self.new_words = []
        self.dict_find_word = ""
        self.word = ""
        self.transc = ""
        self.transl = ""

    def start(self):
        self.init_sloth()

        # to start mainloop() for window
        self.start_loop()

    def help(self):
        """A help about a program."""
        print("Names for every part of the window!")
        s = """
        sessions - a key for a list of savings names. It's
        saving as a independent part of dump.
        dicts - files that used for additional dicts
        text - a path for a text.
        dict - a path for a dictionary.
        opened_text - was a text file opened then True.
        opened_dict - was a dict file opened then True.
        new_words - a path for new words.
        dict_find_word - a word for finding in dict.
        pref - a prefix of the word.
        word - a new word for a saving in the dictionary.
        transc - a transcription word for the word.
        transl - a translation word for the word.
        """
        print(s)

    def init_sloth(self):
        """Initialising sloth."""
        if len(self.sessions) == 0:
            try:
                self.sessions = self.dump.get_dump_data("sessions")
                self.current_session = self.sessions[0]
            except KeyError as e:
                print(f"Not found the saving: {e}")
                return None

        # because when you changed a session index was from a
        # previous session. It's update indexes
        self.dict_find_word = ""
        self.text_find_word = ""

        self.default_dict = {}

        # getting session
        try:
            self.default_dict = self.dump.get_dump_data(self.current_session)
        except KeyError as e:
            print(f"Not found the saving: {e}")
            return None

        # initializing lst_savings by existing sessions
        try:
            # first of all you clear savings
            self.lst_savings.delete(0, tk.END)
            # inserting from a first index
            for x in range(len(self.sessions)):
                self.lst_savings.insert(x, self.sessions[x])
        except KeyError as e:
            self.lst_savings.delete(0, tk.END)
            print("Not exists: %s" % e)

        # initializing text
        try:
            self.path_text = self.default_dict["text"]
            # we opened that file
            with open(self.path_text, "r", encoding="utf-8") as file:
                # cleared the area
                self.txt_text.delete("1.0", tk.END)
                # insert the data
                self.txt_text.insert(tk.END, file.read())
                # I need to know if a text file is opened
                self.opened_text = True
        except KeyError as e:
            # KeyError it's about a dict {}
            # if some error is occured it's not opened
            self.opened_text = False
            print("Not exists: %s" % e)
        except IOError as e:
            # IOError if something wrong with opening a file
            self.opened_text = False
            self.txt_text.delete("1.0", tk.END)
            print("Not found a TEXT file: %s" % e)
        except:
            # any error
            self.opened_text = False
            print("Unknown error.")

        # initializing dictionary
        try:
            # the same situation like in a previous block of a code
            self.path_dict = self.default_dict["dict"]
            with open(self.path_dict, "r", encoding="utf-8") as file:
                self.txt_dict.delete("1.0", tk.END)
                self.txt_dict.insert(tk.END, file.read())
                self.opened_dict = True
        except KeyError as e:
            self.opened_dict = False
            print("Not exists: %s" % e)
        except IOError as e:
            self.opened_dict = False
            self.txt_dict.delete("1.0", tk.END)
            print("Not found a DICT file: %s" % e)
        except:
            self.opened_dict = False
            print("Unknown error.")

        # getting dicts
        try:
            self.dicts = self.default_dict["dicts"]
            # cleared the area
            self.lst_dicts.delete(0, tk.END)
            for x in range(len(self.dicts)):
                # it's because you can add any dict in any location
                # but in dicts you're saving not a name, but an address
                # to a dict. Exception is "buf.txt" if you create it 
                # by yourself
                if self.dicts[x] == "buf.txt":
                    self.lst_dicts.insert(x, self.dicts[x])
                else:
                    name = self.dicts[x]
                    # it's searching backwards a first slash and we take
                    # a string from the last slash to the end. That's a
                    # name of the file in a path
                    name = name[-name[::-1].find('/') :]
                    self.lst_dicts.insert(x, name)
        except KeyError as e:
            self.lst_dicts.delete(0, tk.END)
            print("Not exists: %s" % e)
        except:
            self.lst_dicts.delete(0, tk.END)
            print("Unknown error.")

        # getting new words
        try:
            # first you need to clear data if it's changing a session...
            self.lst_new_words.delete(0, tk.END)

            if self.opened_text:
                buffer = []
                # we're adding a dict if it's opened to the list of dicts
                # or using it like a major dict if we aren't added some
                if self.opened_dict:
                    buffer.append(self.path_dict)
                if len(self.dicts) != 0:
                    buffer.extend(self.dicts)
                # if dict's list is not empty we're adding new words
                if len(buffer) != 0:
                    self.new_words = Finder(buffer,
                        self.path_text).get_new_words()
                    # clearing the area
                    self.lst_new_words.delete(0, tk.END)
                    # showed new words
                    for x in range(len(self.new_words)):
                        self.lst_new_words.insert(x, self.new_words[x])
        except KeyError as e:
            self.lst_new_words.delete(0, tk.END)
            print("Not esists: %s" % e)
        except:
            self.lst_new_words.delete(0, tk.END)
            print("Something went wrong!")

        # getting a dict find word
        try:
            self.dict_find_word = self.default_dict["dict_find_word"]
            self.ent_dict_word.delete(0, tk.END)
            self.ent_dict_word.insert(tk.END, self.dict_find_word)
        except KeyError as e:
            self.ent_dict_word.delete(0, tk.END)
            print("Not exists: %s" % e)

        # getting pref
        try:
            self.pref = self.default_dict["pref"]
            self.ent_pref.delete(0, tk.END)
            self.ent_pref.insert(tk.END, self.pref)
        except KeyError as e:
            self.ent_pref.delete(0, tk.END)
            print("Not exists: %s" % e)

        # getting word
        try:
            self.word = self.default_dict["word"]
            self.ent_word.delete(0, tk.END)
            self.ent_word.insert(tk.END, self.word)
        except KeyError as e:
            self.ent_word.delete(0, tk.END)
            print("Not exists: %s" % e)

        # getting transcription
        try:
            self.transc = self.default_dict["transc"]
            self.ent_transc.delete(0, tk.END)
            self.ent_transc.insert(tk.END, self.transc)
        except KeyError as e:
            self.ent_transc.delete(0, tk.END)
            print("Not exists: %s" % e)

        # getting translation
        try:
            self.transl = self.default_dict["transl"]
            self.ent_transl.delete(0, tk.END)
            self.ent_transl.insert(tk.END, self.transl)
        except KeyError as e:
            self.ent_transl.delete(0, tk.END)
            print("Not exists: %s" % e)

    
    def merge_dicts(self):
        """Merge all dicts that was opened. Except a current dict
        that was opened in a window."""
        buffer = {}
        # getting all words from dicts that was added in a buffer
        for x in self.dicts:
            for y in Dictionary(x).get_dictionary():
                buffer[y] = None
        # open or create buf.txt and adding words from that dict
        with open("buf.txt", "w", encoding="utf-8") as file:
            file.write("\n".join(buffer.keys()))
        # reinitializing dicts with only this buf.txt file with new words
        self.dicts = ["buf.txt"]
        self.lst_dicts.delete(0, tk.END)
        self.lst_dicts.insert(0, self.dicts[0])
        # saving a session with a new data
        self.save_session()

    def add_to_buf(self):
        """Adding (to "buf.txt" file) words that you know."""
        # new words that will be added
        buffer_line = ""
        # if the file exist then we take all text from that file
        # to buffer_line
        try:
            with open("buf.txt", "r", encoding="utf-8") as file:
                buffer_line = file.read()
                buffer_line += '\n'
        except IOError as e:
            print(e)
        # if doesn't exist then we create one
        with open("buf.txt", "w", encoding="utf-8") as file:
            # we're getting a tuple of indexes of the highlighted words
            indexes = self.lst_new_words.curselection()
            buffer = []
            # we starts backwards because after deleting from the
            # beginning it shifts to the beginning and indexes is anymore
            # actual
            for x in indexes[::-1]:
                buffer.append(self.lst_new_words.get(x))
                self.lst_new_words.delete(x)
            # adding all words with \n character
            buffer_line += "\n".join(buffer)
            file.write(buffer_line)

        # if buf.txt is not existing in dicts then we're adding it
        # and in lst_dicts also
        try:
            self.dicts.index("buf.txt")
        except ValueError as e:
            self.dicts.append("buf.txt")
            self.lst_dicts.insert(tk.END, "buf.txt")
            # saving changes to a current session
            self.save_session()

    def delete_dict(self):
        """Delete an added dict earlier."""
        # getting a highlighted dict and delete it from dicts
        index = self.lst_dicts.curselection()[0]
        self.dicts.pop(index)

        self.lst_dicts.delete(0, tk.END)
        for x in range(len(self.dicts)):
            name = self.dicts[x]
            # it's searching backwards a first slash and we take
            # a string from the last slash to the end. That's a
            # name of the file in a path
            name = name[-name[::-1].find('/') :]
            self.lst_dicts.insert(x, name)
        # saving changes
        self.save_session()

    def add_dict(self):
        """Adding a aditional dict"""
        filepath = askopenfilename(
            filetypes=[("Text file", "*.txt"), ("All files", "*.*")]
        )
        # if you wasn't choosing a file exiting from a function
        if not filepath:
            return None
        # we're searching from the end first a '/' match and
        # take beginning from the end of the filepath
        file_name = filepath[-filepath[::-1].find('/') :]
        self.dicts.append(filepath)
        self.lst_dicts.insert(tk.END, file_name)
        self.save_session()

    def clear_fields(self):
        """Clearing fields"""
        self.ent_pref.delete(0, tk.END)
        self.ent_word.delete(0, tk.END)
        self.ent_transc.delete(0, tk.END)
        self.ent_transl.delete(0, tk.END)
        self.ent_dict_word.delete(0, tk.END)
        self.lst_new_words.delete(0, tk.END)
        self.txt_dict.delete("1.0", tk.END)
        self.txt_text.delete("1.0", tk.END)
        self.lst_dicts.delete(0, tk.END)

        self.dicts = []
        self.path_text = ""
        self.path_dict = ""
        self.opened_text = False
        self.opened_dict = False
        self.new_words = []
        self.dict_find_word = ""
        self.word = ""
        self.transc = ""
        self.transl = ""

    def show_new_words(self):
        """Shows new words from checking the current open dict
        and text."""
        if self.opened_text:
            buffer = []
            if self.opened_dict:
                buffer.append(self.path_dict)
            if len(self.dicts) != 0:
                buffer.extend(self.dicts)
            if len(buffer) != 0:
                self.new_words = Finder(buffer,
                    self.path_text).get_new_words()
                self.lst_new_words.delete(0, tk.END)
                for x in range(len(self.new_words)):
                    self.lst_new_words.insert(x, self.new_words[x])

    def add_word(self):
        """Adding a word to the dictionary."""
        # getting a data from fields
        pref = self.ent_pref.get().strip(" ")
        word = self.ent_word.get().strip(" ")
        transc = self.ent_transc.get().strip(" ")
        transl = self.ent_transl.get().strip(" ")
        buffer = []

        # checking if a prefix is correct
        if f"{pref}:" in self.prefixes:
            # minimum a pref and a word you need to add 
            # a word
            if word == "":
                messagebox.showwarning("warning",
                    "You can't add words without a word!")
                return None
            elif transc == "" and transl == "":
                new_line = f"{pref}: {word};"
            elif transc == "":
                new_line = f"{pref}: {word} - {transl};"
            elif transl == "":
                new_line = f"{pref}: {word} [{transc}];"
            else:
                new_line = f"{pref}: {word} [{transc}] - {transl};"
        else:
            messagebox.showerror("Not a correct prefix",
                f"Correct prefixes: {', '.join(self.prefixes)}")
            return None

        # correct deleting of the added word
        try:
            idx_new_word = self.lst_new_words.curselection()[0]
            self.lst_new_words.delete(idx_new_word)
            self.new_words.pop(idx_new_word)
        except IndexError as e:
            print(e)
        except:
            print("Somethin wrong here: self.lst_new_words.curselection()[0]")

        # if txt_dict is empty than we create a new dict from 1 dict index
        if self.txt_dict.get("1.0", tk.END) != '\n':
            # the start and the end index of the last block of 200 words
            end_idx = self.txt_dict.search("[1-9]\n", index=tk.END,
                backwards=True, regexp=True)
            end_idx = end_idx.split(".")[0] + '.' + str(
                int(end_idx.split(".")[1]) + 1)
            start_idx = end_idx.split(".")[0] + ".0"

            # a number of the current 200 words block
            dict_idx = int(self.txt_dict.get(start_idx, end_idx))

            # to get words from that 200 words block and add a new word
            for line in self.txt_dict.get(start_idx, tk.END).split('\n'):
                if line.find(":") != -1 and line.find(";") != -1:
                    buffer.append(line.strip())
            buffer.append(new_line)
        
            # shuffles words by a chosen order
            buffer = self.create_d.shuffle_by_25_words(buffer)
            # and create a dict
            buffer = self.create_d.set_dict(dict_idx, buffer)

            # delete a previous 200 words
            self.txt_dict.delete(start_idx, tk.END)

            # if a start index is 1.0 then without a '\n'
            if start_idx == "1.0":
                new_line = "".join(buffer)
            else:
                new_line = '\n' + "".join(buffer)

            # inseting in the end and focusing on the end
            self.txt_dict.insert(tk.END, new_line)
            self.txt_dict.see(tk.END)
        else:
            # setting a new dict from a first index
            buffer = self.create_d.set_dict(1, [new_line])
            new_line = "".join(buffer)
            self.txt_dict.insert(tk.END, new_line)

    def delete_session(self):
        """Deleting a highlighted session."""
        # deleting a highlighted session from sessions and a session
        # in a dump
        self.dump.delete(self.sessions[self.current_session_index])
        self.sessions.pop(self.current_session_index)
        if len(self.sessions) > 0:
            # resaving a session
            self.dump.save_data(self.sessions, "sessions")
        else:
            # if sessions is 0 size. We delete sessions and clear all fields
            self.dump.delete("sessions")
            self.clear_fields()

        # refill lst savings with a new data
        self.lst_savings.delete(0, tk.END)
        for x in range(len(self.sessions)):
            self.lst_savings.insert(x, self.sessions[x])

    def select_savings(self, event):
        """For jumping from a session to a session"""
        # it's for a session_up function to know what index to delete
        self.current_session_index = self.lst_savings.curselection()[0]

        session = self.lst_savings.get(self.current_session_index)
        self.current_session = session
        self.init_sloth()
    
    def get_current_data(self):
        """Getting current data and returns a dict with the data."""
        current_data = {}

        current_data["dicts"] = self.dicts
        current_data["text"] = self.path_text
        current_data["dict"] = self.path_dict
        current_data["opened_text"] = self.opened_text
        current_data["opened_dict"] = self.opened_dict
        current_data["new_words"] = self.new_words
        current_data["dict_find_word"] = self.ent_dict_word.get()
        current_data["pref"] = self.ent_pref.get()
        current_data["word"] = self.ent_word.get()
        current_data["transc"] = self.ent_transc.get()
        current_data["transl"] = self.ent_transl.get()

        return current_data
   
    def save_session(self):
        """Saving a new session or resaving a current session."""
        # getting the last index of the session in lst_savings
        index = self.lst_savings.index(tk.END)
        session = self.ent_savings.get()
        # clearing of the entry field
        self.ent_savings.delete(0, tk.END)

        # save new data in dict
        filepath = self.dump.get_dump_data(self.current_session)["dict"]
        
        # because after clearing data in current session address to "dict"
        # is not existing. And we're checking if it's existing.
        if filepath != '':
            # saving the data to the dictionary
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(self.txt_dict.get("1.0", tk.END).strip())
        
        # if we added data to the dictionary but a dictionary was not
        # opened. We'll create "dictionary.txt"
        if filepath == '' and self.txt_dict.get("1.0", tk.END) != '\n':
            self.path_dict = 'dictionary.txt'
            with open('dictionary.txt', 'w', encoding='utf-8') as file:
                file.write(self.txt_dict.get("1.0", tk.END).strip())    

        # actually saving a session to the dump or resaving if it's
        # existing now
        if session == '':
            self.dump.save_data(self.get_current_data(),
                self.current_session)
            self.session_up()
        else:
            self.current_session = session
            self.lst_savings.insert(index, session)
            self.current_session_index = index
            self.sessions.append(session)
            self.dump.save_data(self.get_current_data(),
                self.current_session)
            self.session_up()


    def session_up(self):
        """It's up a session in lst_savings after saving"""
        # to delete an item from current place and insert into the beginning
        item = self.sessions.pop(self.current_session_index)
        self.sessions.insert(0, item)
        # resaving sessions because an order was changed
        self.dump.save_data(self.sessions, "sessions")
        # clearing and showind sessions in the right order
        self.lst_savings.delete(0, tk.END)
        for x in range(len(self.sessions)):
            self.lst_savings.insert(x, self.sessions[x])

    def open_text(self):
        """Opens a file with a new text."""
        self.text_find_word = ""

        filepath = askopenfilename(
            filetypes=[("Text file", "*.txt"), ("All files", "*.*")]
        )
        if not filepath:
            return None
        # if the file is opened 
        self.opened_text = True
        self.path_text = filepath

        self.txt_text.delete("1.0", tk.END)
        with open(filepath, "r", encoding="utf-8") as file:
            text = file.read()
            self.txt_text.insert(tk.END, text)      

    def open_dict(self):
        """Opens a dictionary for adding new words."""
        self.dict_find_word = ""
        filepath = askopenfilename(
            filetypes=[("Text file", "*.txt"), ("All files", "*.*")]
        )
        if not filepath:
            return None
        self.opened_dict = True
        self.path_dict = filepath

        self.txt_dict.delete("1.0", tk.END)
        with open(filepath, "r", encoding="utf-8") as file:
            text = file.read()
            self.txt_dict.insert(tk.END, text)

    def selected_word(self, event):
        """Works when you selected a word in lst_new_words."""
        index = self.lst_new_words.curselection()[0]
        word = self.lst_new_words.get(index)

        # updating an information only when you selected another word
        if self.text_find_word != word:
            self.ent_word.delete(0, tk.END)
            self.ent_dict_word.delete(0, tk.END)
            self.ent_word.insert(tk.END, word)
            self.ent_dict_word.insert(tk.END, word)
            self.ent_transc.delete(0, tk.END)
            self.ent_transl.delete(0, tk.END)
            self.ent_pref.delete(0, tk.END)
        
        self.text_find_txt(word)

    def text_find_txt(self, word):
        """It's finding only whole words in the text.
        """
        # we need to zero indexes, next index and add a new
        # finding word
        if self.text_find_word != word:
            self.text_find_word = word
            self.text_word_indexes = []
            self.text_next_index = 0
            # to delete a previous tags
            self.txt_text.tag_remove('found', '1.0', tk.END)
            
            if word:
                idx = '1.0'
                while 1:
                    # found a first index of the found word in text
                    idx = self.txt_text.search(word, idx, nocase=1,
                                    stopindex=tk.END)

                    # if not found a word
                    if not idx: break

                    lastidx = '%s+%dc' % (idx, len(word))

                    # index of the word in the line
                    string_idx = int(idx[idx.find(".")+1 :])
        
                    if string_idx > 0:
                        # we are shifting on one character back
                        # to check if it is a whole word
                        buf_idx = idx[:idx.find(".")] + "." + str(
                            string_idx - 1)

                        # plus 2 because our first index on one symbol
                        # greater of the word
                        buf_lastidx = '%s+%dc' % (buf_idx, (len(word)+2))
                        
                        # found word with with two additional charachters
                        # one at the beginning and one at the end
                        buf_word = self.txt_text.get(buf_idx, buf_lastidx)
                        buf_word = buf_word.strip(
                            "!@#$%^&*()_+=-`~;:\|'\",./<>? \n"
                        )
                        if buf_word.casefold() == word:
                            self.text_word_indexes.append(idx)
                            self.txt_text.tag_add('found', idx, lastidx)
                    else:
                        # adding only one charachter to the end
                        # because first index is 0
                        buf_lastidx = '%s+%dc' % (idx, (len(word)+1))
                        buf_word = word.strip(
                            "!@#$%^&*()_+=-`~;:\|'\",./<>? \n")
                        if buf_word.casefold() == word:
                            self.text_word_indexes.append(idx)
                            self.txt_text.tag_add('found', idx, lastidx)

                    # idx equals lastidx because we need to find a next
                    # word from the end index of the first one
                    idx = lastidx
                # turning found words in red colour for highlighting
                self.txt_text.tag_config('found', foreground='red')

        # shifting in the found words by changing view in the text
        # widget
        i = self.text_next_index
        size = len(self.text_word_indexes)
        if size > i:
            self.text_next_index += 1
            self.txt_text.see(self.text_word_indexes[i])
        elif i == size and size != 0:
            # we're comming back to the first found word
            self.text_next_index = 1
            self.txt_text.see(self.text_word_indexes[0])

    def dict_find_txt(self):
        """It's finding all character set matches"""
        word = self.ent_dict_word.get()

        if self.dict_find_word != word:
            self.dict_find_word = word
            self.dict_word_indexes = []
            self.dict_next_index = 0

            self.txt_dict.tag_remove('dict', '1.0', tk.END)
            
            if word:
                idx = '1.0'
                while 1:
                    idx = self.txt_dict.search(word, idx, nocase=1,
                                    stopindex=tk.END)
                    if not idx: break
                    lastidx = '%s+%dc' % (idx, len(word))

                    self.txt_dict.tag_add('dict', idx, lastidx)
                    self.dict_word_indexes.append(idx)

                    idx = lastidx
                self.txt_dict.tag_config('dict', foreground='red')

        i = self.dict_next_index
        size = len(self.dict_word_indexes)
        if size > i:
            self.dict_next_index += 1
            self.txt_dict.see(self.dict_word_indexes[i])
        elif i >= size and size != 0:
            self.dict_next_index = 1
            self.txt_dict.see(self.dict_word_indexes[0])
