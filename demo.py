from requests import post, get
import json
from dotenv import load_dotenv
import base64
import os

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def main():
    # artist_name = input("What's the artist? ")
    token = get_token()
    # print(token)
    result = search_for_artist(token, "Seedhe maut")
    print(result)

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization" : "Basic " + auth_base64,
        "Content-Type" : "application/x-www-form-urlencoded"
    } 
    data = {"grant_type" : "client_credentials"}
    result = post(url, headers = headers, data = data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"q=remaster%2520artist%3A{artist_name}&type=album&limit=1"
    query_url = url + "?" + query
    params = {
    "q": f"artist:{artist_name}",
    "type": "artist",
    "limit": 1
    }

    result = get(url, headers=headers, params=params)
    result = get(query_url, headers= headers)
    json_result = result.json()["artists"]["items"]
    if len(json_result) == 0:
        print("No artist with name exists...")
        return None
    
    print(result.status_code)
    print(result.text)
    return json_result



if __name__ == "__main__":
    main()
