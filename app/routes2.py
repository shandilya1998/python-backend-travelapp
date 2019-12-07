from app import app, db
from flask_login import current_user, login_user, login_required, logout_user
from app.models import users, places, itineraryItems
from flask import redirect, url_for, flash, jsonify, request, session
from app.forms import LoginForm, RegistrationForm
from werkzeug.datastructures import MultiDict
import random 
import json
from app.APICalls import APICalls

# @app.route('/user/<username>')

# @login_required #to be figured out later
"""
Notes : -
The app performs the following functions-
    # Receives requests from the front end, evoking necessary functions to obtain outputs
     and sending the appriate response
"""

@app.route('/xyz')
def home_():
    return 'This is the home of travelapp'
@app.route('/',
           methods=['POST'])
# the second URL will also lead to the same response
@app.route('/home',
           methods=['POST'])
# Protects a view function against anonymous users
def home():
    # Serves as the entry page to the app will be the first page the user lands on
    # This will create the session and will also help for passwordless login, but this will be implemented later
    # check on 127.0.0.1:5000 or https://localhost:5000 four response on a browser
    data = request.get_json()
    print(data)
    session['user'] = data['username']
    session['initiation_page'] = 0
    session.save_session()
    return 'Let us start plan the next trip'


@app.route('/PlacesDirectory/card_data/<int:idplaces>',
           methods=['GET'])
@login_required
def get_card_data(idplaces):
    # returns all place data to front end card component
    place = places.query.filter_by(idplaces=idplaces).first_or_404()
    data = {'placeName': place.name,
            'city': place.city,
            'closingTime': place.closingTime,
            'openingTime': place.opeingTime,
            'stayTime': place.stayTime,
            'history': place.history,
            'descriptionShort': place.descriptionShort,
            'descriptionLong': place.descriptionLong,
            'address': place.address,
            'phoneNum': place.phoneNum}  # fill all information as is required
    return jsonify(data)


@app.route('/login',
           methods=['POST'])
def login():
    # login not functioning correctly fix later
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    # WTForms can take multidict as input.
    # The json data in the request is to be converted into a MultiDict to populate the form in the backend
    # The information json is then used to validate against the data in the table users
    data = MultiDict(request.get_json())
    form = LoginForm(data,
                     csrf_enabled=False)
    print(form)
    if form.validate_on_submit():
        print('validated')
        user = users.query.filter_by(username=form.username.data).first()
        print(user)
        if user is None or not user.check_password(form.password.data):
            print('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user,
                   remember=form.remember_me.data)
        return redirect(url_for('home'))
    # find out what to return from the final return here
    # currently the input json is being returned here
    return jsonify({'output': 'log in here',
                    'username': form.username.data,
                    'password': form.password.data,
                    'remember_me': form.remember_me.data})


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/register',
           methods=['POST'])
def register():
    # This function processed user input from the user registration form
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    print('executed')
    data = MultiDict(request.get_json())
    form = RegistrationForm(data, csrf_enabled=False)
    print(form.data)
    if form.validate_on_submit():
        print('validated')
        user = users(username=form.username.data,
                     email=form.email.data)
        user.set_password(
            form.password.data)  # set_password() generates a hash that is stored. This improveds security of user data
        db.session.add(user)
        db.session.commit()
        flash('Congratulation, you are a new user')
        return redirect(url_for('login'))
    print(form.errors)
    return 'Successfully Registered' + ' ' + form.username.data + ' ' + form.email.data

@app.route('/profile/<int:idusers>',
           methods=['GET'])
def get_profile_page(idusers):
    # Returns a response to a request for profile page data
    user = users.query.filter_by(idusers=idusers).first_or_404()
    userprofiletags = user.userProfileTags
    print(userprofiletags)
    # Add other information to be sent with too like trips taken and number of trips takes
    data = {'username': user.username,
            'numTripsTaken': user.numTripsTaken,
            'email': user.email,
            'profileTags': userprofiletags}
    return jsonify(data)

@app.route('/add_to_itinerary',
           methods = ['POST'])
