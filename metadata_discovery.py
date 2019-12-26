from spotipy import Spotify
import spotipy.util as util
from spotipy.client import SpotifyException
from numpy import argmin


class MetadataDiscoverer:
    """
    A class to access metadata via the Spotify API and intelligently
    guess the correct meta data for a collection of songs based on their
    track titles
    """

    def __init__(self):
        SPOTIPY_CLIENT_ID = 'b6227692e279468b8dc73975240df0b3'
        SPOTIPY_CLIENT_SECRET = '459cb2f1c81146c0b6eaffbded50f2a2'

        token = util.oauth2.SpotifyClientCredentials(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET)
        cache_token = token.get_access_token()
        self.sp = Spotify(cache_token)

    def find_album_metadata(self, track_list):
        """
        The main method used when editing file metadata to run the cross referencing algorithm.
        :param track_list: The list of track names to be used in the search
        :return: The
        """
        try:
            album_metadata = None
            sorted_track_list = []
            if track_list:
                sorted_track_list = self.sort_track_list(track_list)
                album_metadata = self.cross_reference_album_info(sorted_track_list, [])

            if not album_metadata:
                for i in range(1, len(track_list)):
                    sorted_track_list.insert(0, sorted_track_list.pop(i))
                    album_metadata = self.cross_reference_album_info(sorted_track_list, [])
                    if album_metadata:
                        print("Successfully found the following album metadata: " + str(album_metadata[0]))
                        with open("log.txt", "a") as my_file:
                            my_file.write("Successfully found a single cross-referenced album metadata\n")
                        return album_metadata[0]
                raise ValueError("No metadata found for track list '{0}'".format(', '.join(track_list)))
            print("Successfully found the following album metadata: " + str(album_metadata[0]))
            with open("log.txt", "a") as my_file:
                my_file.write("Successfully found a single cross-referenced album metadata\n")
            return album_metadata[0]
        except ValueError as ve:
            print(ve)
            with open("log.txt", "a") as my_file:
                my_file.write(str(ve) + "\n")
            raise

    def search_for_track_metadata(self, track_title):
        """
        A method to gather all search results for a track title.
        The Spotify API has a limit of 10,000 search results.
        :param track_title: The track title to search with
        :return: A list containing each dictionary of track metadata matched through the search
        """
        try:
            results = self.sp.search(q='track:' + track_title, type='track', limit=50)
            tracks = results['tracks']['items']
            while results['tracks']['next']:
                results = self.sp.next(results['tracks'])
                tracks.extend(results['tracks']['items'])
            print("Found track information for track: " + track_title)
            with open("log.txt", "a") as my_file:
                my_file.write("Found track information for track: " + track_title)

            return tracks
        except SpotifyException:
            raise

    def cross_reference_album_info(self, track_list, common_album_info, starting_track_index=0, total_number_of_successful_requests=0):
        """
        A method to cross reference the album name and album artist of a list of tracks to
        obtain a single dictionary of correct album metadata. Requires Python 3.6+ to use repr() to
        compare dictionaries successfully.
        :param track_list: A list of track strings to cross reference
        :param common_album_info: Used in recursion to pass in the current cross section of album metadata
        :param starting_track_index: Used in recursion to indicate where in the track list to continue cross referencing
        :param total_number_of_successful_requests: The total number of successful API requests
        :return: The single dictionary of album metadata relevant to two or more tracks in the track list. None returned otherwise
        """
        number_successful_requests = 0
        try:
            initialisation_correction = 0
            while not common_album_info and starting_track_index + initialisation_correction <= len(track_list):
                common_album_info = [track['album'] for track in self.search_for_track_metadata(track_list[starting_track_index+initialisation_correction])]
                print("results for: " + track_list[starting_track_index+initialisation_correction])
                print(common_album_info)
                print("")
                with open("log.txt", "a") as my_file:
                    my_file.write("Found album results for: " + track_list[starting_track_index+initialisation_correction] + "\n")
                initialisation_correction += 1
                number_successful_requests += 1
                total_number_of_successful_requests += 1
            for i in range(starting_track_index + initialisation_correction, len(track_list)):
                next_album_info = [track['album'] for track in self.search_for_track_metadata(track_list[i])]
                print("results for: " + track_list[i])
                print(next_album_info)
                print("")
                with open("log.txt", "a") as my_file:
                    my_file.write("Found album results for: " + track_list[i] + "\n")
                album_info_intersection = [element1 for element1 in next_album_info for element2 in common_album_info
                                     if repr(element1) == repr(element2)]

                # Skip track if intersection with previous album info is none
                if album_info_intersection:
                    common_album_info = album_info_intersection
                    total_number_of_successful_requests += 1

                number_successful_requests += 1

                # If the intersection of album info is length one after intersecting two of more tracks, return
                if total_number_of_successful_requests > 1 and len(common_album_info) == 1:
                    return common_album_info
                else:
                    return []

        except SpotifyException as e:
            print("Too many results for Spotify request: " + str(e) + "\nTrack skipped.")
            with open("log.txt", "a") as my_file:
                my_file.write("Too many results for Spotify request: " + str(e) + "\nTrack skipped.\n")
            common_album_info = self.cross_reference_album_info(track_list, common_album_info,
                                                                starting_track_index+number_successful_requests+1,
                                                                total_number_of_successful_requests)

        if len(common_album_info) > 1:
            common_album_info = self.pick_album_with_the_closest_number_of_tracks(common_album_info, len(track_list))
        return common_album_info

    @staticmethod
    def pick_album_with_the_closest_number_of_tracks(albums, track_list_len):
        """
        Picks the album with the number of tracks closest to that of the inputted track list.
        :param albums: A list of potential album metadatas
        :param track_list_len: The length of the input track list
        :return: A list of length 1 with the most relevant album meta data dictionary
        """
        index = argmin([abs(album['total_tracks'] - track_list_len) for album in albums])
        return [albums[index]]

    @staticmethod
    def sort_track_list(track_list):
        return sorted(track_list, key=len, reverse=True)
