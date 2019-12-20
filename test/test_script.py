from audio_folder import AudioFolder
from meta_modifier import MetaDataModifier

if __name__ == "__main__":
    audio_folder = AudioFolder("test")
    path_list = audio_folder.get_file_paths()

    for path in path_list:
        MetaDataModifier(path).set_meta_data(True, True)
