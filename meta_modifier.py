import os, sys
import mutagen
from mutagen.easyid3 import EasyID3
import ntpath
from metadata_discovery import MetadataDiscoverer


class MetaDataModifier:
    """
    A class to edit meta data for files in the same folder.
    This is so it can cross reference gathered file information,
    making the assumption that files are grouped by folder.
    """

    def __init__(self, path_list):
        self.path_list = path_list

    def set_meta_data_for_folder(self, add_track_number=True, cleanup_title=True, ai_metadata=False):
        """
        The main method used by the gui to retrieve and set all the required metadata.
        :param add_track_number: Determines whether an attempt is made to set the track number metadata
        :param cleanup_title: Determines whether an attempt is made to add a clean track title based off the filename
        :param ai_metadata: Determines whether an attempt is made to gather album metadata
        :return: none
        """
        for path in self.path_list:
            file_name = self.extract_filename(path)
            try:
                tag = EasyID3(path)
            except:
                try:
                    tag = mutagen.File(path, easy=True)
                    tag.add_tags()
                except:
                    print("Unexpected error:", sys.exc_info()[0])
                    raise

            # Get the track number from the start of the file name and add to the track number meta data
            if add_track_number:
                track_number = self.retrieve_track_number(file_name)
                if track_number:
                    tag['tracknumber'] = track_number

            # Add a cleaned up track title from the file name to the title meta data
            if cleanup_title:
                tag['title'] = self.strip_to_title(file_name)

            tag.save(path)

        if ai_metadata:
            try:
                MD = MetadataDiscoverer()
                raw_album_metadata = MD.find_album_metadata([self.strip_to_title(self.extract_filename(path)) for path in self.path_list])
                album_metadata = self.extract_useful_album_metadata(raw_album_metadata)
                self.set_album_metadata(album_metadata)
            except ValueError as ve:
                raise

    def set_album_metadata(self, album_metadata):
        for path in self.path_list:
            try:
                tag = EasyID3(path)
            except:
                try:
                    tag = mutagen.File(path, easy=True)
                    tag.add_tags()
                except:
                    print("Unexpected error:", sys.exc_info()[0])
                    raise

            tag['album'] = album_metadata.get('album_name')
            tag['albumartist'] = album_metadata.get('album_artists')
            tag.save(path)

    @staticmethod
    def extract_useful_album_metadata(raw_metadata):
        album_metadata = {}
        album_metadata['album_name'] = raw_metadata.get('name')
        album_metadata['album_artists'] = ', '.join([artist.get('name') for artist in raw_metadata.get('artists')])
        return album_metadata

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
