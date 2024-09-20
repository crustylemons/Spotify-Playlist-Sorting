from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

# Retrieves client id and secret from the .env file
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# Gets the token from Spotify that allows me to do fun things with Spotify data
def get_token():
    # Packages the the id & secret to send it to the API for request
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    # Makes the API request
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    # Sends the API request
    result = post(url, headers=headers, data=data)

    # Turns the json into a python dictionary 
    json_result = json.loads(result.content)

    # Returns json result in 
    return json_result["access_token"]

# Gets a bearer token
# Tells the API: "I'm authorized because here's my token!"
def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


# Retrieves json data about an artist 
def search_for_artist(token, artist_name):
    
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token) # Proves I can access Spotify's data
    query = f"?q={artist_name}&type=artist&limit=1" # Searches for the artist, limiting to the first found

    # Send GET request to API
    result = get(url + query, headers=headers)

    # Turns json into python dictionary
    json_result = json.loads(result.content)["artists"]["items"]

    # Checks if there isn't a result by length of json result
    if len(json_result) == 0:
        print("No artists with this name exists...")
        return None
    
    return json_result[0]


# Retrieve a playlist
def get_my_playlist_id (token, playlist_name, username):
    url = f"https://api.spotify.com/v1/users/{username}/playlists"
    headers = get_auth_header(token) # Proves I can access Spotify's data

    # Send GET request to API
    result = get(url, headers=headers)

    # Turns json into python dictionary and puts the results in an array
    json_result = json.loads(result.content)
    playlists = json_result.get("items", [])

    # Checks if there are any playlist results
    if len(json_result) == 0:
        print("There are no playlists under this username.")
        return None
    

    for playlist in playlists:
        #print(playlist)
        if playlist['name'].lower() == playlist_name.lower():
            print(f"{playlist['name']} - getting id: ")
            return playlist['id']

    return "There are no playlists with this name"

# Retreives all playlists from a user
def get_all_playlists(token, username):
    url = f"https://api.spotify.com/v1/users/{username}/playlists"
    headers = get_auth_header(token) # Proves I can access Spotify's data

    # Send GET request to API
    result = get(url, headers=headers)

    # Turns json into python dictionary and puts the results in an array
    json_result = json.loads(result.content)
    playlists = json_result.get("items", [])
    
    for playlist in playlists:
        print(playlist['name'])


# Start calling functions here :
token = get_token()


get_all_playlists(token, "lilyh396113")