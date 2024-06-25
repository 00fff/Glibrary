from website import create_app
from flask import current_app
from website.apps.cache_config import cache
app = create_app()

if __name__ == "__main__":
    with app.app_context():
        
    # Start the Flask application
        app.run(debug=True)
