"""Models and database functions for project"""

from flask_sqlalchemy import SQLAlchemy
import datetime

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of weather app"""


    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    zipcode = db.Column(db.Integer, db.ForeignKey("locations.zipcode"))

    location = db.relationship("Location", backref=db.backref("users"))

    @staticmethod
    def add_user(email, password, first_name, last_name, zipcode):
        """Add new user"""


        user = User(email=email, password=password, first_name=first_name,
                last_name=last_name, zipcode=zipcode)

        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_user_by_email_and_password(email, password):
        """Get existing user by email and password"""


        user = User.query.filter_by(email=email, password=password).first()

        return user


    @staticmethod
    def get_user_by_email(email):
        """get existing user by email"""


        user = User.query.filter_by(email=email).first()

        return user

    @staticmethod
    def update_zipcode(user_id, zipcode):
        """update existing zipcode"""

        user = User.query.filter_by(user_id=user_id).first()
        user.zipcode = zipcode
        db.session.commit()

        return user



    def __repr__(self):
        """Provide helpful representation when printed"""

        return "<User user_id=%s email=%s first_name=%s last_name=%s zipcode=%d>" % (self.user_id, self.email, self.first_name, self.last_name, self.zipcode)


class Update(db.Model):
    """Table to store updates being posted"""


    __tablename__ = "updates"

    update_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    time = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    post = db.Column(db.String(500), nullable=False)

    #define relationship
    user = db.relationship("User", backref=db.backref("updates"))


    @staticmethod
    def add_update(user_id, post):
        """Add update post"""

        time = datetime.datetime.utcnow()
        update = Update(user_id=user_id, post=post, time=time)

        db.session.add(update)
        db.session.commit()

        return update

    def __repr__(self):
        """Provide helpful representation when printed"""


        return "<Update update_id=%s user_id=%s time=%s post=%s>" % (self.update_id, self.user_id, self.time, self.post)


class Friendship(db.Model):
    """Table to store relationship between friends"""

    __tablename__ = "friendships"

    friendship_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    friend_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    user = db.relationship("User", foreign_keys="Friendship.user_id",
        backref=db.backref("friendships"))
    friend = db.relationship("User", foreign_keys="Friendship.friend_id")

    @staticmethod
    def add_friend(user_id, friend_id):
        """add friend"""

        friendship = Friendship(user_id=user_id, friend_id=friend_id)

        db.session.add(friendship)
        db.session.commit()

        return friendship


    def __repr__(self):
        """provide helpful representation when printed"""

        return "<Friendship friendship_id=%s user_id=%s friend_id=%s>" % (self.friendship_id, self.user_id, self.friend_id)


class Location(db.Model):
    """Table to store location data from locations.json"""

    __tablename__ = "locations"

    zipcode = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    county = db.Column(db.String(100), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    
    #user = db.relationship("User", foreign_keys="Location.zipcode", backref=db.backref("locations"))
    user = db.relationship("User", backref=db.backref("locations"))

    def __repr__(self):
        """Provide helpful representation when printed"""

        return "<Location zipcode=%d city=%s county=%s lat=%f lng=%f>" % (self.zipcode, self.city, self.county, self.lat, self.lng)



##############################################################################
# Add, update, delete functions




##############################################################################
# Query functions





##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///weather'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."