@login_required
def add_to_itinerary():
    # authentication of session here when session is implemented
    data = request.get_json()
    user_id = data.user_d
    session_id = data.session_id
    place_id = data.place_id
    itineraryItems.add_to_itinerary(place_id,
                   session_id, #Needs implementaion of session
                   user_id)

@app.route('/getPlace', methods = ['GET'])
def getPlace():
#need to create a function that can send places to the frontend based on the city
#this function will take a paramater called city and the search parameters that the user has defined in settings
#Need to create a function that will shuffle places according to user information
#the shuffling will be initially based on the decision tree that has been created by yash and ruturaj
#currently the function returns a random place from db
    places_list = places.query.all()
    length = len(places_list)
    place_index = random.randint(0,length-1)
    place = places_list[place_index]
    place_id = place.place_id
    place_name = place.name
    #place_descriptionShort = place.descriptionShort
    place_photo = json.loads(place.photo)
    photo_reference_list = ''
    for photo_data in place_photo:
        photo_reference_list = photo_reference_list+',' + photo_data['photo_reference']
    photo_reference_list = photo_reference_list.strip(',')
    response = {'place_id' : place_id,
                'name' : place_name,
                'description' : 'this is a short description of the place in question',
                'photo' : photo_reference_list}
    print(response)
    return json.dumps(response)

