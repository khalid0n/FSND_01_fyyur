from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_migrate import Migrate

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

migrate = Migrate(app, db)


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    genres = db.Column(db.String(250))
    website = db.Column(db.String(500))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))

    shows = db.relationship("Shows", backref=db.backref('Venue', lazy=True))

    def count_past_shows(self):
        return self.query.join(Shows).filter_by(venue_id=self.id).filter(
            Shows.start_time < datetime.now()).count()

    def count_upcoming_shows(self):
        return self.query.join(Shows).filter_by(venue_id=self.id).filter(
            Shows.start_time > datetime.now()).count()

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    website = db.Column(db.String(500))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))

    shows = db.relationship("Shows", backref=db.backref('Artist', lazy=True))

    def count_past_shows(self):
        return self.query.join(Shows).filter_by(artist_id=self.id).filter(
            Shows.start_time < datetime.now()).count()

    def count_upcoming_shows(self):
        return self.query.join(Shows).filter_by(artist_id=self.id).filter(
            Shows.start_time > datetime.now()).count()


class Shows(db.Model):
    __tablename__ = 'Shows'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    start_time = db.Column('start_time', db.DateTime)

    # @classmethod
    # def get_past_by_venue(cls, venue_id):
    #     shows = cls.query.filter_by(venue_id=venue_id).filter(cls.start_time < datetime.now()).all()
    #     return [show for show in shows]


