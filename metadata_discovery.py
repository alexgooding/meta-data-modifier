from spotipy import Spotify
import spotipy.util as util


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
        results = self.sp.search(q='track:' + track_title, type='track', limit=50)
        tracks = results['tracks']['items']
        while results['tracks']['next']:
            results = self.sp.next(results['tracks'])
            tracks.extend(results['tracks']['items'])
        # print(tracks[0]['album']['name'])
        return tracks

    def cross_reference_tracks_album(self, track_list):
        common_albums_names = [track['album']['name'] for track in self.search_for_track_metadata(track_list[0])]
        for i in range(1, len(track_list)):
            next_album_names = [track['album']['name'] for track in self.search_for_track_metadata(track_list[i])]
            common_albums_names = list(set(next_album_names).intersection(common_albums_names))
        print(common_albums_names)
        print(len(common_albums_names))

if __name__ == '__main__':
    MD = MetadataDiscoverer()
    MD.cross_reference_tracks_album(["kill everybody", "scary monsters and nice sprites"])
