import os.path


class Config():
    def __init__(self):
        pass

    def db_folder_path(self):
        return './database'

    def db_name(self):
        return 'amazon_data.db'

    def table_name(self):
        return 'amazon_data_table'

    def db_path(self):
        return os.path.join(self.db_folder_path(), self.db_name())

    def model_name(self):
        return "llama2:70b"



