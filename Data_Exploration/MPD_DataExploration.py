import pandas as pd
import json
import ast
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

#Spotipy API credentials
client_id = '22eb4af4128d453ea0b0f20219634010'
client_secret = '0b2097f478114da495981277e4c2d761'
client_uri = 'http://localhost/'

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#Reading million playlists csv
df = pd.read_csv("/home/nhegde2/StatsProject/data/MPD.csv")

#Basic data exploration
print("First few rows...")
print(df.head())

print("All the column names...")
print(df.columns)

print("Printing first 5 values of every column....")

for column in df.columns:
    print("Column {}".format(column))
    print("First 5 values of column: [{}]".format(column))
    print(df[column][:5])

    print("----------------------------------------")

print("Unique values of column: [description] ...")

print(df['description'].unique)

print("Dropping column: [description] ...")

df.drop('description', axis=1, inplace = True)

print("Value of one data point in column: [tracks]")

print(df["tracks"][:1])

track_features_path = "/gpfs/fs1/home/nhegde2/StatsProject/track_features_csv/"

#Format conversions
tracks = df["tracks"]
tracks = tracks.to_list()

#Fails in try block
exceptions = []

for i, track in enumerate(tracks):
    ast.literal_eval(track)
    df_track = pd.DataFrame(ast.literal_eval(track))
    track_uris = df_track['track_uri']
    try:
        features = sp.audio_features(list(track_uris))
        features_df = pd.DataFrame(data=features, columns=features[0].keys())
        #Drop redundant column
        features_df.drop('duration_ms', axis = 1, inplace = True)

        #Inner join the two dataframes
        df_track = pd.concat([df_track, features_df], axis=1, join='inner')
        
        #Save track features
        df_track.to_csv(track_features_path + 'track_features_' + 'playlist_' + str(i) + '.csv', index=False)
    except:
        exceptions.append(i)  #Note the index of the exceptions. These have to be removed from MPD csv if MPD data is also considered for analysis.

print("Done..")
print("Exceptions: ", exceptions) #TO-DO: Filter the exceptions from csv file names.
