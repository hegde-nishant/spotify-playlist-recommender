import os
import pandas as pd
from tabulate import tabulate
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

#Spotipy API credentials - Anirudh's creds
client_id = '22eb4af4128d453ea0b0f20219634010'
client_secret = '99ec2c1d45214b22b0499beddc027aa7'
client_uri = 'http://localhost/'

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

folder_path = "/home/nhegde2/StatsProject/track_features_csv/"

#Files count
playlist_count = 0

#tracks_count
tracks_count = 0

#unique_artists
unique_artist_count = 0

#unique_tracks
unique_tracks_count = 0

#All genres
all_genres = []

for files in sorted(os.listdir(folder_path)):
    playlist_count += 1
    
    df = pd.read_csv(folder_path + files)
    
    tracks_count += len(df['pos'])
    
    unique_artist_count += len(list(df['artist_name'].unique()))
    
    unique_tracks_count += len(list(df['track_name'].unique()))
    
    '''
    #Genres
    print("Checking genre of all artists of playlist {}".format(playlist_count))
    
    for artist in list(df['artist_name'].unique()):
        try:
            result = sp.search(artist)
            
            track = result['tracks']['items'][0]
            
            artist = sp.artist(track["artists"][0]["external_urls"]["spotify"])
            
            print(artist["genres"])
            
            #Extend the all genres list
            all_genres.extend(artist["genres"])
            
        except:
            continue
    '''
    
table_data = [
    ["Playlists Count", playlist_count],            #858 from out
    ["Total Tracks", tracks_count],                 #36128 from out
    ["Unique Artists", unique_artist_count],        #23244 from out
    ["Unique Tracks", unique_tracks_count]          #35619 from out
]

# Print the table
headers = ["Metric", "Value"]
print(tabulate(table_data, headers=headers, tablefmt="grid"))

'''
#Dictionary for genre counts
genre_count_dict = {}

for genre in all_genres:
    genre_count_dict[genre] = all_genres.count(genre)
    
print(genre_count_dict)

#Saving genre dictionary
genre_df = pd.DataFrame(genre_count_dict.items(), columns=['Genre', 'Count'])
genre_df.to_csv('track_genre.csv', index=False)
'''
 