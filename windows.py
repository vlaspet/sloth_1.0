import tkinter as tk

class Window:
    def __init__(self):
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
        self.lbl_new_words.grid(row=0, column=0, sticky="wens")

        self.lst_new_words = tk.Listbox(self.frm_new_words, width=20,
            height=20, selectmode=tk.EXTENDED)
        self.lst_new_words.grid(row=1, column=0, sticky="ns")
        self.lst_new_words.bind("<<ListboxSelect>>", self.selected_word)

        self.btn_new_words = tk.Button(self.frm_new_words,
            text="Show new words", command=self.show_new_words)
        self.btn_new_words.grid(row=2, column=0, sticky="we")

        # words that you know but don't add to dictionary
        self.btn_new_words = tk.Button(self.frm_new_words,
            text="Add to buf.txt", command=self.add_to_buf)
        self.btn_new_words.grid(row=3, column=0, sticky="we")

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

        #dictionary
        self.lbl_dict = tk.Label(self.frm_dict, text="Dictionary",
            width=45)
        self.lbl_dict.grid(row=0, column=0, sticky="nse")

        self.txt_dict = tk.Text(self.frm_dict, width=60, height=40)
        self.txt_dict.grid(row=1, column=0, sticky="nse")

        self.ent_dict_word = tk.Entry(self.frm_dict, width=15)
        self.ent_dict_word.grid(row=2, column=0, sticky="nswe", padx=10)

        self.btn_find_dict = tk.Button(self.frm_dict, text="Find",
            command=self.dict_find_txt)
        self.btn_find_dict.grid(row=3, column=0, sticky="wens")

        #navigation
        self.lbl_savings = tk.Label(self.frm_navig, text="Navigation")
        self.lbl_savings.grid(row=5, column=0, sticky="we")

        self.btn_open_text = tk.Button(self.frm_navig, text="Text",
            command=self.open_text)
        self.btn_open_text.grid(row=6, column=0, sticky="we")
        self.btn_open_text.rowconfigure(1, weight=0)

        self.btn_open_dict = tk.Button(self.frm_navig, text="Dictionary",
            command=self.open_dict)
        self.btn_open_dict.grid(row=7, column=0, sticky="we")

        self.btn_clear_fields = tk.Button(self.frm_navig,
            text="Clear fields", command=self.clear_fields)
        self.btn_clear_fields.grid(row=8, column=0, sticky="we")

        self.btn_shuffle_dict = tk.Button(self.frm_navig,
            text="Shuffle dict", command=self.shuffle_dict)
        self.btn_shuffle_dict.grid(row=9, column=0, sticky="we")

        #savings
        self.lbl_savings = tk.Label(self.frm_navig, text="Savings")
        self.lbl_savings.grid(row=0, column=0, sticky="we")

        self.lst_savings = tk.Listbox(self.frm_navig, width=15, height=5)
        self.lst_savings.grid(row=1, column=0)
        self.lst_savings.bind("<<ListboxSelect>>", self.select_savings)

        self.ent_savings = tk.Entry(self.frm_navig, width=15)
        self.ent_savings.grid(row=3, column=0)

        self.btn_delete = tk.Button(self.frm_navig, text="Delete",
            command=self.delete_session)
        self.btn_delete.grid(row=2, column=0, sticky="we")

        self.btn_save = tk.Button(self.frm_navig, text="Save",
            command=self.save_session)
        self.btn_save.grid(row=4, column=0, sticky="we")

        # dicts
        self.lbl_dicts = tk.Label(self.frm_navig, text="Dicts")
        self.lbl_dicts.grid(row=0, column=1, sticky="we")

        self.lst_dicts = tk.Listbox(self.frm_navig, width=15, height=5)
        self.lst_dicts.grid(row=1, column=1)

        self.btn_dicts_delete = tk.Button(self.frm_navig, text="Delete",
            command=self.delete_dict)
        self.btn_dicts_delete.grid(row=2, column=1, sticky="we")

        self.btn_dicts_add = tk.Button(self.frm_navig, text="Add",
            command=self.add_dict)
        self.btn_dicts_add.grid(row=3, column=1, sticky="we")

        self.btn_dicts_merge = tk.Button(self.frm_navig, text="Merge dicts",
            command=self.merge_dicts)
        self.btn_dicts_merge.grid(row=4, column=1, sticky="we")

    def start_loop(self):
        self.window.mainloop()