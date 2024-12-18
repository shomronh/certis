from logger.logs_handler import LogsHandler
from files.files_utils import FilesUtils


class FilesCorruptionsHandler:

    @staticmethod
    def write_json_file(directory: str, file_name: str, data: any):

        try:
            FilesUtils.create_folder(directory)

            path = FilesUtils.get_file_path(directory, file_name)
            FilesUtils.create_json_file_if_not_exist(path)

            temp_path = FilesUtils.get_file_path(directory, f'temp_{file_name}')
            FilesUtils.create_json_file_if_not_exist(temp_path)

            FilesUtils.write_json_file(temp_path, data)
            LogsHandler.get_instance().log(f"write temporary data to temp_path={temp_path} succeeded")

            FilesUtils.rename_file(temp_path, path)
            LogsHandler.get_instance().log(f"rename temp_path={temp_path} to path={path} succeeded")

        except Exception as e:
            LogsHandler.get_instance().error(f"trying to write to json file failed: {e}")


    # TODO: try to load previous temporary file before switching to empty file mode
    @staticmethod
    def read_json_file(path: str):
        try:
            data = FilesUtils.read_json_file(path)
            LogsHandler.get_instance().critical(f"reading json file {path} succeeded")
            return data
        except Exception as e:
            LogsHandler.get_instance().critical(f"reading json file {path} failed, switching to empty file: {e}")
            data = {}
            FilesUtils.write_json_file(path, data)
            return data
