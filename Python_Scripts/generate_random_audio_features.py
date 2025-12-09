"""
generate_random_audio_features.py
---------------------------------
This script generates random audio features for a list of tracks in an Excel file.
It is intended for testing, demonstration, or visualisation purposes when actual
Spotify audio features are not available.

Each track will have 8 features:
- danceability
- energy
- speechiness
- acousticness
- instrumentalness
- liveness
- valence
- tempo

Dependencies:
    - pandas
    - numpy
    - openpyxl (for Excel export)

"""

# ---------------------------
# Imports
# ---------------------------
import pandas as pd
import numpy as np

# ---------------------------
# Constants
# ---------------------------
INPUT_FILE = "merged_album_tracks_cleaned.xlsx"  # Input Excel file
OUTPUT_FILE = "audio_features_random.xlsx"       # Output Excel file

# List of 8 audio features
AUDIO_FEATURES = [
    "danceability", "energy", "speechiness",
    "acousticness", "instrumentalness", "liveness",
    "valence", "tempo"
]

# ---------------------------
# Main execution
# ---------------------------
if __name__ == "__main__":
    # Load the Excel file
    df = pd.read_excel(INPUT_FILE)

    # DataFrame with track URLs
    new_df = pd.DataFrame()
    new_df['track_url'] = df['track_url']  # Change to 'track_id' if preferred

    # Generate random values for each audio feature
    for feature in AUDIO_FEATURES:
        # Random decimals between 0 and 1, rounded to 1 decimal place
        new_df[feature] = np.round(np.random.rand(len(new_df)), 1)

    # Save to Excel
    new_df.to_excel(OUTPUT_FILE, index=False)
    print(f"New file '{OUTPUT_FILE}' created successfully with 1-decimal features!")
