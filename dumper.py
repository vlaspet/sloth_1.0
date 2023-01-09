from pickle import dump
from pickle import load

class Dumper:
    def __init__(self, file_name):
        self.dump_dict = {}
        self.file_name = file_name
        try:
            with open(file_name, 'rb') as file:
                self.dump_dict = load(file)
        except Exception as ex:
            print("Exception in Dumper __init__", ex)
            try:
                with open(file_name, 'wb') as file:
                    dump(self.dump_dict, file)
            except Exception as ex:
                print("Trying to create dump file.", ex)
    def save_data(self, data, name):
        self.dump_dict[name] = data
        with open(self.file_name, "wb") as file:
            dump(self.dump_dict, file)
    def get_dump_data(self, name):
        return self.dump_dict[name]
    def get_dump(self):
        return self.dump_dict
    def clear_dump(self):
        try:
            with open(self.file_name, 'wb') as file:
                dump({}, file)
        except Exception as ex:
            print("Exception of writing in a pickle.", ex)
    def delete(self, name):
        self.dump_dict.pop(name)
        with open(self.file_name, "wb") as file:
            dump(self.dump_dict, file)


# def select_savings(self, event):
#     index = self.lst_savings.curselection()[0]
#     session = self.lst_savings.get(index)
#     # self.name_session = session
#     self.init_from_dump(session)

# def save_session(self):
#     index = self.lst_savings.index(tk.END)
#     session = self.ent_savings.get()
#     self.ent_savings.delete(0, tk.END)
#     self.lst_savings.insert(index, session)
#     self.current_savings["session"].append(session)

#     self.current_savings.clear()

#     self.current_savings["session"] = [session]
#     if self.path_text != '':
#         self.current_savings["text"] = self.path_text
#     if self.path_dict != '':
#         self.current_savings["dict"] = self.path_dict

#     self.dump.save_data(self.current_savings, session)