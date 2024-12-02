import pandas as pd
import ast

def feature_engineering(data):
    # Categorize tracks based on appearance counts
    track_counts = data.groupby('track_uri').size().reset_index(name='playlist_count')
    
    def categorize_track(count):
        if count == 1:
            return 'Unique Song'
        elif 2 <= count <= 5:
            return 'Common Song'
        else:
            return 'Popular Song'
    
    track_counts['category'] = track_counts['playlist_count'].apply(categorize_track)
    data = data.merge(track_counts, on='track_uri', how='left')

    # Average track position within playlists
    data['average_position'] = data.groupby('track_uri')['pos'].transform('mean')

    # Compute average audio features for each playlist
    audio_features = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness','instrumentalness', 'liveness', 'valence', 'tempo']
    avg_playlist_features = data.groupby('playlist_id')[audio_features].mean().add_suffix('_avg_playlist')
    data = data.merge(avg_playlist_features, on='playlist_id', how='left')
    
    # Genre analysis
    data['genre_list'] = data['genre'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else [])
    exploded = data.explode('genre_list')
    genre_counts = exploded['genre_list'].value_counts().reset_index(name='count')
    genre_counts.rename(columns={'index': 'genre'}, inplace=True)
    
    return data, genre_counts