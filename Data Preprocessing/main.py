import os
import pandas as pd
from load_and_merge import load_and_merge_playlists
from clean_data import clean_data
from feature_engineering import feature_engineering
from utils import ensure_directory_exists

def main():
    # Directories
    input_dir = 'Data'
    output_dir = 'Processed_Playlists'
    ensure_directory_exists(output_dir)

    # Load and Merge
    print("Loading and merging data...")
    merged_data = load_and_merge_playlists(input_dir, output_dir)

    # Clean Data
    print("Cleaning data...")
    cleaned_data = clean_data(merged_data)

    # Feature Engineering
    print("Performing feature engineering...")
    final_data, genre_counts = feature_engineering(cleaned_data)

    # Save Outputs
    print("Saving processed data...")
    final_data.to_csv(os.path.join(output_dir, 'final_cleaned_playlist_data.csv'), index=False)
    genre_counts.to_csv(os.path.join(output_dir, 'genre_counts.csv'), index=False)
    print("Data processing complete.")

if __name__ == "__main__":
    main()