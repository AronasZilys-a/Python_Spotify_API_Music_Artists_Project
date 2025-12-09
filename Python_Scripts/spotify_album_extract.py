"""
spotify_album_extract.py
------------------------
This script fetches all full albums for a list of Spotify artists.
It reads artist IDs from an existing Excel file, queries the Spotify API,
and outputs album metadata including:
- Artist name and ID
- Album name and type
- Release date
- Total tracks
- Spotify URL
- Album image URL

Dependencies:
    - python-dotenv
    - requests
    - pandas
    - openpyxl (for Excel export)
    
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

# ---------------------------
# Load Spotify credentials from .env
# ---------------------------
load_dotenv()
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

if not client_id or not client_secret:
    raise ValueError("Spotify CLIENT_ID and CLIENT_SECRET must be set in .env")

# ---------------------------
# get Spotify API token
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

    # Load existing artist list
    artist_df = pd.read_excel("nyc_hiphop_artists.xlsx")
    artist_ids = artist_df[['name', 'spotify_id']].to_dict('records')

    all_albums = []

    # Fetch albums for each artist
    for artist in artist_ids:
        artist_name = artist['name']
        artist_id = artist['spotify_id']
        print(f"Fetching albums for {artist_name}...")

        url = f"https://api.spotify.com/v1/artists/{artist_id}/albums?include_groups=album&limit=50"
        response = get(url, headers=headers)
        response.raise_for_status()  # Ensure API errors are caught
        data = response.json()

        # Extract relevant album information
        for album in data['items']:
            album_dict = {
                'artist_name': artist_name,
                'artist_id': artist_id,
                'album_name': album['name'],
                'album_type': album['album_type'],  # should always be "album"
                'release_date': album['release_date'],
                'total_tracks': album['total_tracks'],
                'spotify_url': album['external_urls']['spotify'],
                'image_url': album['images'][0]['url'] if album['images'] else None
            }
            all_albums.append(album_dict)

    # Convert to DataFrame and save as Excel
    df_albums = pd.DataFrame(all_albums)
    output_file = "nyc_hiphop_artist_albums.xlsx"
    df_albums.to_excel(output_file, index=False)
    print(f"Albums data saved to {output_file}")
