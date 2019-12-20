import os, sys
import mutagen
from mutagen.easyid3 import EasyID3
import ntpath


class MetaDataModifier:

    def __init__(self, file_path):
        self.file_path = file_path
        self.file_name = self.extract_filename(file_path)

    def set_meta_data(self, add_track_number=True, cleanup_title=True):
        try:
            tag = EasyID3(self.file_path)
        except:
            try:
                tag = mutagen.File(self.file_path, easy=True)
                tag.add_tags()
            except:
                print("Unexpected error:", sys.exc_info()[0])
                raise

        # Get the track number from the start of the file name and add to the track number meta data
        if add_track_number:
            track_number = self.retrieve_track_number(self.file_name)
            if track_number:
                tag['tracknumber'] = track_number

        # Add a cleaned up track title from the file name to the title meta data
        if cleanup_title:
            tag['title'] = self.strip_to_title(self.file_name)

        tag.save(self.file_path)

    @staticmethod
    def extract_filename(path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

    @staticmethod
    def strip_to_title(name):
        return os.path.splitext(name.lstrip('0123456789.- '))[0]

    @staticmethod
    def retrieve_track_number(name):
        name = name.lstrip()
        track_number = []
        for char in name:
            if char.isdigit():
                if char != '0' or track_number:
                    track_number.append(char)
            else:
                break

        return "".join(track_number)

    def print_file_name(self):
        print(self.file_name)