@app.route('/getPlacesFirstTime', methods = ['GET'])
def getPlacesFirstTime():
    response =[{'place_id' : 'ChIJ4zGFAZpYwokRGUGph3Mf37k',
                 'name' : 'Central Park',		      
		         'description' : 'New York\'s escape from New York',
		         'photo' : "CmRaAAAAhdTR_SOFlHjhRT7b4dGnMTnHoLqkPJKdiAgXNidCWMB1BP5I0GBzHyQGBjApDqS0VN_jZuwtumnCjorBqNnRQpbh12fNoEGMZsJuRQA8XAO2XxlgngkrPY1KqeL0qTpJEhDWuxsc7J_RpvuuzZk-EgtXGhQjNvko-QguCiSLC5uNnBrurEvUQw,CmRaAAAASO5zwGAJm49FhxObdJlnoAMVlDWYq0QtwqAMEPdzYsChsBYpdoHMFgP0yWFCaLSOwJNcGaAd-ZlW8gBvz_8mKrUzoTwgyUBHUDCsMf_byCXO3n6Rdp_C3sA8tE_OF56rEhCBY52QnnUwYf5TWtftyyTWGhRm6cWKwDeGt5fMUPl5qKEqrq70Nw,CmRaAAAAU6sV_qgin7ivsYM84h-vZEKqo-9CX7F2m6QtqNX26FNxS4g-NPT4hRdJ_ymgNlzXF0nRinqhlKRYYjt_DVY0X6VUt9IneL4AHHgLKtnO_-YShlGBr8IaQFvhEOVsJGakEhAgBuGkecz3fDrWtY8dDm6yGhTR0fFzdu5hrDtYNAaxHz5-R504AA,CmRaAAAAZOvyXjFYhYTqPAN4-QYQjaXy3Z13Ty6skESZiCZDkYSn3BnFnlHTrqxMFBmTXaEWaxbLDKV2TDysBxGJ3rw4ra_NgUOJZ9fM-Q-D36ZMy8tUFTRZ5_sqt5zkFWLM7v1JEhA2E5opbJQhzlkOa8WooH0mGhR-gq_gfos548ip4LNIb5LLqNRuQg,CmRaAAAA5WkoP9Zw5WOyIXIoZIldGIeOFGkTy8j3EPGBWF0QJiJ3Y22MLrn4Mwyb6iFZuAHQQrBzIFObZ3-QeyIDnn0Ayq0m9Rlf0qS9h0eoqnPQnDFpyRZDLuxMJupJGpJDOKtxEhA8aMh-ID92psG5Xku6rldyGhTqM190NLECoDZdgeAy8LVEkSQzug,CmRaAAAAGh_KfDYZ0WFYXv1nFkusfmnyjbGXYmBQbL8VgrlGpWin6VmXQZt7OdBM40aQ-FUe-JBgrMI2QATummI3uAChs-gvs-QyC4kwcDQtGW0ONftetDad57l0r3HVbJPFpGUnEhAVMoALU8kjerh5xW73o7UbGhTIqFmyM1ATvx5nUkmF5qPDBhb1yA"},
                {
	    	     'place_id' : 'ChIJPTacEpBQwokRKwIlDXelxkA',
		         'name' : 'Statue of Liberty National Monument',	
		         'description' : 'A figure of Libertas, a robed Roman liberty goddess',
		         'photo' : "CmRaAAAAhdTR_SOFlHjhRT7b4dGnMTnHoLqkPJKdiAgXNidCWMB1BP5I0GBzHyQGBjApDqS0VN_jZuwtumnCjorBqNnRQpbh12fNoEGMZsJuRQA8XAO2XxlgngkrPY1KqeL0qTpJEhDWuxsc7J_RpvuuzZk-EgtXGhQjNvko-QguCiSLC5uNnBrurEvUQw,CmRaAAAASO5zwGAJm49FhxObdJlnoAMVlDWYq0QtwqAMEPdzYsChsBYpdoHMFgP0yWFCaLSOwJNcGaAd-ZlW8gBvz_8mKrUzoTwgyUBHUDCsMf_byCXO3n6Rdp_C3sA8tE_OF56rEhCBY52QnnUwYf5TWtftyyTWGhRm6cWKwDeGt5fMUPl5qKEqrq70Nw,CmRaAAAAU6sV_qgin7ivsYM84h-vZEKqo-9CX7F2m6QtqNX26FNxS4g-NPT4hRdJ_ymgNlzXF0nRinqhlKRYYjt_DVY0X6VUt9IneL4AHHgLKtnO_-YShlGBr8IaQFvhEOVsJGakEhAgBuGkecz3fDrWtY8dDm6yGhTR0fFzdu5hrDtYNAaxHz5-R504AA,CmRaAAAAZOvyXjFYhYTqPAN4-QYQjaXy3Z13Ty6skESZiCZDkYSn3BnFnlHTrqxMFBmTXaEWaxbLDKV2TDysBxGJ3rw4ra_NgUOJZ9fM-Q-D36ZMy8tUFTRZ5_sqt5zkFWLM7v1JEhA2E5opbJQhzlkOa8WooH0mGhR-gq_gfos548ip4LNIb5LLqNRuQg,CmRaAAAA5WkoP9Zw5WOyIXIoZIldGIeOFGkTy8j3EPGBWF0QJiJ3Y22MLrn4Mwyb6iFZuAHQQrBzIFObZ3-QeyIDnn0Ayq0m9Rlf0qS9h0eoqnPQnDFpyRZDLuxMJupJGpJDOKtxEhA8aMh-ID92psG5Xku6rldyGhTqM190NLECoDZdgeAy8LVEkSQzug,CmRaAAAAGh_KfDYZ0WFYXv1nFkusfmnyjbGXYmBQbL8VgrlGpWin6VmXQZt7OdBM40aQ-FUe-JBgrMI2QATummI3uAChs-gvs-QyC4kwcDQtGW0ONftetDad57l0r3HVbJPFpGUnEhAVMoALU8kjerh5xW73o7UbGhTIqFmyM1ATvx5nUkmF5qPDBhb1yA"},	       
	            {
		         'place_id' : 'ChIJ9U1mz_5YwokRosza1aAk0jM',
		         'name' : 'Rockefeller Center',
		         'description' : 'A large complex Midtown Manhattan, New York City',
		         'photo' : "CmRaAAAAhdTR_SOFlHjhRT7b4dGnMTnHoLqkPJKdiAgXNidCWMB1BP5I0GBzHyQGBjApDqS0VN_jZuwtumnCjorBqNnRQpbh12fNoEGMZsJuRQA8XAO2XxlgngkrPY1KqeL0qTpJEhDWuxsc7J_RpvuuzZk-EgtXGhQjNvko-QguCiSLC5uNnBrurEvUQw,CmRaAAAASO5zwGAJm49FhxObdJlnoAMVlDWYq0QtwqAMEPdzYsChsBYpdoHMFgP0yWFCaLSOwJNcGaAd-ZlW8gBvz_8mKrUzoTwgyUBHUDCsMf_byCXO3n6Rdp_C3sA8tE_OF56rEhCBY52QnnUwYf5TWtftyyTWGhRm6cWKwDeGt5fMUPl5qKEqrq70Nw,CmRaAAAAU6sV_qgin7ivsYM84h-vZEKqo-9CX7F2m6QtqNX26FNxS4g-NPT4hRdJ_ymgNlzXF0nRinqhlKRYYjt_DVY0X6VUt9IneL4AHHgLKtnO_-YShlGBr8IaQFvhEOVsJGakEhAgBuGkecz3fDrWtY8dDm6yGhTR0fFzdu5hrDtYNAaxHz5-R504AA,CmRaAAAAZOvyXjFYhYTqPAN4-QYQjaXy3Z13Ty6skESZiCZDkYSn3BnFnlHTrqxMFBmTXaEWaxbLDKV2TDysBxGJ3rw4ra_NgUOJZ9fM-Q-D36ZMy8tUFTRZ5_sqt5zkFWLM7v1JEhA2E5opbJQhzlkOa8WooH0mGhR-gq_gfos548ip4LNIb5LLqNRuQg,CmRaAAAA5WkoP9Zw5WOyIXIoZIldGIeOFGkTy8j3EPGBWF0QJiJ3Y22MLrn4Mwyb6iFZuAHQQrBzIFObZ3-QeyIDnn0Ayq0m9Rlf0qS9h0eoqnPQnDFpyRZDLuxMJupJGpJDOKtxEhA8aMh-ID92psG5Xku6rldyGhTqM190NLECoDZdgeAy8LVEkSQzug,CmRaAAAAGh_KfDYZ0WFYXv1nFkusfmnyjbGXYmBQbL8VgrlGpWin6VmXQZt7OdBM40aQ-FUe-JBgrMI2QATummI3uAChs-gvs-QyC4kwcDQtGW0ONftetDad57l0r3HVbJPFpGUnEhAVMoALU8kjerh5xW73o7UbGhTIqFmyM1ATvx5nUkmF5qPDBhb1yA"},
                {'place_id' : 'ChIJ5_UX8spdwokRawVDXyCCxk0',
                 'name' : 'Dawn of Glory',
                 'description' : 'this is a short description of the place in question',
                 'photo' : "CmRaAAAAhdTR_SOFlHjhRT7b4dGnMTnHoLqkPJKdiAgXNidCWMB1BP5I0GBzHyQGBjApDqS0VN_jZuwtumnCjorBqNnRQpbh12fNoEGMZsJuRQA8XAO2XxlgngkrPY1KqeL0qTpJEhDWuxsc7J_RpvuuzZk-EgtXGhQjNvko-QguCiSLC5uNnBrurEvUQw,CmRaAAAASO5zwGAJm49FhxObdJlnoAMVlDWYq0QtwqAMEPdzYsChsBYpdoHMFgP0yWFCaLSOwJNcGaAd-ZlW8gBvz_8mKrUzoTwgyUBHUDCsMf_byCXO3n6Rdp_C3sA8tE_OF56rEhCBY52QnnUwYf5TWtftyyTWGhRm6cWKwDeGt5fMUPl5qKEqrq70Nw,CmRaAAAAU6sV_qgin7ivsYM84h-vZEKqo-9CX7F2m6QtqNX26FNxS4g-NPT4hRdJ_ymgNlzXF0nRinqhlKRYYjt_DVY0X6VUt9IneL4AHHgLKtnO_-YShlGBr8IaQFvhEOVsJGakEhAgBuGkecz3fDrWtY8dDm6yGhTR0fFzdu5hrDtYNAaxHz5-R504AA,CmRaAAAAZOvyXjFYhYTqPAN4-QYQjaXy3Z13Ty6skESZiCZDkYSn3BnFnlHTrqxMFBmTXaEWaxbLDKV2TDysBxGJ3rw4ra_NgUOJZ9fM-Q-D36ZMy8tUFTRZ5_sqt5zkFWLM7v1JEhA2E5opbJQhzlkOa8WooH0mGhR-gq_gfos548ip4LNIb5LLqNRuQg,CmRaAAAA5WkoP9Zw5WOyIXIoZIldGIeOFGkTy8j3EPGBWF0QJiJ3Y22MLrn4Mwyb6iFZuAHQQrBzIFObZ3-QeyIDnn0Ayq0m9Rlf0qS9h0eoqnPQnDFpyRZDLuxMJupJGpJDOKtxEhA8aMh-ID92psG5Xku6rldyGhTqM190NLECoDZdgeAy8LVEkSQzug,CmRaAAAAGh_KfDYZ0WFYXv1nFkusfmnyjbGXYmBQbL8VgrlGpWin6VmXQZt7OdBM40aQ-FUe-JBgrMI2QATummI3uAChs-gvs-QyC4kwcDQtGW0ONftetDad57l0r3HVbJPFpGUnEhAVMoALU8kjerh5xW73o7UbGhTIqFmyM1ATvx5nUkmF5qPDBhb1yA"},
                {'place_id' : 'ChIJTwGkpIFYwokRf5k4y-SDUfg',
                 'name' : 'Soldiers’ and Sailors’ Monument',
                 'description' : 'this is a short description of the place in question',
                 'photo' : "CmRaAAAAhdTR_SOFlHjhRT7b4dGnMTnHoLqkPJKdiAgXNidCWMB1BP5I0GBzHyQGBjApDqS0VN_jZuwtumnCjorBqNnRQpbh12fNoEGMZsJuRQA8XAO2XxlgngkrPY1KqeL0qTpJEhDWuxsc7J_RpvuuzZk-EgtXGhQjNvko-QguCiSLC5uNnBrurEvUQw,CmRaAAAASO5zwGAJm49FhxObdJlnoAMVlDWYq0QtwqAMEPdzYsChsBYpdoHMFgP0yWFCaLSOwJNcGaAd-ZlW8gBvz_8mKrUzoTwgyUBHUDCsMf_byCXO3n6Rdp_C3sA8tE_OF56rEhCBY52QnnUwYf5TWtftyyTWGhRm6cWKwDeGt5fMUPl5qKEqrq70Nw,CmRaAAAAU6sV_qgin7ivsYM84h-vZEKqo-9CX7F2m6QtqNX26FNxS4g-NPT4hRdJ_ymgNlzXF0nRinqhlKRYYjt_DVY0X6VUt9IneL4AHHgLKtnO_-YShlGBr8IaQFvhEOVsJGakEhAgBuGkecz3fDrWtY8dDm6yGhTR0fFzdu5hrDtYNAaxHz5-R504AA,CmRaAAAAZOvyXjFYhYTqPAN4-QYQjaXy3Z13Ty6skESZiCZDkYSn3BnFnlHTrqxMFBmTXaEWaxbLDKV2TDysBxGJ3rw4ra_NgUOJZ9fM-Q-D36ZMy8tUFTRZ5_sqt5zkFWLM7v1JEhA2E5opbJQhzlkOa8WooH0mGhR-gq_gfos548ip4LNIb5LLqNRuQg,CmRaAAAA5WkoP9Zw5WOyIXIoZIldGIeOFGkTy8j3EPGBWF0QJiJ3Y22MLrn4Mwyb6iFZuAHQQrBzIFObZ3-QeyIDnn0Ayq0m9Rlf0qS9h0eoqnPQnDFpyRZDLuxMJupJGpJDOKtxEhA8aMh-ID92psG5Xku6rldyGhTqM190NLECoDZdgeAy8LVEkSQzug,CmRaAAAAGh_KfDYZ0WFYXv1nFkusfmnyjbGXYmBQbL8VgrlGpWin6VmXQZt7OdBM40aQ-FUe-JBgrMI2QATummI3uAChs-gvs-QyC4kwcDQtGW0ONftetDad57l0r3HVbJPFpGUnEhAVMoALU8kjerh5xW73o7UbGhTIqFmyM1ATvx5nUkmF5qPDBhb1yA"},
                {'place_id' : 'ChIJW1Ftu3_ywokRDiPPhPTsOZY',
                 'name' : 'War Memorial Field',
                 'description' : 'this is a short description of the place in question',
                 'photo' : "CmRaAAAAhdTR_SOFlHjhRT7b4dGnMTnHoLqkPJKdiAgXNidCWMB1BP5I0GBzHyQGBjApDqS0VN_jZuwtumnCjorBqNnRQpbh12fNoEGMZsJuRQA8XAO2XxlgngkrPY1KqeL0qTpJEhDWuxsc7J_RpvuuzZk-EgtXGhQjNvko-QguCiSLC5uNnBrurEvUQw,CmRaAAAASO5zwGAJm49FhxObdJlnoAMVlDWYq0QtwqAMEPdzYsChsBYpdoHMFgP0yWFCaLSOwJNcGaAd-ZlW8gBvz_8mKrUzoTwgyUBHUDCsMf_byCXO3n6Rdp_C3sA8tE_OF56rEhCBY52QnnUwYf5TWtftyyTWGhRm6cWKwDeGt5fMUPl5qKEqrq70Nw,CmRaAAAAU6sV_qgin7ivsYM84h-vZEKqo-9CX7F2m6QtqNX26FNxS4g-NPT4hRdJ_ymgNlzXF0nRinqhlKRYYjt_DVY0X6VUt9IneL4AHHgLKtnO_-YShlGBr8IaQFvhEOVsJGakEhAgBuGkecz3fDrWtY8dDm6yGhTR0fFzdu5hrDtYNAaxHz5-R504AA,CmRaAAAAZOvyXjFYhYTqPAN4-QYQjaXy3Z13Ty6skESZiCZDkYSn3BnFnlHTrqxMFBmTXaEWaxbLDKV2TDysBxGJ3rw4ra_NgUOJZ9fM-Q-D36ZMy8tUFTRZ5_sqt5zkFWLM7v1JEhA2E5opbJQhzlkOa8WooH0mGhR-gq_gfos548ip4LNIb5LLqNRuQg,CmRaAAAA5WkoP9Zw5WOyIXIoZIldGIeOFGkTy8j3EPGBWF0QJiJ3Y22MLrn4Mwyb6iFZuAHQQrBzIFObZ3-QeyIDnn0Ayq0m9Rlf0qS9h0eoqnPQnDFpyRZDLuxMJupJGpJDOKtxEhA8aMh-ID92psG5Xku6rldyGhTqM190NLECoDZdgeAy8LVEkSQzug,CmRaAAAAGh_KfDYZ0WFYXv1nFkusfmnyjbGXYmBQbL8VgrlGpWin6VmXQZt7OdBM40aQ-FUe-JBgrMI2QATummI3uAChs-gvs-QyC4kwcDQtGW0ONftetDad57l0r3HVbJPFpGUnEhAVMoALU8kjerh5xW73o7UbGhTIqFmyM1ATvx5nUkmF5qPDBhb1yA"},
                {'place_id' : 'ChIJG58WIRRbwokR7dpKH0kIX6Q',
                 'name' : 'Prospect Park War Memorial',
                 'description' : 'this is a short description of the place in question',
                 'photo' : "CmRaAAAAhdTR_SOFlHjhRT7b4dGnMTnHoLqkPJKdiAgXNidCWMB1BP5I0GBzHyQGBjApDqS0VN_jZuwtumnCjorBqNnRQpbh12fNoEGMZsJuRQA8XAO2XxlgngkrPY1KqeL0qTpJEhDWuxsc7J_RpvuuzZk-EgtXGhQjNvko-QguCiSLC5uNnBrurEvUQw,CmRaAAAASO5zwGAJm49FhxObdJlnoAMVlDWYq0QtwqAMEPdzYsChsBYpdoHMFgP0yWFCaLSOwJNcGaAd-ZlW8gBvz_8mKrUzoTwgyUBHUDCsMf_byCXO3n6Rdp_C3sA8tE_OF56rEhCBY52QnnUwYf5TWtftyyTWGhRm6cWKwDeGt5fMUPl5qKEqrq70Nw,CmRaAAAAU6sV_qgin7ivsYM84h-vZEKqo-9CX7F2m6QtqNX26FNxS4g-NPT4hRdJ_ymgNlzXF0nRinqhlKRYYjt_DVY0X6VUt9IneL4AHHgLKtnO_-YShlGBr8IaQFvhEOVsJGakEhAgBuGkecz3fDrWtY8dDm6yGhTR0fFzdu5hrDtYNAaxHz5-R504AA,CmRaAAAAZOvyXjFYhYTqPAN4-QYQjaXy3Z13Ty6skESZiCZDkYSn3BnFnlHTrqxMFBmTXaEWaxbLDKV2TDysBxGJ3rw4ra_NgUOJZ9fM-Q-D36ZMy8tUFTRZ5_sqt5zkFWLM7v1JEhA2E5opbJQhzlkOa8WooH0mGhR-gq_gfos548ip4LNIb5LLqNRuQg,CmRaAAAA5WkoP9Zw5WOyIXIoZIldGIeOFGkTy8j3EPGBWF0QJiJ3Y22MLrn4Mwyb6iFZuAHQQrBzIFObZ3-QeyIDnn0Ayq0m9Rlf0qS9h0eoqnPQnDFpyRZDLuxMJupJGpJDOKtxEhA8aMh-ID92psG5Xku6rldyGhTqM190NLECoDZdgeAy8LVEkSQzug,CmRaAAAAGh_KfDYZ0WFYXv1nFkusfmnyjbGXYmBQbL8VgrlGpWin6VmXQZt7OdBM40aQ-FUe-JBgrMI2QATummI3uAChs-gvs-QyC4kwcDQtGW0ONftetDad57l0r3HVbJPFpGUnEhAVMoALU8kjerh5xW73o7UbGhTIqFmyM1ATvx5nUkmF5qPDBhb1yA"},
                {'place_id' : 'ChIJediv5RJawokRmMf13KiefBY',
                 'name' : 'East Coast Memorial',
                 'description' : 'this is a short description of the place in question',
                 'photo' : "CmRaAAAAhdTR_SOFlHjhRT7b4dGnMTnHoLqkPJKdiAgXNidCWMB1BP5I0GBzHyQGBjApDqS0VN_jZuwtumnCjorBqNnRQpbh12fNoEGMZsJuRQA8XAO2XxlgngkrPY1KqeL0qTpJEhDWuxsc7J_RpvuuzZk-EgtXGhQjNvko-QguCiSLC5uNnBrurEvUQw,CmRaAAAASO5zwGAJm49FhxObdJlnoAMVlDWYq0QtwqAMEPdzYsChsBYpdoHMFgP0yWFCaLSOwJNcGaAd-ZlW8gBvz_8mKrUzoTwgyUBHUDCsMf_byCXO3n6Rdp_C3sA8tE_OF56rEhCBY52QnnUwYf5TWtftyyTWGhRm6cWKwDeGt5fMUPl5qKEqrq70Nw,CmRaAAAAU6sV_qgin7ivsYM84h-vZEKqo-9CX7F2m6QtqNX26FNxS4g-NPT4hRdJ_ymgNlzXF0nRinqhlKRYYjt_DVY0X6VUt9IneL4AHHgLKtnO_-YShlGBr8IaQFvhEOVsJGakEhAgBuGkecz3fDrWtY8dDm6yGhTR0fFzdu5hrDtYNAaxHz5-R504AA,CmRaAAAAZOvyXjFYhYTqPAN4-QYQjaXy3Z13Ty6skESZiCZDkYSn3BnFnlHTrqxMFBmTXaEWaxbLDKV2TDysBxGJ3rw4ra_NgUOJZ9fM-Q-D36ZMy8tUFTRZ5_sqt5zkFWLM7v1JEhA2E5opbJQhzlkOa8WooH0mGhR-gq_gfos548ip4LNIb5LLqNRuQg,CmRaAAAA5WkoP9Zw5WOyIXIoZIldGIeOFGkTy8j3EPGBWF0QJiJ3Y22MLrn4Mwyb6iFZuAHQQrBzIFObZ3-QeyIDnn0Ayq0m9Rlf0qS9h0eoqnPQnDFpyRZDLuxMJupJGpJDOKtxEhA8aMh-ID92psG5Xku6rldyGhTqM190NLECoDZdgeAy8LVEkSQzug,CmRaAAAAGh_KfDYZ0WFYXv1nFkusfmnyjbGXYmBQbL8VgrlGpWin6VmXQZt7OdBM40aQ-FUe-JBgrMI2QATummI3uAChs-gvs-QyC4kwcDQtGW0ONftetDad57l0r3HVbJPFpGUnEhAVMoALU8kjerh5xW73o7UbGhTIqFmyM1ATvx5nUkmF5qPDBhb1yA"},
                {'place_id' : 'ChIJVXMEQzZawokRsbjWS6ekTwc ',
                 'name' : 'Brooklyn War Memorial',
                 'description' : 'this is a short description of the place in question',
                 'photo' : "CmRaAAAAhdTR_SOFlHjhRT7b4dGnMTnHoLqkPJKdiAgXNidCWMB1BP5I0GBzHyQGBjApDqS0VN_jZuwtumnCjorBqNnRQpbh12fNoEGMZsJuRQA8XAO2XxlgngkrPY1KqeL0qTpJEhDWuxsc7J_RpvuuzZk-EgtXGhQjNvko-QguCiSLC5uNnBrurEvUQw,CmRaAAAASO5zwGAJm49FhxObdJlnoAMVlDWYq0QtwqAMEPdzYsChsBYpdoHMFgP0yWFCaLSOwJNcGaAd-ZlW8gBvz_8mKrUzoTwgyUBHUDCsMf_byCXO3n6Rdp_C3sA8tE_OF56rEhCBY52QnnUwYf5TWtftyyTWGhRm6cWKwDeGt5fMUPl5qKEqrq70Nw,CmRaAAAAU6sV_qgin7ivsYM84h-vZEKqo-9CX7F2m6QtqNX26FNxS4g-NPT4hRdJ_ymgNlzXF0nRinqhlKRYYjt_DVY0X6VUt9IneL4AHHgLKtnO_-YShlGBr8IaQFvhEOVsJGakEhAgBuGkecz3fDrWtY8dDm6yGhTR0fFzdu5hrDtYNAaxHz5-R504AA,CmRaAAAAZOvyXjFYhYTqPAN4-QYQjaXy3Z13Ty6skESZiCZDkYSn3BnFnlHTrqxMFBmTXaEWaxbLDKV2TDysBxGJ3rw4ra_NgUOJZ9fM-Q-D36ZMy8tUFTRZ5_sqt5zkFWLM7v1JEhA2E5opbJQhzlkOa8WooH0mGhR-gq_gfos548ip4LNIb5LLqNRuQg,CmRaAAAA5WkoP9Zw5WOyIXIoZIldGIeOFGkTy8j3EPGBWF0QJiJ3Y22MLrn4Mwyb6iFZuAHQQrBzIFObZ3-QeyIDnn0Ayq0m9Rlf0qS9h0eoqnPQnDFpyRZDLuxMJupJGpJDOKtxEhA8aMh-ID92psG5Xku6rldyGhTqM190NLECoDZdgeAy8LVEkSQzug,CmRaAAAAGh_KfDYZ0WFYXv1nFkusfmnyjbGXYmBQbL8VgrlGpWin6VmXQZt7OdBM40aQ-FUe-JBgrMI2QATummI3uAChs-gvs-QyC4kwcDQtGW0ONftetDad57l0r3HVbJPFpGUnEhAVMoALU8kjerh5xW73o7UbGhTIqFmyM1ATvx5nUkmF5qPDBhb1yA"}]
    return json.dumps(response)

@app.route('/getPhotos/<photoreference_string>/<int:maxwidth>' , methods = ['GET', 'POST'])
def getPhotos(photoreferences_string, maxwidth):
    # -- FOR INFORMATION ON HOW TO HANDLE REQUEST DATA ON FLASK 
    # -- https://scotch.io/bar-talk/processing-incoming-request-data-in-flask
    photoreference_list = photoreferences_string.split(',')
    photo_list = []
    for reference in photoreference_list:
        photo = APICalls.get_places_photo_api(reference,maxwidth)
        photo_list.append(photo)
    return photo_list

@app.route('/getPlaceDetails', methods = ['GET'])
def getPlaceDetails():
    return  None


# -- FOR HOW TO UPLOAD FILES IN FLASK -- https://medium.com/techkylabs/getting-started-with-python-flask-framework-part-3-1f0e355c9be5


