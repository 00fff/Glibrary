from flask import Flask, request, render_template
import requests
from website.apps.share_models import Game, User
from datetime import datetime, date
from website.apps.cache_config import cache
from website.database import db
from flask_mail import Message
from website.apps.mail import mail

CLIENT_ID = 'w69saddrm609bdexx1qv7k8334kspc'
CLIENT_SECRET = 'raegpu6z9tovkh7j92mch8mk7uf31t'

def get_access_token():
    auth_url = 'https://id.twitch.tv/oauth2/token'
    auth_params = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'client_credentials'
    }
    auth_response = requests.post(auth_url, params=auth_params)
    return auth_response.json()['access_token']

def get_cover(game_id, headers):
    endpoint = 'https://api.igdb.com/v4/covers'
    data = f'fields url; where id = {game_id};'
    response = requests.post(endpoint, headers=headers, data=data)
    covers = response.json()
    return covers 

def get_platform_name(platform_id, headers):
    endpoint = 'https://api.igdb.com/v4/platforms'
    data = f'fields name; where id = {platform_id};'
    response = requests.post(endpoint, headers=headers, data=data)
    platform_info = response.json()
    if platform_info:
        return platform_info[0]['name']
    else:
        return None

def get_creators(creator_id, headers):
    endpoint = 'https://api.igdb.com/v4/companies'
    access_token = get_access_token()
    headers = {
        'Client-ID': CLIENT_ID,
        'Authorization': f'Bearer {access_token}'
    }
    data = f'fields name; where id = {creator_id};'
    response = requests.post(endpoint, headers=headers, data=data)
    creator_info = response.json()
    if creator_info:
        return creator_info[0]['name']
    else:
        return "Company Could Not Be Found"

def get_genres(genre_id, headers):
    endpoint = 'https://api.igdb.com/v4/genres'
    data = f'fields name; where id = {genre_id};'
    response = requests.post(endpoint, headers=headers, data=data)
    genre_info = response.json()
    if genre_info:
        return genre_info[0]['name']
    else:
        return None

def get_game(query):
    access_token = get_access_token()
    headers = {
        'Client-ID': CLIENT_ID,
        'Authorization': f'Bearer {access_token}'
    }
    endpoint = 'https://api.igdb.com/v4/games'
    data = f'search "{query}"; fields name, summary, cover, platforms, genres, first_release_date, involved_companies, rating; limit 5;'
    response = requests.post(endpoint, headers=headers, data=data)
    game_info = response.json()

    if game_info:
        processed_games = []
        for game_data in game_info:
            platforms = game_data.get('platforms', [])
            platform_names = []
            for pid in platforms:
                platform_name = get_platform_name(pid, headers)
                platform_names.append(platform_name)
            
            cover_url = "https://upload.wikimedia.org/wikipedia/commons/0/06/Question-mark.jpg"
            cover_data = game_data.get('cover')
            if cover_data:
                cover_id = get_cover(cover_data, headers=headers)
                cover_url = cover_id[0]['url']
            
            formatted_date = None
            date_timestamp = game_data.get('first_release_date')
            if date_timestamp:
                formatted_date = datetime.utcfromtimestamp(date_timestamp).strftime('%Y-%m-%d')
            
            genres = game_data.get('genres', [])
            genre_names = []
            for genre_id in genres:
                genre_name = get_genres(genre_id, headers)
                genre_names.append(genre_name)
            
            rating = game_data.get('rating')
            if rating:
                rating = int(rating)
                
            involved_companies = game_data.get('involved_companies', [])
            companies = []
            for company_id in involved_companies:
                company_name = get_creators(company_id, headers)
                companies.append(company_name)
            
            game_data['genres'] = genre_names
            game_data['rating'] = rating
            game_data['platforms'] = platform_names
            game_data['cover'] = cover_url
            game_data['first_release_date'] = formatted_date
            game_data['involved_companies'] = companies
            
            processed_games.append(game_data)
            
            add_game_to_database(game_data)
        
        return processed_games
    else:
        return None

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
        return game_info
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None
default_cover_url = "https://upload.wikimedia.org/wikipedia/commons/0/06/Question-mark.jpg"

def add_game_to_database(game_data):
    """
    Add a new game to the database.

    Args:
        game_data (dict): Data of the game to be added.
    """
    check_game = Game.query.filter_by(title=game_data['name']).first()
    if check_game:
        return check_game
    release_date = None
    if 'first_release_date' in game_data and game_data['first_release_date']:
        # Convert the release date string to a Python date object
        release_date = datetime.strptime(game_data['first_release_date'], '%Y-%m-%d').date()
    description = game_data.get('summary', '')
    cover = game_data.get('cover', default_cover_url)  # Use default cover URL if cover data is not present
    new_game = Game(
        title=game_data['name'],
        description=description,
        art=cover,  # Assign the cover URL directly to the art attribute
        platform=', '.join(game_data['platforms']),
        genre=', '.join(game_data['genres']),
        release_date=release_date,
        developer=', '.join(game_data['involved_companies']),
        publisher=', '.join(game_data['involved_companies']),
        rating=int(game_data['rating']) if game_data['rating'] else None
    )
    db.session.add(new_game)
    db.session.commit()
