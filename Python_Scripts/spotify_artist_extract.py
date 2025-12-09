"""
artist_info.py
-----------------------
This script connects to the Spotify Web API using client credentials
to extract information about a list of artists. The data includes:
- Artist name
- Spotify ID
- External URL
- Follower count
- Popularity score
- Profile image URL

The script saves the results as an Excel file in the current directory.

Dependencies:
    - python-dotenv
    - requests
    - pandas
    - openpyxl

"""

# ---------------------------
# Imports
# ---------------------------
from dotenv import load_dotenv
import os
import base64
import requests
import pandas as pd

# ---------------------------
# Load Spotify credentials from .env
# ---------------------------
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

if not client_id or not client_secret:
    raise ValueError("Spotify CLIENT_ID and CLIENT_SECRET must be set in .env")

# ---------------------------
# get Spotify API token
# ---------------------------
def get_token():
    """
    Generates a Spotify API token using client credentials flow.

    Returns:
        str: Access token for Spotify API requests
    """
    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}

    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()["access_token"]

# ---------------------------
# fetch artist information
# ---------------------------
def get_artist_info(artist_name, headers):
    """
    Fetch artist metadata from Spotify API.

    Args:
        artist_name (str): Name of the artist to search
        headers (dict): Authorization headers with API token

    Returns:
        dict or None: Artist information dictionary, or None if not found
    """
    url = f"https://api.spotify.com/v1/search?q={artist_name}&type=artist&limit=1"
    response = requests.get(url, headers=headers)
    data = response.json()

    # Check if artist exists
    if data.get("artists", {}).get("items"):
        artist = data["artists"]["items"][0]
        return {
            "artist_name": artist["name"],
            "artist_id": artist["id"],
            "artist_url": artist["external_urls"]["spotify"],
            "artist_followers": artist["followers"]["total"],
            "artist_popularity": artist["popularity"],
            "artist_image_url": artist["images"][0]["url"] if artist["images"] else None,
        }
    else:
        print(f"No data found for {artist_name}")
        return None

# ---------------------------
# Main execution
# ---------------------------
if __name__ == "__main__":
    # Get API token and set headers
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    # List of artists to fetch
    artists = [
        "The Notorious B.I.G.",
        "Nas",
        "Mobb Deep",
        "Fat Joe",
        "Wu-Tang Clan",
        "Cam'ron",
        "Fabolous"
    ]

    all_data = []
    for artist in artists:
        print(f"Fetching data for {artist}...")
        info = get_artist_info(artist, headers)
        if info:
            all_data.append(info)

    # Save
    df = pd.DataFrame(all_data)
    output_file = "nyc_hiphop_artists_info.xlsx"
    df.to_excel(output_file, index=False)
    print(f"Data saved to {output_file}")

