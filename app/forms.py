from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo 
from werkzeug.datastructures import CombinedMultiDict
from app.models import users

from flask_uploads import UploadSet, IMAGES
images = UploadSet('images', IMAGES)



#This class implements the login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


#This class implements the registration form
class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(),
                        Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    password2 = PasswordField('Repeat Password',
                              validators=[DataRequired(),
                              EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = users.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = users.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class EditProfileForm(FlaskForm):
    """
        This form is sent when the 'SAVE' button on the edit profile sreen is pressed
        Add Other attributes to change
    """
    fname = StringField('First Name', validators = [DataRequired()])
    lname = StringFiels('Last Name', validators = [DataRequired()])
    
class UploadProfileImageForm(FlaskForm):
    """
        This form is used to upload user profile image 
    """
    upload = FileField('image', validators=[
             FileRequired(),
             FileAllowed(images, 'Images only!')
            ])




