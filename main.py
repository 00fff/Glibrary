from website import create_app
from flask import current_app
from website.apps.cache_config import cache

# Initialize the Flask application
app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

# Note: No need to explicitly start the app with gunicorn when deploying to Heroku
# Heroku will use the command specified in Procfile to start the app with gunicorn
