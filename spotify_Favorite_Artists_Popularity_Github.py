import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify API credentials
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='Enter Client ID',
                                               client_secret='Enter Client Secret',
                                               redirect_uri='Enter Redirect Uri',
                                               scope='user-top-read'))

# Fetch top artists
top_artists = sp.current_user_top_artists(limit=20, time_range='medium_term')  # Adjust 'limit' and 'time_range' as needed

artist_names = [artist['name'] for artist in top_artists['items']]
popularity_scores = [artist['popularity'] for artist in top_artists['items']]

import matplotlib.pyplot as plt

plt.figure(figsize=(10, 8))
plt.barh(artist_names, popularity_scores, color='skyblue')
plt.xlabel('Popularity Score')
plt.ylabel('Artists')
plt.title('My Top Spotify Artists by Popularity')
plt.tight_layout()
plt.show()

