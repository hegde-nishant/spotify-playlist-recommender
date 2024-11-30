import os
import pandas as pd
import spotipy
import ast
from spotipy.oauth2 import SpotifyClientCredentials
from natsort import natsorted
import subprocess
import json

import time
import requests  # Import the requests library for controlling timeouts
from spotipy.exceptions import SpotifyException

folder_path = "/home/nhegde2/StatsProject/track_features_csv/"
json_save_path = "/home/nhegde2/StatsProject/genre_and_popularity/"

#Files count
playlist_count = 0

#Access Token
access_token = "BQDyiX7qbtLSgn4or6waoYjsmWuedGRHkAfnbIksJtEh8qCokoB_jK_fNaKxDe4jeqOsFspRSJXtsC7iwYN3Tbrxm6tzMmfHavtn3aI-sSLvo5JcqEs"

#print(natsorted(os.listdir(folder_path)).index("track_features_playlist_364.csv"))

for i, files in enumerate(natsorted(os.listdir(folder_path))[65:165]):
    playlist_genres = []
    track_popularity = []       #Also fetch track popularity
    
    playlist_count += 1
    
    df = pd.read_csv(folder_path + files)
    print("Working with: ", files)
    print("Index: ", i)
    
    #Genres
    print("Checking genre and popularity of all artists of playlist {}".format(playlist_count))
    
    for j, artist_uri in enumerate(list(df['artist_uri'])):
        print('-----------------------------------------')
        save_folder_name = files.replace(".csv", "")
        
        # Create the directory if it doesn't exist
        if not os.path.exists(os.path.join(json_save_path, save_folder_name)):
            os.makedirs(os.path.join(json_save_path, save_folder_name))
            
        save_path = os.path.join(json_save_path, save_folder_name)
        
        #Fetch artist data
        url = "https://api.spotify.com/v1/artists/" + artist_uri.split(':')[-1]
        headers = "Authorization: Bearer " + access_token
        command = ["curl", "--request", "GET", "--url", url, "--header", headers]

        result = subprocess.run(command, capture_output=True, text=True)
        
        # Check if the request was successful (status code 200)
        if result.returncode == 0:
            # Save the output to a JSON file
            with open(save_path + '/' + str(j) + "_artist_info" + ".json", "w") as json_file:
                json.dump(json.loads(result.stdout), json_file, indent=4)
            print("Data saved to {}".format(str(j) + "_artist_info" + ".json"))
        else:
            print(f"Failed to fetch data. Error: {result.stderr}")
        
        track_uri = df['track_uri'][j]
       
        url = "https://api.spotify.com/v1/tracks/" + track_uri.split(':')[-1]
        headers = "Authorization: Bearer " + access_token
        command = ["curl", "--request", "GET", "--url", url, "--header", headers]
        
        result = subprocess.run(command, capture_output=True, text=True)
        
        # Check if the request was successful (status code 200)
        if result.returncode == 0:
            # Save the output to a JSON file
            with open(save_path + '/' + str(j) + "_track_info" + ".json", "w") as json_file:
                json.dump(json.loads(result.stdout), json_file, indent=4)
            print("Data saved to {}".format(str(j) + "_track_info" + ".json"))
        else:
            print(f"Failed to fetch data. Error: {result.stderr}")