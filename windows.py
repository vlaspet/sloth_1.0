import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from dumper import Dumper
from create_dict import CreateDict
import copy

class Window:
    def __init__(self, dump, create_d):
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
        self.current_session = "default"
        self.path_text = ""
        self.path_dict = ""
        self.path_new_words = ""
        self.dict_find_word = ""
        self.word = ""
        self.transc = ""
        self.transl = ""

        self.current_index = 0

        self.working_area()

        try:
            self.sessions = self.dump.get_dump_data("sessions")
            self.current_session = self.sessions[0]
        except KeyError as e:
            print(f"Not found the saving: {e}")

        try:
            self.init_sloth(self.dump.get_dump_data(self.current_session))
        except KeyError as e:
            print(f"Not found the saving: {e}")
        self.window.mainloop()

    def help(self):
        print("Names for every part of the window!")
        s = """
        sessions - a key for a list of savings names. It's
        saving as a independent part of dump.
        text - a path for a text.
        dict - a path for a dictionary.
        new_words - a path for new words.
        dict_find_word - a word for finding in dict.
        pref - a prefix of the word.
        word - a new word for a saving in the dictionary.
        transc - a transcription word for the word.
        transl - a translation word for the word.
        """
        print(s)

    def init_sloth(self, init_dict):
        # because when you changed a session index was from a
        # previous session. It's update indexes
        self.dict_find_word = ""
        self.text_find_word = ""

        self.default_dict = {}

        # getting "default" savings if not exists then creating
        try:
            self.default_dict = init_dict
        except KeyError as e:
            print("Not exists: %s" % e)
            # self.sessions = ["default"]

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
        except KeyError as e:
            print("Not exists: %s" % e)
        except IOError as e:
            self.txt_text.delete("1.0", tk.END)
            print("Not found a TEXT file: %s" % e)
        except:
            print("Unknown error.")

        # initializing dictionary
        try:
            self.path_dict = self.default_dict["dict"]
            with open(self.path_dict, "r", encoding="utf-8") as file:
                self.txt_dict.delete("1.0", tk.END)
                self.txt_dict.insert(tk.END, file.read())
        except KeyError as e:
            print("Not exists: %s" % e)
        except IOError as e:
            self.txt_dict.delete("1.0", tk.END)
            print("Not found a DICT file: %s" % e)
        except:
            print("Unknown error.")

        # initializing new words
        try:
            self.path_new_words = self.default_dict["new_words"]
            # IT'S NOT A COPY
            with open(self.path_new_words, "r", encoding="utf-8") as file:
                self.lst_new_words.delete(0, tk.END)
                self.lst_new_words.insert(tk.END, file.read())
        except KeyError as e:
            print("Not exists: %s" % e)
        except IOError as e:
            # self.lst_new_words.delete(0, tk.END)
            print("Not found a NEW WORDS file: %s" % e)
        except:
            print("Unknown error.")

        # getting dict word
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

    def working_area(self):
        self.window = tk.Tk()

        self.window.title("Simple text editor")
        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)

        self.frm_window = tk.Frame(self.window, relief=tk.RAISED, bd=1)
        self.frm_window.rowconfigure(0, weight=1)
        self.frm_window.columnconfigure(0, weight=1)
        self.frm_window.grid(row=0, column=0, sticky="nswe")

        self.frm_blocks = tk.Frame(self.frm_window, relief=tk.RAISED, bd=1)
        self.frm_blocks.rowconfigure([0], weight=1)
        self.frm_blocks.columnconfigure([0], weight=1)
        self.frm_blocks.grid(row=0, column=0, sticky="nswe")

        self.frm_new_words = tk.Frame(self.frm_blocks, relief=tk.RAISED, bd=1)
        self.frm_new_words.rowconfigure([1], weight=1)
        self.frm_new_words.grid(row=0, column=1, sticky="wens")

        self.frm_case = tk.Frame(self.frm_blocks, relief=tk.RAISED, bd=1)
        self.frm_case.rowconfigure(0, weight=1)
        self.frm_case.columnconfigure(0, weight=1)
        self.frm_case.grid(row=0, column=0, sticky="nswe")

        self.frm_words = tk.Frame(self.frm_case, relief=tk.RAISED, bd=1)
        self.frm_words.rowconfigure([0], weight=1)
        self.frm_words.columnconfigure([0, 1, 2], weight=1)
        self.frm_words.grid(row=1, column=0, sticky="nswe")

        self.frm_dict = tk.Frame(self.frm_case, relief=tk.RAISED, bd=1)
        self.frm_dict.rowconfigure(1, weight=1)
        self.frm_dict.columnconfigure(0, weight=1)
        self.frm_dict.grid(row=0, column=0, sticky="nse")

        self.frm_navig = tk.Frame(self.frm_case, relief=tk.RAISED, bd=0)
        self.frm_navig.rowconfigure(1, weight=1)
        self.frm_navig.columnconfigure(0, weight=1)
        self.frm_navig.grid(row=0, column=0, sticky="nw")

        # New text
        self.txt_text = tk.Text(self.frm_window, width=140, height=5)
        self.txt_text.grid(row=2, column=0, sticky="sew")

        # showing new words from text
        self.lbl_new_words = tk.Label(self.frm_new_words, text="New words")
        self.lbl_new_words.grid(row=0, column=0,
            sticky="wens")

        self.lst_new_words = tk.Listbox(self.frm_new_words, width=20, height=20)
        self.lst_new_words.grid(row=1, column=0, sticky="ns")
        self.lst_new_words.insert(0, "tool")
        self.lst_new_words.bind("<<ListboxSelect>>", self.lst_selected_word)

        self.scr_text = tk.Scrollbar(self.frm_new_words, orient='vertical',
            command=self.lst_new_words.yview)
        self.scr_text.grid(row=1, column=1, sticky="ns")
        self.lst_new_words["yscrollcommand"] = self.scr_text.set


        # The area of filling new words
        self.lbl_pref = tk.Label(self.frm_words, text="Prefix")
        self.lbl_word = tk.Label(self.frm_words, text="Word")
        self.lbl_transc = tk.Label(self.frm_words, text="Transcription")
        self.lbl_transl = tk.Label(self.frm_words, text="Translation")

        self.lbl_pref.grid(row=0, column=0,  sticky="n", padx=10)
        self.lbl_word.grid(row=0, column=1,  sticky="n", padx=10)
        self.lbl_transc.grid(row=0, column=2, sticky="n", padx=10)
        self.lbl_transl.grid(row=0, column=3, sticky="n", padx=10)

        self.ent_pref = tk.Entry(self.frm_words, width=5)
        self.ent_word = tk.Entry(self.frm_words, width=15)
        self.ent_transc = tk.Entry(self.frm_words, width=20)
        self.ent_transl = tk.Entry(self.frm_words, width=20)

        self.ent_pref.grid(row=1, column=0, sticky="n", padx=10)
        self.ent_word.grid(row=1, column=1, sticky="n", padx=10)
        self.ent_transc.grid(row=1, column=2, sticky="n", padx=10)
        self.ent_transl.grid(row=1, column=3, sticky="n", padx=10)

        self.btn_add_word = tk.Button(self.frm_words, text="Add word",
            command=self.add_word)
        self.btn_add_word.grid(row=2, column=0)

        # everything with dictionary
        self.lbl_dict = tk.Label(self.frm_dict, text="Dictionary",
            width=45)
        self.lbl_dict.grid(row=0, column=0, sticky="nse")

        self.txt_dict = tk.Text(self.frm_dict, width=60, height=40)
        self.txt_dict.grid(row=1, column=0, sticky="nse")

        self.btn_find_dict = tk.Button(self.frm_dict, text="Find",
            command=self.dict_find_txt)
        self.btn_find_dict.grid(row=3, column=0, sticky="wens")

        self.ent_dict_word = tk.Entry(self.frm_dict, width=15)
        self.ent_dict_word.grid(row=2, column=0, sticky="nswe", padx=10)

        #navigation
        self.lbl_savings = tk.Label(self.frm_navig, text="Navigation")
        self.lbl_savings.grid(row=0, column=0, sticky="we")

        self.btn_open_text = tk.Button(self.frm_navig, text="Text",
            command=self.open_text)
        self.btn_open_text.grid(row=5, column=0, sticky="we")
        self.btn_open_text.rowconfigure(1, weight=0)

        self.btn_open_dict = tk.Button(self.frm_navig, text="Dict",
            command=self.open_dict)
        self.btn_open_dict.grid(row=6, column=0, sticky="we")

        self.btn_add_dict = tk.Button(self.frm_navig, text="Add Dict")
        self.btn_add_dict.grid(row=7, column=0, sticky="we")

        #savings
        self.lbl_savings = tk.Label(self.frm_navig, text="Savings")
        self.lbl_savings.grid(row=0, column=0, sticky="we")

        self.lst_savings = tk.Listbox(self.frm_navig, width=15, height=5)
        self.lst_savings.grid(row=1, column=0)
        self.lst_savings.bind("<<ListboxSelect>>", self.select_savings)

        self.ent_savings = tk.Entry(self.frm_navig, width=15)
        self.ent_savings.grid(row=3, column=0)

        self.btn_save = tk.Button(self.frm_navig, text="Delete",
            command=self.delete_session)
        self.btn_save.grid(row=2, column=0, sticky="we")

        self.btn_save = tk.Button(self.frm_navig, text="Save",
            command=self.save_session)
        self.btn_save.grid(row=4, column=0, sticky="we")

    def add_word(self):
        pref = self.ent_pref.get().strip(" ")
        word = self.ent_word.get().strip(" ")
        transc = self.ent_transc.get().strip(" ")
        transl = self.ent_transl.get().strip(" ")
        buffer = []
        new_line = f"{pref}: {word} [{transc}] - {transl};"

        end_idx = self.txt_dict.search("[1-9]\n", index=tk.END, backwards=True,
            regexp=True)
        end_idx = end_idx.split(".")[0] + '.' + str(int(end_idx.split(".")[1]) + 1)
        start_idx = end_idx.split(".")[0] + ".0"
        
        dict_idx = int(self.txt_dict.get(start_idx, end_idx))

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
        self.dump.delete(self.sessions[self.current_index])
        self.sessions.pop(self.current_index)
        if len(self.sessions) > 0:
            self.dump.save_data(self.sessions, "sessions")
        else:
            self.dump.delete("sessions")
        print(self.dump.get_dump())

        self.lst_savings.delete(0, tk.END)
        for x in range(len(self.sessions)):
            self.lst_savings.insert(x, self.sessions[x])

    def select_savings(self, event):
        self.current_index = self.lst_savings.curselection()[0]

        session = self.lst_savings.get(self.current_index)
        self.current_session = session
        self.init_sloth(self.dump.get_dump_data(session))
    
    def get_current_data(self):
        current_data = {}

        current_data["text"] = self.path_text
        current_data["dict"] = self.path_dict
        current_data["new_words"] = self.path_new_words
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
            self.dump.save_data(copy.deepcopy(self.get_current_data()),
                self.current_session)
            self.session_up()
        else:
            self.current_session = session
            self.lst_savings.insert(index, session)
            self.current_index = index
            self.sessions.append(session)
            self.dump.save_data(copy.deepcopy(self.get_current_data()),
                self.current_session)
            self.session_up()

        # save new data in dict
        filepath = self.dump.get_dump_data(self.current_session)["dict"]
        
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(self.txt_dict.get("1.0", tk.END).strip())

    def session_up(self):
        l = [x for x in range(self.lst_savings.size())]
        item = self.sessions.pop(self.current_index)
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
        self.path_dict = filepath

        self.txt_dict.delete("1.0", tk.END)
        with open(filepath, "r", encoding="utf-8") as file:
            text = file.read()
            self.txt_dict.insert(tk.END, text)

    def lst_selected_word(self, event):
        index = self.lst_new_words.curselection()[0]
        word = self.lst_new_words.get(index)
        self.ent_word.delete(0, tk.END)
        self.ent_dict_word.delete(0, tk.END)
        self.ent_word.insert(tk.END, word)
        self.ent_dict_word.insert(tk.END, word)
        
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
        if self.text_find_word != word:
            self.text_find_word = word
            self.text_word_indexes = []
            self.text_next_index = 0

            self.txt_text.tag_remove('found', '1.0', tk.END)
            
            if word:
                idx = '1.0'
                while 1:
                    idx = self.txt_text.search(word, idx, nocase=1,
                                    stopindex=tk.END)
                    if not idx: break
                    lastidx = '%s+%dc' % (idx, len(word))

                    string_idx = int(idx[idx.find(".")+1 :])
        
                    if string_idx > 0:
                        buf_idx = idx[:idx.find(".")] + "." + str(string_idx - 1)
                        buf_lastidx = '%s+%dc' % (buf_idx, (len(word)+2))
                        buf_word = self.txt_text.get(buf_idx, buf_lastidx)
                        buf_word = buf_word.strip(
                            "!@#$%^&*()_+=-`~;:\|'\",./<>? \n"
                        )
                        if buf_word == word:
                            self.text_word_indexes.append(idx)
                            self.txt_text.tag_add('found', idx, lastidx)
                    else:
                        buf_lastidx = '%s+%dc' % (buf_idx, (len(word)+1))
                        buf_word = word.strip("!@#$%^&*()_+=-`~;:\|'\",./<>? \n")
                        if buf_word == word:
                            self.text_word_indexes.append(idx)
                            self.txt_text.tag_add('found', idx, lastidx)

                    idx = lastidx
                self.txt_text.tag_config('found', foreground='red')

        i = self.text_next_index
        size = len(self.text_word_indexes)
        if size > i:
            self.text_next_index += 1
            self.txt_text.see(self.text_word_indexes[i])
        elif i >= size and size != 0:
            self.text_next_index = 1
            self.txt_text.see(self.text_word_indexes[0])

    def dict_find_txt(self):
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

w = Window(d, c_d)
