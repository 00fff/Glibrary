from website.app import create_app
from website.apps.auth.models import User

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        all_users = User.query.all()
        """for user in all_users:
            print(f"User ID: {user.id}, Username: {user.username}, Email: {user.email}")"""
    # Start the Flask application
    app.run(debug=True)