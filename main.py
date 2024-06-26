from website import create_app

# Initialize the Flask application
app = create_app()

if __name__ == "__main__":
    # Only run the development server when running locally
    app.run(host='0.0.0.0', port=5000)
