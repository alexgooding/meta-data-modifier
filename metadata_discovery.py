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

    def search_for_track_metadata(self, track_title):
        try:
            results = self.sp.search(q='track:' + track_title, type='track', limit=50)
            tracks = results['tracks']['items']
            while results['tracks']['next']:
                results = self.sp.next(results['tracks'])
                tracks.extend(results['tracks']['items'])
            return tracks
        except SpotifyException:
            raise

    def cross_reference_album_info(self, track_list, common_album_info=None, starting_track_index=0):
        number_successful_requests = 0
        try:
            initialisation_correction = 0
            if not common_album_info and starting_track_index <= len(track_list):
                common_album_info = [track['album'] for track in self.search_for_track_metadata(track_list[starting_track_index])]
                initialisation_correction = 1
                number_successful_requests += 1
            for i in range(starting_track_index + initialisation_correction, len(track_list)):
                next_album_info = [track['album'] for track in self.search_for_track_metadata(track_list[i])]
                common_album_info = [element1 for element1 in next_album_info for element2 in common_album_info
                                     if repr(element1) == repr(element2)]
                number_successful_requests += 1

        except SpotifyException as e:
            print("Too many results for Spotify request: " + str(e))
            common_album_info = self.cross_reference_album_info(track_list, common_album_info, starting_track_index+number_successful_requests+1)

        if len(common_album_info) > 1:
            common_album_info = self.pick_album_with_the_closest_number_of_tracks(common_album_info, len(track_list))
        return common_album_info

    @staticmethod
    def pick_album_with_the_closest_number_of_tracks(albums, track_list_len):
        index = argmin([abs(album['total_tracks'] - track_list_len) for album in albums])
        return [albums[index]]
