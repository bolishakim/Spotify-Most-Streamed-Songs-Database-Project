import pandas as pd

# Load the dataset
df = pd.read_csv('Spotify Most Streamed Songs.csv')
df = df.drop_duplicates(subset=['track_name'])
df['track_name'] = df['track_name'].str.replace(r'[^\x00-\x7F]+', '?', regex=True)
# Convert columns to numeric and handle errors (non-numeric values will become NaN)
df['streams'] = pd.to_numeric(df['streams'], errors='coerce')
df['in_deezer_playlists'] = df['in_deezer_playlists'].str.replace(',', '').astype(int)
df['in_deezer_playlists'] = pd.to_numeric(df['in_deezer_playlists'], errors='coerce')
df['in_shazam_charts'] = pd.to_numeric(df['in_shazam_charts'], errors='coerce')

# Fill NaN values with 0 or any other value before converting to int64
df['streams'] = df['streams'].fillna(0).astype('int64')
df['in_deezer_playlists'] = df['in_deezer_playlists'].fillna(0).astype('int64')
df['in_shazam_charts'] = df['in_shazam_charts'].fillna(0).astype('int64')

# Convert other columns that are categorical or strings to appropriate types
df['mode'] = df['mode'].astype('category')

# 1. Normalize the Artist Table and Track Table

# Initialize an empty list for storing artist-track associations
artist_rows = []

# Iterate through the dataset to split and normalize artist names
for index, row in df.iterrows():
    artists = [artist.strip() for artist in row['artist(s)_name'].split(',')]  # Split artist names by comma
    for artist in artists:
        # For each artist, create a record with associated track details
        artist_rows.append({
            'Artist_Name': artist,
            'Track_Name': row['track_name'],
            'Streams': row['streams'],
            'Released_Month': row['released_month'],
            'Released_Year': row['released_year'],
            'Released_Day': row['released_day'],
            'Cover_URL': row.get('cover_url', 'Not Found')  # Handle missing Cover_URL with a default value
        })

# Convert the artist-track data to a DataFrame
normalized_df = pd.DataFrame(artist_rows)

# 2. Artist Table
# Extract unique artists and assign unique IDs
artist_df = normalized_df[['Artist_Name']].drop_duplicates().reset_index(drop=True)
artist_df['Artist_ID'] = 'Ar' + (artist_df.index + 1000).astype(str)
cols = ['Artist_ID'] + [col for col in artist_df.columns if col != 'Artist_ID']
artist_df = artist_df[cols]

# 3. Track Table
# Extract unique track-related data and assign unique IDs
track_df = normalized_df[['Track_Name', 'Streams', 'Released_Day', 'Released_Month', 'Released_Year', 'Cover_URL']].drop_duplicates().reset_index(drop=True)
track_df['Track_ID'] = 'Tr' + (track_df.index + 1000).astype(str)
cols = ['Track_ID'] + [col for col in track_df.columns if col != 'Track_ID']
track_df = track_df[cols]

# 4. Artist-Track Table (Many-to-Many Relationship)
# Create a join table to store artist-track associations
artist_track_data = []

for idx, row in normalized_df.iterrows():
    track_id = track_df[track_df['Track_Name'] == row['Track_Name']].iloc[0]['Track_ID']
    artist_id = artist_df[artist_df['Artist_Name'] == row['Artist_Name']].iloc[0]['Artist_ID']
    
    # Add the relationship to the join table
    artist_track_data.append({
        'Artist_ID': artist_id,
        'Track_ID': track_id
    })

# Convert the artist-track association data into a DataFrame
artist_track_df = pd.DataFrame(artist_track_data)

# 5. Metric Table
# Extract unique metrics (song features) and assign unique IDs
metric_columns = ['danceability_%', 'valence_%', 'energy_%', 'acousticness_%', 
                  'instrumentalness_%', 'liveness_%', 'speechiness_%', 'bpm', 'mode']

# Get the metric data (song features) and ensure track association
metric_df = df[metric_columns].drop_duplicates().reset_index(drop=True)
metric_df['Metric_ID'] = 'Mt' + (metric_df.index + 1000).astype(str)
track_id_map = track_df.set_index('Track_Name')['Track_ID'].to_dict()  # Map track_name to Track_ID
metric_df['Track_ID'] = df['track_name'].map(track_id_map)  # Map the Track_ID for each row
metric_df = metric_df[['Metric_ID', 'Track_ID'] + metric_columns]

# 6. Platform Table
# Define platform-related data columns
platform_data = []
platform_columns = {
    'Spotify': ['in_spotify_playlists', 'in_spotify_charts'],
    'Apple': ['in_apple_playlists', 'in_apple_charts'],
    'Deezer': ['in_deezer_playlists', 'in_deezer_charts'],
    'Shazam': ['in_shazam_charts']
}
platform_id_counter = 1000

for idx, row in df.iterrows():
    track_id = track_df.loc[track_df['Track_Name'] == row['track_name'], 'Track_ID'].values[0]
    for platform, columns in platform_columns.items():
        if platform == "Shazam":
            platform_data.append({
                'Platform_ID': f'Pl{platform_id_counter}',
                'Track_ID': track_id,
                'Platform_Name': platform,
                'In_Playlists': 0,
                'In_Charts': row[columns[0]]
            })
        else:
            platform_data.append({
                'Platform_ID': f'Pl{platform_id_counter}',
                'Track_ID': track_id,
                'Platform_Name': platform,
                'In_Playlists': row[columns[0]],
                'In_Charts': row[columns[1]]
            })
        platform_id_counter += 1

platform_df = pd.DataFrame(platform_data)

# 7. Save or Return the Tables for Use in Another Script

# Save to CSV (to be used in other scripts or database loading)
artist_df.to_csv('Databases Tables/artist_table.csv', index=False)
track_df.to_csv('Databases Tables/track_table.csv', index=False)
artist_track_df.to_csv('Databases Tables/artist_track_table.csv', index=False)
metric_df.to_csv('Databases Tables/metric_table.csv', index=False)
platform_df.to_csv('Databases Tables/platform_table.csv', index=False)

# Return the tables directly for use in another Python script
def get_normalized_data():
    return artist_df, track_df, artist_track_df, metric_df, platform_df

# Call the function to return the dataframes
artist_df, track_df, artist_track_df, metric_df, platform_df = get_normalized_data()
