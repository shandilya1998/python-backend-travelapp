from flask import Flask, session
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_session import Session
app = Flask(__name__)

# This imports all configurations as defined in class Config()
app.config.from_object(Config)

# This creates an object that represents the database
db = SQLAlchemy(app)
migrate = Migrate( app,
                   db)

#creates an object of the LoginManager Flask extension
login = LoginManager(app)
#this tells flask_login which is the view function that handles login
login.login_view = 'login'

#Creates the instance for SQLAlchemy session data storage
#Once the intergface has been imported, flask_session can be used like flask.session
#with no changes in syntax whatsoever
session = Session(app)
#SqlAlchemySessionInterface(app = app,
                           #db = db,
                          # table = 'sessions',
                           #key_prefix = 'sess_',
                           #use_signer = True,
                           #permanent = True)
app.config['SESSION_SQLALCHEMY'] = db
session.app.session_interface.db.create_all()
from app import routes,models
#db.create_all()
