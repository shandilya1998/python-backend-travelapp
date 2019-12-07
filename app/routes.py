from app import app, db
from flask_login import current_user, login_user, login_required, logout_user
from app.models import users, places, itineraryItems
from flask import redirect, url_for, flash, jsonify, request, session, Flask
from app.forms import LoginForm, RegistrationForm
from werkzeug.datastructures import MultiDict
import random
import json
from app.APICalls import APICalls


places = 100
quantity = 20

@app.route('/')
def index():
    return 'This is Sherpa, your travel guide'

@app.route("/load/", methods = ['GET'])
def load():
    """ Route to return the places """

    time.sleep(0.2)  # Used to simulate delay

    if request.args:
        counter = int(request.args.get("page"))  # The 'counter' value sent in the QS
        # The request in the front-end must send all the three parameters required here - 
        # page. city and filters
        # filters is a list of tags the user wants to see
        filters = str.split(requests.args.get('filters')) # list of all the filters to be applied for search
        if counter == 0:
            print(f"Returning posts 0 to {quantity}")
            # Slice 0 -> quantity from the db
            res = make_response(jsonify('demo response'), 200)

        elif counter == places:
            print("No more posts")
            res = make_response(jsonify({}), 200)

        else:
            print("Returning posts {counter} to {counter + quantity}")
            # Slice counter -> quantity from the db
            res = make_response(jsonify('demo response'), 200)

    return res

"""
    References-
    https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
    https://pythonise.com/series/learning-flask/flask-query-strings
    https://scotch.io/bar-talk/processing-incoming-request-data-in-flask
    For more advanced features - https://exploreflask.com/en/latest/views.html
"""
