import spotipy
from spotipy.oauth2 import SpotifyOAuth
import matplotlib.pyplot as plt

# Initialize Spotify client with your credentials
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='Enter Client ID',
                                               client_secret='Enter Client Secret',
                                               redirect_uri='Enter Redirect URI',
                                               scope='user-top-read'))

# Fetch your top tracks from Spotify
top_tracks = sp.current_user_top_tracks(limit=20, time_range='long_term')

# Extract track names
track_names = [track['name'] for track in top_tracks['items']]

# Use index position as a proxy for frequency (not exact play counts)
# Higher position indicates more frequent listening
positions = range(len(track_names))

# Create a bar chart
plt.figure(figsize=(10, 8))
plt.barh(track_names, positions, color='skyblue')
plt.xlabel('Position in Top Tracks (Lower is More Frequent)', fontweight='bold', fontsize=18)
plt.ylabel('Tracks', fontweight='bold', fontsize=18)
plt.title('My Top Tracks on Spotify', fontweight='bold', fontsize=20)
plt.tight_layout()
plt.gca().invert_yaxis()  # Invert y-axis so top tracks appear at the top
plt.show()



