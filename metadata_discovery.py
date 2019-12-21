from spotipy import Spotify
import spotipy.util as util
from spotipy.client import SpotifyException


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
            # print(tracks[0])
            return tracks
        except SpotifyException:
            raise

    def cross_reference_tracks_album(self, track_list, common_track_info=None, starting_track_index=0):
        number_successful_requests = 0
        try:
            if not common_track_info:
                common_track_info = [[track['album']['name'], [artist['name'] for artist in track['artists']]] for track in
                                     self.search_for_track_metadata(track_list[starting_track_index])]
            # print(common_track_info)
            starting_track_index += 1
            number_successful_requests += 1
            for i in range(starting_track_index, len(track_list)):
                next_track_info = [[track['album']['name'], [artist['name'] for artist in track['artists']]] for track in
                                     self.search_for_track_metadata(track_list[i])]
                # common_track_info = list(set(next_track_info).intersection(common_track_info))
                common_track_info = [element1 for element1 in common_track_info for element2 in next_track_info if element1 == element2]
                number_successful_requests += 1
            print(common_track_info)
            print(len(common_track_info))
        except SpotifyException as e:
            print("Too many results for Spotify request: " + str(e))
            self.cross_reference_tracks_album(track_list, common_track_info, number_successful_requests+1)

if __name__ == '__main__':
    MD = MetadataDiscoverer()
    # MD.search_for_track_metadata("kill everybody")
    MD.cross_reference_tracks_album(["right in", "the devil's den", "right on time"])
