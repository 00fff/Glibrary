from flask import Blueprint, render_template
from flask_login import login_required
views = Blueprint('views', __name__)
@views.route('/')
def home():
    return render_template('base.html')