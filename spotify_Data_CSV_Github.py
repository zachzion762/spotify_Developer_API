import sys
import os

# Ensure the sys.path includes the directory where pandas is installed
sys.path.append('Enter System Path')

# Print sys.path to confirm the correct paths are included
print(sys.path)

import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth



# Function to fetch and append new tracks
def fetch_and_append_new_tracks(sp, csv_path='spotify_listening_history.csv'):
    # Load the existing data if available to find the most recent 'played_at' timestamp
    if os.path.exists(csv_path):
        df_existing = pd.read_csv(csv_path)
        last_played_at = df_existing['played_at'].max()
    else:
        df_existing = pd.DataFrame()
        last_played_at = None

    # Fetch the last 50 tracks played
    results = sp.current_user_recently_played(limit=50)
    tracks_data = []

    for item in results['items']:
        track = item['track']
        played_at = item['played_at']
        # Only add tracks that were played after the last recorded timestamp
        if last_played_at is None or played_at > last_played_at:
            tracks_data.append({
                'played_at': played_at,
                'track_name': track['name'],
                'artist': ', '.join(artist['name'] for artist in track['artists']),
                'track_id': track['id'],
                'album': track['album']['name']
            })

    # Convert to DataFrame
    df_tracks = pd.DataFrame(tracks_data)

    # Append new data to the existing dataset if there is any
    if not df_tracks.empty:
        df_combined = pd.concat([df_existing, df_tracks], ignore_index=True)
        df_combined.to_csv(csv_path, index=False)

# Specify your cache path for Spotify token
cache_path = '/home/zzion/.cache-spotipy'  # Adjust as needed

# Initialize Spotify client with explicit cache_path
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='Enter Client ID',
                                               client_secret='Enter Client Secret',
                                               redirect_uri='Enter Redirect URI',
                                               scope='user-read-recently-played',
                                               cache_path=cache_path))

# Call the function to fetch and append new tracks
fetch_and_append_new_tracks(sp)
