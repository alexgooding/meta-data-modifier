import glob


class AudioFolder:
    """
    Methods for gathering file paths of files with specific encodings.
    """

    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.common_audio_encodings = ['.mp3']

    def get_file_paths(self):
        """
        Recursively search a file path for files with the extensions
        listed in the class initialisation.
        :return: A list of file paths for each file found
        """
        path_list = []
        for encoding in self.common_audio_encodings:
            # Handle individual files being passed in
            if encoding in self.folder_path:
                path_list.append(self.folder_path)
                break
            pattern = self.folder_path + '/' + '**/*' + encoding
            path_list.extend(glob.glob(pattern, recursive=True))

        return path_list

    def get_file_paths_by_folder(self):
        """
        Uses get_file_paths to retrieve file paths and then organises
        them into sublists by the folder the files are contained in.
        :return: A list of lists containing the file paths found
        """
        file_paths = self.get_file_paths()
        file_paths_by_folder = []
        while file_paths:
            path_to_check = file_paths.pop(0)
            folder_paths = [path_to_check]
            for path in file_paths:
                if path.split('\\')[-2] == path_to_check.split('\\')[-2]:
                    folder_paths.append(path)
            file_paths_by_folder.append(folder_paths)
            file_paths = [path for path in file_paths if path not in folder_paths]

        return file_paths_by_folder
