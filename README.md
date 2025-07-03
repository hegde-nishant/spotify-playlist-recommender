# Spotify Playlist Recommender

A comprehensive analysis project focused on optimizing playlist recommendations through statistical and non-parametric analysis of track popularity, genre diversity, and playlist structure using the Million Playlist Dataset (MPD).

## Overview

This project analyzes Spotify playlist data to understand patterns in music consumption and recommendation systems. The codebase processes large-scale playlist data, integrates with the Spotify Web API for enhanced metadata, and performs statistical analysis to derive insights about track popularity and playlist composition.

## Features

- **Data Processing Pipeline**: Modular ETL pipeline for processing Million Playlist Dataset
- **Spotify API Integration**: Fetches track metadata including genres, popularity scores, and audio features
- **Feature Engineering**: Creates derived features like track categorization and playlist-level statistics
- **Statistical Analysis**: Implements Mann-Whitney U tests and other non-parametric analyses
- **Genre Analysis**: Comprehensive genre diversity and distribution analysis

## Project Structure

```
spotify-playlist-recommender/
├── Data Preprocessing/           # Core data processing pipeline
│   ├── main.py                  # Pipeline orchestrator
│   ├── load_and_merge.py        # Data loading and merging
│   ├── clean_data.py            # Data cleaning and standardization
│   ├── feature_engineering.py   # Feature creation and transformation
│   └── utils.py                 # Utility functions
├── Data_Exploration/            # Initial data exploration
│   └── MPD_DataExploration.py   # Million Playlist Dataset analysis
├── Tests/                       # Statistical tests
│   └── Mann_Whitney_U/          # Non-parametric test implementations
├── FetchTrackGenre.py          # Spotify genre metadata fetcher
├── FetchTrackGenre_and_Popularity.py  # Extended metadata fetcher
└── TrackFeatures_Exploration.py # Audio features analysis
```

## Prerequisites

- Python 3.7+
- Spotify Developer Account (for API access)

## Required Dependencies

Install the following Python packages:

```bash
pip install pandas spotipy natsort tabulate requests
```

## Setup

### 1. Spotify API Credentials

1. Create a Spotify Developer account at [Spotify for Developers](https://developer.spotify.com/)
2. Create a new app to get your Client ID and Client Secret
3. Update the credentials in the following files:
   - `FetchTrackGenre.py` (lines 13-14)
   - `FetchTrackGenre_and_Popularity.py` (lines 13-14)
   - `Data_Exploration/MPD_DataExploration.py` (lines 8-10)
   - `TrackFeatures_Exploration.py` (lines 8-10)

```python
client_id = 'your_spotify_client_id'
client_secret = 'your_spotify_client_secret'
```

### 2. Data Directory Setup

Create the following directory structure:

```
Data/                    # Input CSV files (playlist data)
Processed_Playlists/     # Output directory (auto-created)
```

## Usage

### Main Data Processing Pipeline

Run the complete data processing pipeline:

```bash
cd "Data Preprocessing"
python main.py
```

This will:
1. Load and merge playlist CSV files from `Data/` directory
2. Clean and standardize the data
3. Perform feature engineering
4. Output processed files to `Processed_Playlists/`

### Individual Components

**Fetch Genre Information:**
```bash
python FetchTrackGenre.py
```

**Fetch Genre and Popularity:**
```bash
python FetchTrackGenre_and_Popularity.py
```

**Explore Track Features:**
```bash
python TrackFeatures_Exploration.py
```

## Data Flow

1. **Input**: CSV files containing playlist track data in `Data/` directory
2. **Processing**:
   - Load and merge multiple playlist files
   - Clean data (handle missing values, standardize formats)
   - Enrich with Spotify API metadata (genres, popularity, audio features)
   - Engineer features (track categorization, playlist statistics)
3. **Output**: 
   - `final_cleaned_playlist_data.csv`: Complete processed dataset
   - `genre_counts.csv`: Genre distribution statistics
   - `merged_playlists_with_counts.csv`: Intermediate merged data

## Track Categorization

Tracks are automatically categorized based on playlist appearance frequency:

- **Unique Song**: Appears in only 1 playlist
- **Common Song**: Appears in 2-5 playlists
- **Popular Song**: Appears in 6+ playlists

## Audio Features

The pipeline extracts and analyzes Spotify's audio features:
- Danceability, Energy, Loudness
- Speechiness, Acousticness, Instrumentalness
- Liveness, Valence, Tempo
- Key, Mode, Time Signature

## Statistical Analysis

The project includes implementations of:
- Mann-Whitney U tests for non-parametric comparisons
- Genre diversity metrics
- Playlist structure analysis
- Track popularity correlations

## Research Applications

This codebase supports research in:
- Music recommendation systems
- Playlist generation algorithms
- Music consumption pattern analysis
- Genre classification and clustering
- Statistical modeling of music preferences

## Important Notes

- **API Rate Limits**: The Spotify API has rate limits. The code includes retry logic and timeout handling.
- **Data Size**: Processing large datasets may take significant time due to API calls.
- **Credentials**: Never commit Spotify credentials to version control.

## Contributing

1. Ensure all new features include appropriate error handling
2. Add unit tests for new functionality in `Tests/`
3. Update documentation for any API changes
4. Follow the existing code structure and naming conventions

## License

This project is for research and educational purposes. Please respect Spotify's API terms of service and the Million Playlist Dataset license terms.
