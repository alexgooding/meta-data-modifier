import glob


class AudioFolder:

    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.common_audio_encodings = ['.mp3']

    def get_file_paths(self):
        path_list = []
        for encoding in self.common_audio_encodings:
            # Handle individual files being passed in
            if encoding in self.folder_path:
                path_list.append(self.folder_path)
                break
            pattern = self.folder_path + '/' + '**/*' + encoding
            path_list.extend(glob.glob(pattern, recursive=True))

        return path_list
