from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import requests

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
    result = requests.get(url + query, headers=headers)

    if result.status_code == 200:
        # Turns json into python dictionary
        json_result = json.loads(result.text)["artists"]["items"]
        
        # Checks if there isn't a result by length of json result
        if len(json_result) == 0:
            print("No artists with this name exists...")
            return None
        
        return json_result[0]
    
    else:
        # Handle error responses
        print(f"Failed to get artist: {result.status_code} - {result.text}")
        return None

# Retreives all json data of playlists from a user
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

# Retrieve all json data of a playlist
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
            #print(f"{playlist['name']} - getting id: {playlist['id']}")
            return playlist['id']

    return "There are no playlists with this name"

# Retrieve all json data of tracks from a playlist
def get_all_tracks (token, playlist_name, username):
    playlist_id = get_my_playlist_id(token, playlist_name, username)
    
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = get_auth_header(token) # Proves I can access Spotify's data

    all_tracks = []

    # while loop that gets items 100 at a time
    while url: # While there's more songs to fetch
        # Send GET request to API
        result = get(url, headers=headers)

        # Check if the request was successful
        if result.status_code == 200:
            # Turns json into python dictionary
            json_result = json.loads(result.content)
                
            # Append the current batch of tracks to the all_tracks list
            all_tracks.extend(json_result['items'])

            url = json_result['next']

        else:
            print("unsuccessful retrevial")
            break

    
    #song_names = [item['track']['name'] for item in all_tracks]
    return all_tracks

# Create a new playlist
### DOESN'T WORK YET
def duplicate_playlist(token, playlist_name, new_playlist_name, username):
    #playlist_id = get_my_playlist_id(token, playlist_name, username)
    url = f"https://api.spotify.com/v1/users/{username}/playlists"
    headers = get_auth_header(token) # Proves I can access Spotify's data

    # Define the request body
    data = {
        "name": new_playlist_name,
        "description": f"Playlist created with API: {new_playlist_name}",
        "public": False
    }

    # Requests to make a new playlist to the API
    response = requests.post(url, headers=headers, json=data)

    # Check if the request was successful
    if response.status_code == 201:
        # Parse the JSON response
        playlist = response.json()
        print(f"Playlist '{playlist['name']}' created successfully!")
        print(playlist['items']['name'])
        return playlist  # Return the playlist data
    else:
        # Handle error responses
        print(f"Failed to create playlist: {response.status_code} - {response.text}")
        return None





# Sorts all songs from a playlist by seperating albums into a new playlist
def sort_playlist(token, playlist_name, username, new_playlist_name):
    # gets all playlist tracks
    playlist_tracks = get_all_tracks(token, playlist_name, username)
    
    # create a new playlist called new_playlist_name
    ####

    # for each track on playlist_name
        # add to playlist new_playlist_name
    # for each track on playlist_name, starting on track 2, 
        # if the previous song's album = current song's album
            # create max_random_num = 10
            # if playlist length is less than 10,
                # set max_random_num to the playlist length
            # generate a random number from 2 - max_random_num
            # put the track at that spot in the playlist
    
    # print out: new_playlist_name + " has been created!"
    

# Start calling functions here :
token = get_token()
username = "lilyh396113"


#get_all_playlists(token, "lilyh396113")
#get_all_tracks(token, "Adamant_Ashley‘s Main Playlist", "lilyh396113")
#duplicate_playlist(token, "Adamant_Ashley‘s Main Playlist", "new playlist", username)
search_for_artist(token, "Taylor Swift")