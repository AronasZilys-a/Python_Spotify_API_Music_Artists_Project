"""
spotify_track_extract.py
------------------------
This script fetches all tracks for a list of Spotify albums, including
track metadata and popularity scores. It reads album IDs from an existing
Excel file and outputs a complete track dataset.

Data collected per track:
- Artist name
- Album name
- Track name and number
- Duration (ms)
- Explicit flag
- Spotify URL
- Preview URL
- Popularity (0-100)

Dependencies:
    - python-dotenv
    - requests
    - pandas
    - openpyxl (for Excel export)

Usage:
    1. Ensure a `.env` file exists with:
        CLIENT_ID=your_spotify_client_id
        CLIENT_SECRET=your_spotify_client_secret
    2. Ensure `nyc_hiphop_artist_albums.xlsx` exists with the required columns.
    3. Run:
        python spotify_track_extract.py
"""

# ---------------------------
# Imports
# ---------------------------
from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import pandas as pd
import time

# ---------------------------
# Load Spotify credentials from .env
# ---------------------------
load_dotenv()
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

if not client_id or not client_secret:
    raise ValueError("Spotify CLIENT_ID and CLIENT_SECRET must be set in .env")

# ---------------------------
# Function to get Spotify API token
# ---------------------------
def get_token():
    """
    Generates a Spotify API token using the Client Credentials Flow.

    Returns:
        str: Access token for Spotify API requests
    """
    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')

    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + auth_base64,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {'grant_type': 'client_credentials'}

    result = post(url, headers=headers, data=data)
    result.raise_for_status()
    json_result = json.loads(result.content)
    return json_result['access_token']

# ---------------------------
# Main execution
# ---------------------------
if __name__ == "__main__":
    # Get API token and set headers
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    # Load album data from Excel
    albums_df = pd.read_excel("nyc_hiphop_artist_albums.xlsx")
    albums = albums_df[['artist_name', 'artist_id', 'album_name', 'spotify_url']].copy()
    # Extract album ID from Spotify URL
    albums['album_id'] = albums_df['spotify_url'].apply(lambda x: x.split('/')[-1])

    all_tracks = []

    # Fetch tracks for each album
    for _, album in albums.iterrows():
        album_id = album['album_id']
        artist_name = album['artist_name']
        album_name = album['album_name']
        print(f"Fetching tracks for album '{album_name}' by {artist_name}...")

        # Get album tracks
        url = f"https://api.spotify.com/v1/albums/{album_id}/tracks?limit=50"
        response = get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Fetch detailed info for each track (to get popularity)
        for track in data['items']:
            track_id = track['id']
            track_detail_url = f"https://api.spotify.com/v1/tracks/{track_id}"
            track_detail_response = get(track_detail_url, headers=headers)
            track_detail_response.raise_for_status()
            track_detail = track_detail_response.json()

            track_dict = {
                'artist_name': artist_name,
                'album_name': album_name,
                'track_name': track['name'],
                'track_number': track['track_number'],
                'duration_ms': track['duration_ms'],
                'explicit': track['explicit'],
                'spotify_url': track['external_urls']['spotify'],
                'preview_url': track['preview_url'],
                'popularity': track_detail.get('popularity')  # 0-100 score
            }
            all_tracks.append(track_dict)
            # Optional: small delay to respect API rate limits
            time.sleep(0.1)

    # Convert to DataFrame and save as Excel
    df_tracks = pd.DataFrame(all_tracks)
    output_file = "nyc_hiphop_album_tracks.xlsx"
    df_tracks.to_excel(output_file, index=False)
    print(f"Tracks data with popularity saved to {output_file}")
