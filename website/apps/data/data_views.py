from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .models import User
from website.database import db
from flask_restful import Api
dataB = Blueprint('auth', __name__, template_folder='templates/auth')
api = Api(dataB)