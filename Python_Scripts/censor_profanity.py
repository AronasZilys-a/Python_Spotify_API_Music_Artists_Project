"""
censor_profanity.py
-------------------
This script cleans the 'track_name' column in a merged album-tracks Excel file
by censoring profanity using the 'better_profanity' library. It is intended for
cleaning track names before visualization or analysis.

Dependencies:
    - pandas
    - better_profanity
    - openpyxl (for Excel read/write)

Usage:
    1. Ensure the input Excel file exists with a 'track_name' column.
    2. Run:
        python clean_track_names.py
"""

# ---------------------------
# Imports
# ---------------------------
import pandas as pd
from better_profanity import profanity

# ---------------------------
# Constants
# ---------------------------
INPUT_FILE = "merged_album_tracks.xlsx"
OUTPUT_FILE = "merged_album_tracks_cleaned.xlsx"
COLUMN_TO_CLEAN = "track_name"

# ---------------------------
# Main execution
# ---------------------------
if __name__ == "__main__":
    # Read data
    df = pd.read_excel(INPUT_FILE)

    # Load the default profanity list
    profanity.load_censor_words()

    # Check if the target column exists
    if COLUMN_TO_CLEAN in df.columns:
        # Ensure all values are strings and censor profanity
        df[COLUMN_TO_CLEAN] = df[COLUMN_TO_CLEAN].astype(str).apply(lambda x: profanity.censor(x))
        print(f"Profanity filtered in '{COLUMN_TO_CLEAN}' column.")
    else:
        print(f"Column '{COLUMN_TO_CLEAN}' not found in Excel file!")

    # Save the cleaned dataset
    df.to_excel(OUTPUT_FILE, index=False)
    print(f"Cleaned dataset saved as: {OUTPUT_FILE}")
