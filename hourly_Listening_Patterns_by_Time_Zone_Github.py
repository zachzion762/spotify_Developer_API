import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('spotify_listening_history.csv')

# Adjust datetime and timezone
df['played_at'] = pd.to_datetime(df['played_at'])
if df['played_at'].dt.tz is None:
    df['played_at'] = df['played_at'].dt.tz_localize('UTC')
df['played_at'] = df['played_at'].dt.tz_convert('America/Denver')

# Specific dates for analysis and plotting setup
dates = ['2024-02-09', '2024-02-10', '2024-02-11', '2024-02-12']
df['date'] = df['played_at'].dt.date
df['hour'] = df['played_at'].dt.hour
plt.figure(figsize=(15, 8))
bar_width = 0.4
n_dates = len(dates)
hours = sorted(df['hour'].unique())

# Plotting the bars for each date
for i, date in enumerate(dates):
    df_date = df[df['date'] == pd.to_datetime(date).date()]
    hourly_counts = df_date.groupby('hour').size()
    offsets = [x + i * bar_width for x in hours]
    plt.bar(offsets, hourly_counts.reindex(hours, fill_value=0), width=bar_width, label=date)

# Highlighting spans with labels
plt.axvspan(15, 18, color='yellow', alpha=0.3)
plt.axvspan(13, 15, color='orange', alpha=0.3)
plt.axvspan(6.5, 8, color='blue', alpha=0.3)
plt.axvspan(8, 10, color='green', alpha=0.3)

# Collecting handles and labels from the plot
handles, labels = plt.gca().get_legend_handles_labels()

# Adding custom labels for highlighted spans
custom_labels = ['Morning Commute', 'Morning Wind Down', 'Evening Commute', 'Evening Routine']
custom_colors = ['blue', 'green', 'yellow', 'orange']  # Corresponding colors
custom_handles = [plt.Rectangle((0, 0), 1, 1, color=color, alpha=0.3) for color in custom_colors]

# Combine original handles with custom ones
handles.extend(custom_handles)
labels.extend(custom_labels)

# Your desired order of labels
desired_order = ['2024-02-09', '2024-02-10', '2024-02-11', '2024-02-12', 'Morning Commute', 'Morning Wind Down', 'Evening Commute', 'Evening Routine']

# Reorder handles and labels based on the desired order
ordered_handles = [handles[labels.index(label)] for label in desired_order]
ordered_labels = desired_order

# Creating the legend with ordered handles and labels
plt.legend(ordered_handles, ordered_labels, title="Legend")

plt.title('Hourly Listening Patterns During Night Shift Routine')
plt.xlabel('Hour of Day')
plt.ylabel('Number of Tracks Played')
plt.xticks([r + bar_width * (n_dates / 2) - bar_width / 2 for r in hours], hours)

plt.show()
