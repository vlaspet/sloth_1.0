from pickle import dump
from pickle import load

class Dumper:
    def __init__(self, file_name):
        self.dump_dict = {}
        # where to save data
        self.file_name = file_name
        # trying to open in the binary mode if it will not open
        # we'll create a file for saving
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
        # saving a data by a name
        self.dump_dict[name] = data
        with open(self.file_name, "wb") as file:
            dump(self.dump_dict, file)

    def get_dump_data(self, name):
        return self.dump_dict[name]

    def get_dump(self):
        return self.dump_dict

    def clear_dump(self):
        # just rewriting a file with an empty dict
        try:
            with open(self.file_name, 'wb') as file:
                dump({}, file)
        except Exception as ex:
            print("Exception of writing in a pickle.", ex)

    def delete(self, name):
        # just to delete from a current self.dump_dict
        # and rewrite a dump file with the changed dict
        self.dump_dict.pop(name)
        with open(self.file_name, "wb") as file:
            dump(self.dump_dict, file)
