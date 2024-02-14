import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import matplotlib.pyplot as plt

# Spotify credentials and setup
client_id = 'Enter Client ID'
client_secret = 'Enter Client Secret'
redirect_uri = 'Enter Redirect URI'
scope = 'user-top-read'

# Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))

# Fetch the top artists
top_artists = sp.current_user_top_artists(limit=50, time_range='long_term')

# Initialize a dictionary to count genres
genre_counts = {}

for artist in top_artists['items']:
    for genre in artist['genres']:
        if genre in genre_counts:
            genre_counts[genre] += 1
        else:
            genre_counts[genre] = 1

# Convert genre_counts to a Pandas DataFrame for easier handling
df_genres = pd.DataFrame(list(genre_counts.items()), columns=['Genre', 'Count'])

# Sort the DataFrame by count to get the top genres
df_genres = df_genres.sort_values(by='Count', ascending=False).reset_index(drop=True)

# Plotting
plt.figure(figsize=(10, 8))
plt.bar(df_genres['Genre'][:10], df_genres['Count'][:10], color='skyblue')
plt.xlabel('Genres', fontweight='bold')
plt.ylabel('Count', fontweight='bold')
plt.xticks(rotation=45, ha='right')
plt.title('Top 10 Music Genres from My Spotify Data', fontweight='bold')
plt.tight_layout()
plt.show()

