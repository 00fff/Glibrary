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


def top_games():
    access_token = get_access_token()
    headers = {
        'Client-ID': CLIENT_ID,
        'Authorization': f'Bearer {access_token}'
    }
    endpoint = 'https://api.igdb.com/v4/games'
    data = f'search *; fields name, summary; where rating > 75; limit 50;'
    response = requests.post(endpoint, headers=headers, data=data)
    game_info = response.json()
    return game_info

