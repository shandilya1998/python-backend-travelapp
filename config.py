import os

class Config():
    #Test Secret Key
    SECRET_KEY = 'changeme'
    #Database config
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://shandilya:Princyy-12345@127.0.0.1:5432/db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # this configurea session for when users enter the app, login and deletes it when they logout
    SESSION_TYPE = 'sqlalchemy'
    SESSION_PERMANENT = True

