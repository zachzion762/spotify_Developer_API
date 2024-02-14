import spotipy
from spotipy.oauth2 import SpotifyOAuth
import matplotlib.pyplot as plt
import numpy as np
from adjustText import adjust_text  # Import the library for adjusting text

# Your Spotify API credentials and initialization of the Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='Enter Client ID',
                                               client_secret='Enter Client Secret',
                                               redirect_uri='Enter Redirect URI',
                                               scope='user-top-read'))

# Fetching top tracks and audio features
top_tracks = sp.current_user_top_tracks(limit=20, time_range='long_term')
track_ids = [track['id'] for track in top_tracks['items']]
audio_features = sp.audio_features(track_ids)

# Extracting valence, energy, loudness, and track names
valences = [feature['valence'] for feature in audio_features]
energies = [feature['energy'] for feature in audio_features]
loudness = [feature['loudness'] for feature in audio_features]
track_names = [track['name'] for track in top_tracks['items']]

# Adjusting loudness for visibility in the plot
loudness_adjusted = [abs(loud) + 10 for loud in loudness]  # Increase point size

plt.figure(figsize=(14, 10))

# Adjusting y-axis limits to reduce empty space
plt.ylim(bottom=np.percentile(energies, 20) - 0.05, top=np.percentile(energies, 100) + 0.05)


# Color coding by energy: the higher the energy, the warmer the color
colors = np.array(energies) * 100  # Adjust color intensity

# Creating scatter plot with color coding and adjusted sizes
sc = plt.scatter(valences, energies, s=loudness_adjusted, c=colors, cmap='coolwarm', alpha=0.6, edgecolors='black', linewidth=0.5)

# Adding color bar to indicate energy levels
cbar = plt.colorbar(sc)
cbar.set_label('Energy Level')

# Customizing the plot with labels and a grid
plt.xlabel('Valence (Mood Positivity)', fontsize=12, fontweight='bold')
plt.ylabel('Energy (Intensity)', fontsize=12, fontweight='bold')
plt.title('My Top Tracks: Mood vs. Intensity', fontsize=16, fontweight='bold')

plt.grid(True, which='both', linestyle='--', linewidth=0.75, alpha=0.5)

# Drawing quadrant lines and adding quadrant descriptions
mean_valence = np.mean(valences)
mean_energy = np.mean(energies)

plt.axhline(mean_energy, color='gray', linestyle='--')
plt.axvline(mean_valence, color='gray', linestyle='--')

# Enhanced Quadrant descriptions with solid background and zorder
quadrant_texts = [
    plt.text(0.1, 0.9, 'Happy & Energetic', transform=plt.gca().transAxes, fontsize=14, fontweight='bold', color='green', 
             bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5', alpha=1), zorder=5),
    plt.text(0.1, 0.1, 'Sad & Calm', transform=plt.gca().transAxes, fontsize=14, fontweight='bold', color='blue',
             bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5', alpha=1), zorder=5),
    plt.text(0.9, 0.9, 'Happy & Calm', transform=plt.gca().transAxes, fontsize=14, fontweight='bold', color='darkorange', ha='right',
             bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5', alpha=1), zorder=5),
    plt.text(0.9, 0.1, 'Sad & Energetic', transform=plt.gca().transAxes, fontsize=14, fontweight='bold', color='red', ha='right',
             bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5', alpha=1), zorder=5)
]

# Highlighting and labeling a few tracks for interest
annotations = []
for i, txt in enumerate(track_names):
    if energies[i] > 0.8 or valences[i] < 0.2:  # Example condition to label specific tracks
        annotation = plt.annotate(txt, (valences[i], energies[i]), textcoords="offset points", xytext=(5,5), ha='right', fontsize=9, fontweight='bold', clip_on=True)
        annotations.append(annotation)

# Use adjust_text to improve label placement
adjust_text(annotations, arrowprops=dict(arrowstyle='->', color='red'))

plt.tight_layout()
plt.show()
