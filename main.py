from website import create_app
from flask import current_app
from website.apps.cache_config import cache

# Initialize the Flask application
app = create_app()

if __name__ == "__main__":
    # Run the app using Flask's development server (only for local testing)
    app.run(debug=False)

# Note: No need to explicitly start the app with gunicorn when deploying to Heroku
# Heroku will use the command specified in Procfile to start the app with gunicorn
