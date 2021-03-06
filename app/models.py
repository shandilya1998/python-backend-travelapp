from app import db, login
from app.APICalls import APICalls
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

#Every class here represents a table in the database

@login.user_loader
def load_user(iduser):
    return users.query.get(int(iduser))

def in_places_served(idplace):
    return db.session.query(place).filter_by(idplace = idplace).scalar() is not None


class place(db.Model):
    idplace = db.Column(db.String(100),
                         primary_key = True,
                         nullable = False,
                         unique = True,
                         index = True)# the column being referenced should be the sole index for the referenced table
    # for the foreign key to be successfully applied
    # places details API will have to be called to fetch the photos of a place as photoreference changes with time
    # thus all the other information need not be stored
    name = db.Column(db.String(200),
                      nullable = False)
    latitude = db.Column(db.Float(9))
    longitude = db.Column(db.Float(9))
    city = db.Column(db.String(50),
                     nullable = False)
    openingHours = db.Column(db.JSON)
    photo = db.Column(db.JSON)
    stayTime = db.Column(db.Time)
    numUsersVisited = db.Column(db.Integer)
    history = db.Column(db.String(400))
    descriptionShort = db.Column(db.String(200))
    descriptionLong = db.Column(db.String(1000))
    address = db.Column(db.String(1000))
    phoneNum = db.Column(db.String(20))
    website = db.Column(db.String(2000))
    tags = db.relationship('placeDescriptionTag',
                           backref = 'place')

    itineraryItem = db.relationship('itineraryItem',
                                     backref = 'place')
    reviews = db.relationship('experienceReview',
                              backref = 'place')     

    def add_to_db(self, idplace):
        exists = self.in_places(idplace)
        if not exists:
            place_details = APICalls.call_places_details_api(idplace)
            place = places(place_details) # correct this statement based on the response from places details API
            db.session.add(place)
            db.session.commit()

    def serialize(self):
            return {
                    'name' : self.name,
                    'latitude' : self.latitude,
                    'longitude' : self.longitude,
                    'city' : self.city, 
                    'openingHours' : self.openingHours,
                    'photo' : self.photo,
                    'stayTime' : self.stayTime,
                    'numUsersVisited' : self.numUsersVisited,
                    'history' : self.history,
                    'descriptionShort' : self.descriptionShort, 
                    'address' : self.address,
                    'phoneNum' : self.phoneNum,
                    'website' : self.website,
                    'tags' : [tag.serialize() for tag in self.tags],
                    'itineraryItem' : self.itineraryItem,
                    'reviews' : self.reviews}

    def __repr__(self):
        return '<Place {}>'.format(self.name)


class user(UserMixin, db.Model):
    iduser = db.Column(db.Integer,
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
                              default = 0)
    password = db.Column(db.String(100))
    session = db.relationship('session',
                               backref = 'user')
    itinerary = db.relationship('itinerary',
                                backref = 'user')
    trips = db.relationship('trip',
                            backref = 'user')
    reviews = db.relationship('experienceReview',
                              backref = 'reviewsUser')
    userProfileTag = db.relationship('userProfileTag',
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
        return self.iduser

    def __repr__(self):
        return '<Place {}'.format(self.username)


class placeDescriptionTag(db.Model):
    idplaceDescription = db.Column(db.Integer,
                                   primary_key = True,
                                   nullable = False,
                                   autoincrement = True,
                                   unique = True)
    idplace = db.Column(db.String(100),
                         db.ForeignKey('place.idplace'),
                         nullable = False)
    tag = db.Column(db.String(50),
                    nullable = False)

    def __repr__(self):
        return '<Place Tag {}>'.format(self.tag)

    def serialize(self):
        return {
                'idplaceDescription' : self.idplaceDescription,
                'idplace' : self.idplace,
                'tag' : self.tag
                }


class session(db.Model):
    idsession = db.Column(db.Integer,
                   primary_key = True,
                   nullable = False,
                   unique = True,
                   autoincrement = True)
    iduser = db.Column(db.Integer,
                       db.ForeignKey('user.iduser'))
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
    iduser = db.Column(db.Integer,
                       db.ForeignKey('user.iduser'))
    idsession = db.Column(db.Integer,
                          db.ForeignKey('session.idsession'))
    items = db.relationship('itineraryItem',
                             backref = 'itinerary')

    def get_itinerary_id(self,
                         idsession,
                         iduser):
        itinerary_ = itinerary.query.filter_by(iduser = iduser,
                                               idsession = idsession)
        if itinerary_.scalar() is not None:
            return itinerary_.iditinerary
        else:
            itinerary_ = itinerary(idsession = idsession,
                                   iduser = iduser)
            db.session.add(itinerary_)
            db.session.commit()
            return itinerary_.iditinerary

    def _repr__(self):
        return 'itinerary num {}'.format(self.iditinerary)


class itineraryItem(db.Model):
    iditineraryItem = db.Column(db.Integer,
                                primary_key = True,
                                nullable = False,
                                autoincrement = True,
                                unique = True)
    iditinerary = db.Column(db.Integer,
                            db.ForeignKey('itinerary.iditinerary'))
    idplace = db.Column(db.String(100),
                        db.ForeignKey('place.idplace'))

    def add_to_itinerary(self,
                         idplace,
                         idsession,
                         iduser):
        # this function will be called to add a place to the itinerary according to place_id, session_id and user_id
        place.add_to_db(idplace)
        # get_itinerary_id() returns the iditinerary with idsession and iduser
        iditinerary = itinerary.get_itinerary_id(idsession, #needs implementation of session
                                                 iduser)
        itineraryItem = itineraryItems(iditinerary = iditinerary,
                                       idplace = idplace)
        db.session.add(itineraryItem)
        db.session.commit()

    def __repr__(self):
        return 'Item {}'.format(self.iditineraryItem)


class trip(db.Model):
    idtrip = db.Column(db.Integer,
                        primary_key = True,
                        nullable = False)
    iduser = db.Column(db.Integer,
                       db.ForeignKey('user.iduser'))
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
    iduser = db.Column(db.Integer,
                       db.ForeignKey('user.iduser'))
    idplace = db.Column(db.String(100),
                        db.ForeignKey('place.idplace'))
    idtrip = db.Column(db.Integer,
                       db.ForeignKey('trip.idtrip'))
    tripRating = db.Column(db.Integer,
                           nullable = False)
    review = db.Column(db.String(200))
    timeSpent = db.Column(db.Time,
                          nullable = False)

    def __repr__(self):
        return 'review {}'.format(self.idexperienceReview)

class userProfileTag(db.Model):
    iduserprofileTag = db.Column(db.Integer,
                              primary_key = True,
                              nullable = False)
    iduser = db.Column(db.Integer,
                       db.ForeignKey('user.iduser'))
    tag = db.Column(db.String(45),
                    nullable = False)



