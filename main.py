from website import create_app
from website.apps.auth.models import User
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
    with app.app_context():
        all_users = User.query.all()
    # Print the data of each user
