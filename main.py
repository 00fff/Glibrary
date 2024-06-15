from website.app import create_app
from website.apps.share_models import User, Game
from website.apps.cache_config import cache

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        all_users = User.query.all()
        for user in all_users:
            if user.owned_games:
                first_game_title = user.owned_games[0].game.title
            else:
                first_game_title = "No games owned"
            print(f"User ID: {user.user_id}, Username: {user.username}, Email: {user.email}, First Game: {first_game_title}")
    # Start the Flask application
    app.run(debug=True)
