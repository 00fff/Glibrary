from main import app  # Import your Flask app instance
from website.database import db  # Import your SQLAlchemy instance

with app.app_context():
    # Drop all tables
    db.drop_all()
    # Recreate all tables
    db.create_all()
    print("Database has been reset.")