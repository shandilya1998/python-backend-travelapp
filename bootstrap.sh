#!/bin/sh

#Export flask app. Input is app path
export FLASK_APP=~/TravelApp/python-backend-travelapp/travelapp.py

#Development Mode
export FLASK_ENV=development

#activate virtual environment
source venv/bin/activate
#Run app on all listening ports of the server
flask run -h 127.0.0.1 # https://localhost@shandilya:Princyy-12345

