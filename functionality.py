import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox
from dumper import Dumper
from create_dict import CreateDict
from finder import Finder
from dictionary import Dictionary
from windows import Window

class Functionality(Window):
    def __init__(self, dump, create_d):
        Window.__init__(self)

        self.prefixes = ["n:", "v:", "vv:", "adj:", "adv:", "pre:",
            "con:", "pro:", "exc:", "int:", "pref:", "s:"]

        # for finding in text every whole word
        self.text_word_indexes = []
        self.text_next_index = 0
        self.text_find_word = ""

        # for finding in text every whole word
        self.dict_word_indexes = []
        self.dict_next_index = 0
        self.dict_find_word = ""

        # dumper
        self.dump = dump
        self.create_d = create_d
        # dump.clear_dump()

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

        self.init_sloth()

        self.start()

    def help(self):
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
            self.lst_savings.delete(0, tk.END)
            for x in range(len(self.sessions)):
                self.lst_savings.insert(x, self.sessions[x])
        except KeyError as e:
            print("Not exists: %s" % e)

        # initializing text
        try:
            self.path_text = self.default_dict["text"]
            # IT'S NOT A COPY
            with open(self.path_text, "r", encoding="utf-8") as file:
                self.txt_text.delete("1.0", tk.END)
                self.txt_text.insert(tk.END, file.read())
                self.opened_text = True
        except KeyError as e:
            self.opened_text = False
            print("Not exists: %s" % e)
        except IOError as e:
            self.opened_text = False
            self.txt_text.delete("1.0", tk.END)
            print("Not found a TEXT file: %s" % e)
        except:
            self.opened_text = False
            print("Unknown error.")

        # initializing dictionary
        try:
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
            self.lst_dicts.delete(0, tk.END)
            for x in range(len(self.dicts)):
                if self.dicts[x] == "buf.txt":
                    self.lst_dicts.insert(x, self.dicts[x])
                else:
                    name = self.dicts[x]
                    name = name[-name[::-1].find('/') :]
                    self.lst_dicts.insert(x, name)
        except KeyError as e:
            self.lst_dicts.delete(0, tk.END)
            print("Not exists: %s" % e)
        except:
            print("Unknown error.")

        # getting new words
        try:
            # first you need to clear data if it's changing a session...
            self.lst_new_words.delete(0, tk.END)

            if self.opened_text:
                buffer = []
                if self.opened_dict:
                    buffer.append(self.path_dict)
                if len(self.dicts) != 0:
                    buffer.extend(self.dicts)
                if len(buffer) != 0:
                    f = Finder(buffer, self.path_text)
                    self.new_words = f.get_new_words()
                    self.lst_new_words.delete(0, tk.END)
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
        buffer = {}
        for x in self.dicts:
            for y in Dictionary(x).get_dictionary():
                buffer[y] = None
        with open("buf.txt", "w", encoding="utf-8") as file:
            file.write("\n".join(buffer.keys()))
        self.dicts = ["buf.txt"]
        self.lst_dicts.delete(0, tk.END)
        self.lst_dicts.insert(0, self.dicts[0])
        self.save_session()

    def add_to_buf(self):
        line = ""
        try:
            with open("buf.txt", "r", encoding="utf-8") as file:
                line = file.read()
                line += '\n'
        except IOError as e:
            print(e)
        with open("buf.txt", "w", encoding="utf-8") as file:
            indexes = self.lst_new_words.curselection()
            buffer = []
            for x in indexes[::-1]:
                buffer.append(self.lst_new_words.get(x))
                self.lst_new_words.delete(x)
            line += "\n".join(buffer)
            file.write(line)

        try:
            self.dicts.index("buf.txt")
        except ValueError as e:
            self.dicts.append("buf.txt")
            self.lst_dicts.insert(tk.END, "buf.txt")
            self.save_session()

    def delete_dict(self):
        index = self.lst_dicts.curselection()[0]
        self.dicts.pop(index)

        self.lst_dicts.delete(0, tk.END)
        for x in range(len(self.dicts)):
            name = self.dicts[x]
            name = name[-name[::-1].find('/') :]
            self.lst_dicts.insert(x, name)
        self.save_session()

    def add_dict(self):
        filepath = askopenfilename(
            filetypes=[("Text file", "*.txt"), ("All files", "*.*")]
        )
        if not filepath:
            return None
        # we're searching from the end first a '/' match and
        # take beginning from the end of the filepath
        file_name = filepath[-filepath[::-1].find('/') :]
        self.dicts.append(filepath)
        self.lst_dicts.insert(tk.END, file_name)
        self.save_session()

    def clear_fields(self):
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
                f = Finder(buffer, self.path_text)
                self.new_words = f.get_new_words()
                self.lst_new_words.delete(0, tk.END)
                for x in range(len(self.new_words)):
                    self.lst_new_words.insert(x, self.new_words[x])

    def add_word(self):
        pref = self.ent_pref.get().strip(" ")
        word = self.ent_word.get().strip(" ")
        transc = self.ent_transc.get().strip(" ")
        transl = self.ent_transl.get().strip(" ")
        buffer = []

        if f"{pref}:" in self.prefixes:
            if transc == "" and transl == "":
                new_line = f"{pref}: {word};"
            elif transc == "":
                new_line = f"{pref}: {word} - {transl};"
            elif transl == "":
                new_line = f"{pref}: {word} [{transc}];"
            elif pref == "" or word == "":
                messagebox.showwarning("warning",
                    "You can't add words without a prefix or a word!")
                return None
            else:
                new_line = f"{pref}: {word} [{transc}] - {transl};"
        else:
            messagebox.showerror("Not a correct prefix",
                f"Correct prefixes: {', '.join(self.prefixes)}")
            return None

        # correct deleting of the added word
        idx_new_word = self.lst_new_words.curselection()[0]
        self.lst_new_words.delete(idx_new_word)
        self.new_words.pop(idx_new_word)

        # the start and the end index of the last block of 200 words
        end_idx = self.txt_dict.search("[1-9]\n", index=tk.END, backwards=True,
            regexp=True)
        end_idx = end_idx.split(".")[0] + '.' + str(int(end_idx.split(".")[1]) + 1)
        start_idx = end_idx.split(".")[0] + ".0"
        
        # a number of the current 200 words block
        dict_idx = int(self.txt_dict.get(start_idx, end_idx))

        # to get words from that 200 words block and add a new word
        for line in self.txt_dict.get(start_idx, tk.END).split('\n'):
            if line.find(":") != -1 and line.find(";") != -1:
                buffer.append(line.strip())
        buffer.append(new_line)

        buffer = self.create_d.shuffle_by_25_words(buffer)
        buffer = self.create_d.set_dict(dict_idx, buffer)

        self.txt_dict.delete(start_idx, tk.END)

        new_line = '\n' + "".join(buffer)
        self.txt_dict.insert(tk.END, new_line)
        self.txt_dict.see(tk.END)

    def delete_session(self):
        self.dump.delete(self.sessions[self.current_session_index])
        self.sessions.pop(self.current_session_index)
        if len(self.sessions) > 0:
            self.dump.save_data(self.sessions, "sessions")
        else:
            self.dump.delete("sessions")
            self.clear_fields()

        self.lst_savings.delete(0, tk.END)
        for x in range(len(self.sessions)):
            self.lst_savings.insert(x, self.sessions[x])

    def select_savings(self, event):
        self.current_session_index = self.lst_savings.curselection()[0]

        session = self.lst_savings.get(self.current_session_index)
        self.current_session = session
        self.init_sloth()
    
    def get_current_data(self):
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
        index = self.lst_savings.index(tk.END)
        session = self.ent_savings.get()
        self.ent_savings.delete(0, tk.END)

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

        # save new data in dict
        filepath = self.dump.get_dump_data(self.current_session)["dict"]
        
        # because after clearing data in current session address to "dict"
        # is not existing. And we're checking if it's existing.
        if filepath != '':
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(self.txt_dict.get("1.0", tk.END).strip())

    def session_up(self):
        l = [x for x in range(self.lst_savings.size())]
        item = self.sessions.pop(self.current_session_index)
        self.sessions.insert(0, item)
        self.dump.save_data(self.sessions, "sessions")
        self.lst_savings.delete(0, tk.END)
        for x in range(len(self.sessions)):
            self.lst_savings.insert(x, self.sessions[x])

    def open_text(self):
        self.text_find_word = ""

        filepath = askopenfilename(
            filetypes=[("Text file", "*.txt"), ("All files", "*.*")]
        )
        if not filepath:
            return None
        self.opened_text = True
        self.path_text = filepath

        self.txt_text.delete("1.0", tk.END)
        with open(filepath, "r", encoding="utf-8") as file:
            text = file.read()
            self.txt_text.insert(tk.END, text)      

    def open_dict(self):
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
        index = self.lst_new_words.curselection()[0]
        word = self.lst_new_words.get(index)

        if self.text_find_word != word:
            self.ent_word.delete(0, tk.END)
            self.ent_dict_word.delete(0, tk.END)
            self.ent_word.insert(tk.END, word)
            self.ent_dict_word.insert(tk.END, word)
            self.ent_transc.delete(0, tk.END)
            self.ent_transl.delete(0, tk.END)
            self.ent_pref.delete(0, tk.END)
        
        self.text_find_txt(word)

    def open_file(self):
        self.text_find_word = ""
        self.dict_find_word = ""

        filepath = askopenfilename(
            filetypes=[("Text file", "*.txt"), ("All files", "*.*")]
        )
        if not filepath:
            return None
        self.txt_text.delete("1.0", tk.END)
        with open(filepath, "r", encoding="utf-8") as file:
            text = file.read()
            self.txt_text.insert(tk.END, text)
            self.window.title(f"simple text editor - {filepath}")

    def save_file(self):
        filepath = asksaveasfilename(
            filetypes=[("Text file", "*.txt"), ("All files", "*.*")]
        )
        if not filepath:
            return None
        with open(filepath, "w", encoding="utf-8") as file:
            text = self.txt_text.get("1.0", tk.END)
            file.write(text)

    def text_find_txt(self, word):
        """It's finding only whole words in the text.
        """
        # we need to zero indexes, next index and add a new
        # finding word
        if self.text_find_word != word:
            self.text_find_word = word
            self.text_word_indexes = []
            self.text_next_index = 0
            self.txt_text.tag_remove('found', '1.0', tk.END)
            # to delete a previous tags
            
            if word:
                idx = '1.0'
                while 1:
                    idx = self.txt_text.search(word, idx, nocase=1,
                                    stopindex=tk.END)
                    # found a first index of the found word in text

                    # if not found a word
                    if not idx: break

                    lastidx = '%s+%dc' % (idx, len(word))

                    string_idx = int(idx[idx.find(".")+1 :])
                    # index of the word in the line
        
                    if string_idx > 0:
                        buf_idx = idx[:idx.find(".")] + "." + str(
                            string_idx - 1)
                        # we are shifting on one character back
                        # to check if it is a whole word
                        buf_lastidx = '%s+%dc' % (buf_idx, (len(word)+2))
                        # plus 2 because our first index on one symbol
                        # greater of the word
                        buf_word = self.txt_text.get(buf_idx, buf_lastidx)
                        # found word with with two additional charachters
                        # one at the beginning and one at the end
                        buf_word = buf_word.strip(
                            "!@#$%^&*()_+=-`~;:\|'\",./<>? \n"
                        )
                        if buf_word.casefold() == word:
                            self.text_word_indexes.append(idx)
                            self.txt_text.tag_add('found', idx, lastidx)
                    else:
                        buf_lastidx = '%s+%dc' % (idx, (len(word)+1))
                        # adding only one charachter to the end
                        # because first index is 0
                        buf_word = word.strip(
                            "!@#$%^&*()_+=-`~;:\|'\",./<>? \n")
                        if buf_word.casefold() == word:
                            self.text_word_indexes.append(idx)
                            self.txt_text.tag_add('found', idx, lastidx)

                    idx = lastidx
                    # idx equals lastidx because we need to find a next
                    # word from the end index of the first one
                self.txt_text.tag_config('found', foreground='red')
                # turning found words in red colour for highlighting

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

d = Dumper("dump.pickle")
c_d = CreateDict()

w = Functionality(d, c_d)
