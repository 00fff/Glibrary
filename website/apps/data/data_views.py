from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from website.database import db
from flask_restful import Api

data = Blueprint('data', __name__, template_folder='templates/data')
api = Api(data)

@data.route('/search', methods=["POST", "GET"])
def search():
    if request.method == "POST":
        # Handle the POST request
        message = request.form.get('search_query')
        return render_template('search.html', message=message)
    else:
        # Handle the GET request
        return render_template('search.html')
