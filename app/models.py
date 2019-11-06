from app import db,login
from app.APICalls import APICalls
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

#Every class here represents as table in the database

@login.user_loader
def load_user(idusers):
    return users.query.get(int(idusers))

class places(db.Model):
    place_id = db.Column(db.String(100),
                         primary_key = True,
                         nullable = False,
                         unique = True,
                         index = True)# the column being referenced should be the sole index for the referenced table
    # for the foreign key to be successfully applied
    # places details API will have to be called to fetch the photos of a place as photoreference changes with time
    # thus all the other information need not be stored
    name = db.Column(db.String(200),
                      nullable = False)
    latitude = db.Column(db.Float(9),
                         nullable = False)
    longitude = db.Column(db.Float(9),
                          nullable = False)
    city = db.Column(db.String(50),
                     nullable = False)
    openingHours = db.Column(db.JSON)
    photo = db.Column(db.JSON)
    stayTime = db.Column(db.Time)
    numUsersVisited = db.Column(db.Integer)
    history = db.Column(db.String(400))
    descriptionShort = db.Column(db.String(200))
    descriptionLong = db.Column(db.String(1000))
    address = db.Column(db.String(1000),
                        nullable = False)
    phoneNum = db.Column(db.String(20))
    website = db.Column(db.String(2000))
    tags = db.relationship('placeDescriptionTag',
                           backref = 'place')

    itineraryItems = db.relationship('itineraryItems',
                                     backref = 'place')
    reviews = db.relationship('experienceReview',
                              backref = 'place')

    def in_places(self,
                  place_id):
        return db.session.query(places).filter_by(place_id = place_id).scalar() is not None

    def add_to_db(self,place_id):
        exists = self.in_places(place_id)
        if not exists:
            place_details = APICalls.call_places_details_api(place_id)
            place = places(place_details) # correct this statement based on the response from places details API
            db.session.add(place)
            db.session.commit()

    def __repr__(self):
        return '<Place {}>'.format(self.name)


class users(UserMixin, db.Model):
    idusers = db.Column(db.Integer,
                        primary_key = True,
                        nullable = False,
                        autoincrement = True,
                        unique = True)
    username = db.Column(db.String(100),
                         nullable = False,
                         unique = True)
    userPhoneNum = db.Column(db.Integer)
    email = db.Column(db.String(200),
                      #primary_key = True,
                      nullable = False)
    numTripsTaken = db.Column(db.String(10),
                              default = 0,
                              nullable = False)
    password = db.Column(db.String(100))
    session = db.relationship('session',
                               backref = 'user')
    itinerary = db.relationship('itinerary',
                                backref = 'user')
    trips = db.relationship('trips',
                            backref = 'user')
    reviews = db.relationship('experienceReview',
                              backref = 'reviewsUser')
    userprofiletags = db.relationship('userProfileTags',
                                  backref = 'user')

    def set_password(self,
                     password):
        # This function is used to generate a hashed password for a user
        self.password = generate_password_hash(password)

    def check_password(self,
                       password):
        # This function is used to check if the password entered matches the user's password
        return check_password_hash(self.password,
                                   password)

    def get_id(self):
        return self.idusers

    def __repr__(self):
        return '<Place {}'.format(self.username)


class placeDescriptionTag(db.Model):
    idplaceDescription = db.Column(db.Integer,
                                   primary_key = True,
                                   nullable = False,
                                   autoincrement = True,
                                   unique = True)
    place_id = db.Column(db.String(100),
                         db.ForeignKey('places.place_id'),
                         nullable = False)
    tag = db.Column(db.String(50),
                    nullable = False)

    def __repr__(self):
        return '<Place Tag {}>'.format(self.tag)


class session(db.Model):
    id = db.Column(db.Integer,
                   primary_key = True,
                   nullable = False,
                   unique = True,
                   autoincrement = True)
    userID = db.Column(db.Integer,
                       db.ForeignKey('users.idusers'))
    itineratyList = db.relationship('itinerary',
                                    backref = 'session')

    def __repr__(self):
        return 'Session {}'.format(self.id)


class itinerary(db.Model):
    iditinerary = db.Column(db.Integer,
                            primary_key = True,
                            nullable = False,
                            autoincrement = True,
                            unique = True)
    userID = db.Column(db.Integer,
                       db.ForeignKey('users.idusers'))
    sessionID = db.Column(db.Integer,
                          db.ForeignKey('session.id'))
    items = db.relationship('itineraryItems',
                             backref = 'itinerary')

    def get_itinerary_id(self,
                         session_id,
                         user_id):
        itinerary_ = itinerary.query.filter_by(userID = user_id,
                                               sessionID = session_id)
        if itinerary_.scalar() is not None:
            return itinerary_.iditinerary
        else:
            itinerary_ = itinerary(sessionID = session_id,
                                   userID = user_id)
            db.session.add(itinerary_)
            db.session.commit()
            return itinerary_.iditinerary

    def _repr__(self):
        return 'itinerary num {}'.format(self.iditinerary)


class itineraryItems(db.Model):
    iditineraryItem = db.Column(db.Integer,
                                primary_key = True,
                                nullable = False,
                                autoincrement = True,
                                unique = True)
    itineraryID = db.Column(db.Integer,
                            db.ForeignKey('itinerary.iditinerary'))
    placeID = db.Column(db.String(100),
                        db.ForeignKey('places.place_id'))

    def add_to_itinerary(self,
                         place_id,
                         session_id,
                         user_id):
        # this function will be called to add a place to the itinerary according to place_id, session_id and user_id
        places.add_to_db(place_id)
        # get_itinerary_id() returns the itinerary id with session_id and user_id
        itinerary_id = itinerary.get_itinerary_id(session_id, #needs implementation of session
                                                  user_id)
        itineraryItem = itineraryItems(itineraryID = itinerary_id,
                                       placeID = place_id)
        db.session.add(itineraryItem)
        db.session.commit()

    def __repr__(self):
        return 'Item {}'.format(self.iditineraryItem)


class trips(db.Model):
    idtrips = db.Column(db.Integer,
                        primary_key = True,
                        nullable = False)
    userID = db.Column(db.Integer,
                       db.ForeignKey('users.idusers'))
    triptime = db.Column(db.Time,
                         nullable = False)
    tripDistance = db.Column(db.Float(10),
                             nullable = False)
    numPlacesVisted = db.Column(db.Integer,
                                nullable = False)
    reviews = db.relationship('experienceReview',
                              backref = 'reviewsTrip')

    def __repr__(self):
        return 'trip id {}'.format(self.idtrips)


class experienceReview(db.Model):
    idexperienceReview = db.Column(db.Integer,
                                   primary_key = True,
                                   nullable = False)
    userID = db.Column(db.Integer,
                       db.ForeignKey('users.idusers'))
    placeID = db.Column(db.String(100),
                        db.ForeignKey('places.place_id'))
    tripID = db.Column(db.Integer,
                       db.ForeignKey('trips.idtrips'))
    tripRating = db.Column(db.Integer,
                           nullable = False)
    review = db.Column(db.String(200))
    timeSpent = db.Column(db.Time,
                          nullable = False)

    def __repr__(self):
        return 'review {}'.format(self.idexperienceReview)

class userProfileTags(db.Model):
    iduserprofileTag = db.Column(db.Integer,
                              primary_key = True,
                              nullable = False)
    iduser = db.Column(db.Integer,
                       db.ForeignKey('users.idusers'))
    tag = db.Column(db.String(45),
                    nullable = False)



