from flask import Flask
from flask_restful import Resource, Api
from app import app, db
from flask_login import current_user, login_user, login_required, logout_user
from app.models import users, places, itineraryItems
from flask import redirect, url_for, flash, jsonify, request, session
from app.forms import LoginForm, RegistrationForm
from werkzeug.datastructures import MultiDict
import random
import json
from app.APICalls import APICalls

api = Api(app)

