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
    endpoint = f"https://api.igdb.com/v4/platforms/{platform_id}"
    data = 'fields name;'
    response = requests.post(endpoint, headers=headers, data=data)
    if response.status_code == 200:
        platform_info = response.json()
        if platform_info and isinstance(platform_info, list) and 'name' in platform_info[0]:
            return platform_info[0]['name']
    return "Unknown"

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
    if genre_info and genre_info[0]:  # Check if genre_info is not empty and contains at least one element
        return genre_info[0]['name']
    else:
        return None
def get_game(query):
    query = query.lower()
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
            title = game_data.get('name')
            summary = game_data.get('summary')
            platforms = game_data.get('platforms', [])
            platform_names = []
            for pid in platforms:
                platform_name = get_platform_name(pid, headers)
                platform_names.append(platform_name)
            
            cover_url = "https://upload.wikimedia.org/wikipedia/commons/0/06/Question-mark.jpg"
            cover_data = game_data.get('cover')
            if cover_data:
                cover_id = get_cover(cover_data, headers=headers)
                cover_url = cover_id[0]['url'] # Use get method to handle potential missing 'url' key
                
            
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
            game_data['title'] = title
            game_data['description'] = summary
            game_data['genres'] = genre_names
            game_data['rating'] = rating
            game_data['platforms'] = platform_names
            game_data['art'] = cover_url
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
    data = 'fields name, summary, cover, platforms, genres, first_release_date, involved_companies, rating; where rating >= 90; sort rating desc; limit 50;'
    
    try:
        response = requests.post(endpoint, headers=headers, data=data)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        game_info = response.json()
        games = []
        
        for game in game_info:
            name = game.get('name')
            if name is not None:
                name = name.lower()
            else:
                continue
            
            
            # Check if the game exists in the database
            check_game = Game.query.filter_by(title=name).first()
            if check_game:
                # Append a dictionary representation of the check_game object
                
                check_game_data ={
                    'title': check_game.title,
                    'description': check_game.description,
                    'rating': check_game.rating,
                    'platforms': check_game.platform.split(', '),  # Assuming platforms is stored as a comma-separated string
                    'art': check_game.art,
                    'release_date': check_game.release_date,
                    'involved_companies': check_game.developer.split(', '),  # Assuming developer is stored as a comma-separated string
                    'genres': check_game.genre.split(', ')  # Assuming genre is stored as a comma-separated string
                }
                games.append(check_game_data)
            else:
                cover_url = "https://upload.wikimedia.org/wikipedia/commons/0/06/Question-mark.jpg"
                cover_data = game.get('cover')
                if cover_data:
                    cover_id = get_cover(cover_data, headers=headers)
                    cover_url = cover_id[0]['url'] # Use get method to handle potential missing 'url' key


                platforms = game.get('platforms', [])
                platform_names = []
                for pid in platforms:
                    platform_name = get_platform_name(pid, headers)
                    platform_names.append(platform_name)

                formatted_date = None
                date_timestamp = game.get('first_release_date')
                if date_timestamp:
                    formatted_date = datetime.utcfromtimestamp(date_timestamp).strftime('%Y-%m-%d')
                
                genres = game.get('genres', [])
                genre_names = []
                for genre_id in genres:
                    genre_name = get_genres(genre_id, headers)
                    genre_names.append(genre_name)

                rating = game.get('rating')
                rating = int(rating) if rating is not None else 0

                involved_companies = game.get('involved_companies', [])
                companies = []
                for company_id in involved_companies:
                    company_name = get_creators(company_id, headers)
                    companies.append(company_name)

                description = game.get('summary')

                new_game_data = {
                    'title': name,
                    'description': description,
                    'rating': rating,
                    'platforms': platform_names,
                    'art': cover_url,
                    'first_release_date': formatted_date,
                    'involved_companies': companies,
                    'genres': genre_names
                }
                games.append(new_game_data)
                add_game_to_database(new_game_data)
        return games
    
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return render_template("home.html", games=[])






def add_game_to_database(game_data):
    check_game = Game.query.filter_by(title=game_data['title']).first()
    if check_game:
        return check_game
    release_date = None
    if 'first_release_date' in game_data and game_data['first_release_date']:
        release_date = datetime.strptime(game_data['first_release_date'], '%Y-%m-%d').date()
    
    new_game = Game(
        title=game_data['title'],
        description=game_data['description'],  # Use get method with default value
        art=game_data['art'],
        platform=', '.join(game_data['platforms']),
        genre=', '.join(game_data['genres']),
        release_date=release_date,
        developer=', '.join(game_data['involved_companies']),
        publisher=', '.join(game_data['involved_companies']),
        rating=game_data['rating']
    )
    db.session.add(new_game)
    db.session.commit()
