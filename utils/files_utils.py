
import json
import os

class FilesUtils:
    
    @staticmethod
    def create_folder(directory: str):
        if not os.path.exists(directory):
            os.makedirs(directory)

    @staticmethod
    def create_json_file_if_not_exist(path: str):
        if not os.path.isfile(path):
            with open(path, "w") as file:
                json.dump({}, file, indent=4)
                file.flush()

    @staticmethod
    def read_json_file(path: str):
        with open(path, 'r') as file:
            data = json.load(file)
        return data
    
    @staticmethod
    def write_json_file(path: str, data: any):
        with open(path, "w") as file:
            json.dump(data, file, indent=4)
            file.flush()

    @staticmethod
    def is_path_exists(path):
        return os.path.exists(path)
    
    @staticmethod
    def get_file_path(directory: str, file_name: str):
        return os.path.join(directory, file_name)
       