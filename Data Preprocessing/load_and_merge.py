import pandas as pd
import glob
import os

def load_and_merge_playlists(input_dir, output_dir):
    all_files = glob.glob(os.path.join(input_dir, '*.csv'))
    df_list = []

    for idx, file in enumerate(all_files):
        df = pd.read_csv(file)
        df['playlist_id'] = idx  # Assign unique identifier for each playlist
        df_list.append(df)

    merged_data = pd.concat(df_list, ignore_index=True)
    track_counts = merged_data.groupby('track_uri').size().reset_index(name='playlist_count')
    merged_data = merged_data.merge(track_counts, on='track_uri', how='left')

    merged_output_path = os.path.join(output_dir, 'merged_playlists_with_counts.csv')
    merged_data.to_csv(merged_output_path, index=False)
    return merged_data