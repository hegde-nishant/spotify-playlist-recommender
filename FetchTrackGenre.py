import os
import pandas as pd
import spotipy
import ast
from spotipy.oauth2 import SpotifyClientCredentials
from natsort import natsorted

import time
import requests  # Import the requests library for controlling timeouts
from spotipy.exceptions import SpotifyException

#Spotipy API credentials
client_id = 'b6a49f1969f141d6b35ae5df7e0e9e22'
client_secret = '99ec2c1d45214b22b0499beddc027aa7'
client_uri = 'http://localhost/'

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

folder_path = "/home/nhegde2/StatsProject/track_features_csv/"

#Files count
playlist_count = 0

# Set the timeout duration (e.g., 30 seconds)
timeout_duration = 30  # Timeout for the search request

# Set the maximum number of retries in case of failure
max_retries = 3
retry_delay = 5  # Time to wait between retries (in seconds)

sp._session.headers.update({'timeout': str(timeout_duration)})

print(len(natsorted(os.listdir(folder_path))))

for files in natsorted(os.listdir(folder_path))[171:]:
    playlist_genres = []
    playlist_count += 1
    
    df = pd.read_csv(folder_path + files)
    print("Working with: ", files)
    
    #Genres
    print("Checking genre of all artists of playlist {}".format(playlist_count))
    
    for artist in list(df['artist_name']):
        retries = 0
        while retries < max_retries:
            try:
                result = sp.search(artist)
                
                if not result['tracks']['items']:
                    playlist_genres.append(None)  # Append None if no result is found
                    break
            
                track = result['tracks']['items'][0]

                artist = sp.artist(track["artists"][0]["external_urls"]["spotify"])
                
                #Append the playlist genres list
                genres = artist.get("genres", [])
                #playlist_genres.append(artist["genres"])
                playlist_genres.append(genres if genres else None)
                
                break
                
            except requests.exceptions.Timeout:
                # Handle timeout exception
                print(f"Timeout while searching for artist {artist}. Retrying... ({retries + 1}/{max_retries})")
                retries += 1
                time.sleep(retry_delay)  # Wait before retrying

            except SpotifyException as e:
                # Handle Spotify-specific exceptions
                print(f"Spotify error occurred for artist {artist}: {e}")
                playlist_genres.append(None)
                break  # Move to the next artist in case of an API error

            except Exception as e:
                # Handle other unexpected exceptions
                print(f"Unexpected error occurred for artist {artist}: {e}")
                playlist_genres.append(None)
                break  # Move to the next artist

        # If maximum retries reached and still failed, append None
        if retries == max_retries:
            print(f"Failed to get data for artist {artist} after {max_retries} retries.")
            playlist_genres.append(None)
    
    if len(playlist_genres) != len(df['pos']):
        while len(playlist_genres) < len(df['pos']):
            playlist_genres.append(None)
            
    #Add the genre information
    df['genre'] = playlist_genres
    
    #Save the new csv
    df.to_csv(folder_path + files, index = False)
