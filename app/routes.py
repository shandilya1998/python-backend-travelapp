from app import app, db
from flask_login import current_user, login_user, login_required, logout_user
from app.models import users, place, itineraryItems
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
    session = Session()

    if request.args:
        counter = int(request.args.get("page"))  # The 'counter' value sent in the QS
        # The request in the front-end must send all the three parameters required here - 
        # page. city and filters
        # filters is a list of tags the user wants to see
        filters = str.split(requests.args.get('filters')) # list of all the filters to be applied for search
        if counter:
            quantity = int(requests.args.city.get('per_page'))
            p = session.query(place).filter(city = filters['city']).paginate(page = counter, per_page = quantity, error_out = True)
            print(f"Returning posts {counter} to {counter+quantity}")
            #p = pd.Series(p)
            # Slice 0 -> quantity from the db
            #res = make_response(logged_apply(p, jsonify), 200)
            res = make_response(jsonify(logged_apply(pd.Series(list(p)), serialize_ )), 200)
        elif counter == places:
            print("No more posts")
            res = make_response(jsonify({}), 200)
        else: 
            raise ValueError('Please enter valid page number : \'None\' type value found, when expecting an \'int\'')
    return res

def logged_apply(g, func, *args, **kwargs):
    """
        g - dataframe
        func - function to apply to the dataframe
        *args, **kwargs are the arguments to func
        The method applies the function to all the elements of the dataframe and shows progress
    """
    step_percentage = 100. / len(g)
    import sys
    sys.stdout.write('apply progress:   0%')
    sys.stdout.flush()

    def logging_decorator(func):
        def wrapper(*args, **kwargs):
            progress = wrapper.count * step_percentage
            sys.stdout.write('\033[D \033[D' * 4 + format(progress, '3.0f') + '%')
            sys.stdout.flush()
            wrapper.count += 1
            return func(*args, **kwargs)
        wrapper.count = 0
        return wrapper

    logged_func = logging_decorator(func)
    res = g.apply(logged_func, *args, **kwargs)
    sys.stdout.write('\033[D \033[D' * 4 + format(100., '3.0f') + '%' + '\n')
    sys.stdout.flush()
    return res

def serialize_(ob):
    """
        This function serializes each place object for sending to frontend
    """
    return ob.serialize()






"""
    References-
    https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
    https://pythonise.com/series/learning-flask/flask-query-strings
    https://scotch.io/bar-talk/processing-incoming-request-data-in-flask
    For more advanced features - https://exploreflask.com/en/latest/views.html
"""
