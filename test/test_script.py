from audio_folder import AudioFolder
from meta_modifier import MetaDataModifier

if __name__ == "__main__":
    audio_folder = AudioFolder("../test/test_resources/Sanctuary")
    path_list = audio_folder.get_file_paths()
    MetaDataModifier(path_list).set_meta_data_for_folder(False, False, True)

