import spotipy
from spotipy.oauth2 import SpotifyOAuth
from collections import defaultdict
import matplotlib.pyplot as plt

def main():
    # Spotify API credentials - Replace these with your actual credentials
    client_id = 'Enter Client ID'
    client_secret = 'Enter Client Secret'
    redirect_uri = 'Enter Redirect Uri'
    scope = 'user-top-read'

    # Initialize Spotify client
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                   client_secret=client_secret,
                                                   redirect_uri=redirect_uri,
                                                   scope=scope))

    # Fetch top tracks
    top_tracks = sp.current_user_top_tracks(limit=50, time_range='long_term')  # Adjust limit/time_range as needed

    # Count appearances of each artist in top tracks
    artist_appearances = defaultdict(int)
    for track in top_tracks['items']:
        for artist in track['artists']:
            artist_appearances[artist['name']] += 1

    # Sort artists by number of appearances, descending
    sorted_artists = sorted(artist_appearances.items(), key=lambda x: x[1], reverse=True)

    # Select top 20 artists for plotting
    artist_names, appearance_counts = zip(*sorted_artists[:20])

    # Create a horizontal bar chart
    plt.figure(figsize=(10, 8))
    plt.barh(artist_names, appearance_counts, color='skyblue')
    plt.xlabel('NUMBER OF APPEARANCES IN TOP TRACKS', fontweight='bold',fontsize=15)
    plt.ylabel('ARTISTS', fontweight='bold',fontsize=15)
    plt.title('FAVORITE ARTISTS PER LISTENING FREQUENCY', fontweight='bold',fontsize=18)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
