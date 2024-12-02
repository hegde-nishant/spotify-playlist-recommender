import pandas as pd
import ast

def clean_data(data):
    # Standardize column names
    data.columns = [column.strip().replace(' ', '_').lower() for column in data.columns]
    
    # Convert columns to appropriate types
    numeric_columns = ['duration_ms', 'danceability', 'energy', 'loudness', 'speechiness','acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
    integer_columns = ['key', 'mode', 'time_signature']
    
    data[numeric_columns] = data[numeric_columns].apply(pd.to_numeric, errors='coerce')
    data[integer_columns] = data[integer_columns].apply(pd.to_numeric, downcast='integer', errors='coerce')
    
    # Handle missing values
    data.dropna(subset=['track_uri'], inplace=True)
    for col in numeric_columns:
        data[col].fillna(data[col].median(), inplace=True)
    
    # Parse genres
    data['genre'] = data['genre'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
    
    # Remove duplicates
    data.drop_duplicates(subset=['track_uri', 'playlist_id'], inplace=True)
    
    return data