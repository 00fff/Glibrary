from flask import Flask, request, render_template
import requests
from website.apps.share_models import Game, User
CLIENT_ID = 'w69saddrm609bdexx1qv7k8334kspc'
CLIENT_SECRET = 'raegpu6z9tovkh7j92mch8mk7uf31t'
# 4qvty5aiyk34ca4vce500471ebd1ip
def get_access_token():
    auth_url = 'https://id.twitch.tv/oauth2/token'
    auth_params = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'client_credentials'
    }
    auth_response = requests.post(auth_url, params=auth_params)
    return auth_response.json()['access_token']

def get_game(query):
    access_token = get_access_token()
    headers = {
        'Client-ID': CLIENT_ID,
        'Authorization': f'Bearer {access_token}'
    }
    endpoint = 'https://api.igdb.com/v4/games'
    data = f'search "{query}"; fields name, summary;'
    response = requests.post(endpoint, headers=headers, data=data)
    game_info = response.json()
    print(game_info)
    if game_info:
        return game_info[0]  # Return the first 5
    else:
        return None  # Return None if no game is found

def get_cover(game_id, headers):
    access_token = get_access_token()
    headers = {
        'Client-ID': CLIENT_ID,
        'Authorization': f'Bearer {access_token}'
    }
    endpoint = 'https://api.igdb.com/v4/covers'
    data = f'fields url; where id = {game_id};'
    response = requests.post(endpoint, headers=headers, data=data)
    covers = response.json()
    return covers 

def top_games():
    access_token = get_access_token()
    headers = {
        'Client-ID': CLIENT_ID,
        'Authorization': f'Bearer {access_token}'
    }
    endpoint = 'https://api.igdb.com/v4/games'
    data = 'fields name, summary, rating; where rating >= 90; sort rating desc; limit 50;'
    response = requests.post(endpoint, headers=headers, data=data)
    if response.status_code == 200:
        game_info = response.json()
        for game in game_info:
            id = game["id"]
            # cover = get_cover(id, headers=headers)
            # return cover
        return game_info
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None