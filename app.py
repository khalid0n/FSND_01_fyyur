#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import sys

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


class Shows(db.Model):
  __tablename__ = 'Shows'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
  start_time = db.Column('start_time', db.DateTime)


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')

#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():

  data = []
  total_venues = Venue.query.all()

  for venue in total_venues:
    values = {
      "city": venue.city,
      "state": venue.state,
      "venues": Venue.query.filter_by(city=venue.city).all()
    }
    data.append(values)

  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():

  search_str = request.form.get('search_term', '')
  # using 'ilike' for case-insensitivity
  filtered_venue = Venue.query.filter(Venue.name.ilike('%' + search_str + '%'))

  response = {
    "count": filtered_venue.count(),
    "data": filtered_venue
  }

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):

  past_shows = []
  upcoming_shows = []

  venue = Venue.query.get(venue_id)

  for show in venue.shows:
    tmp_show = {
      "artist_id": show.artist_id,
      "artist_name": show.Artist.name,
      "artist_image_link": show.Artist.image_link,
      "start_time": show.start_time
    }
    if show.start_time > datetime.now():
      upcoming_shows.append(tmp_show)
    else:
      past_shows.append(tmp_show)

  data = {
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows)
  }

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  try:
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    address = request.form['address']
    phone = request.form['phone']
    facebook_link = request.form['facebook_link']
    genres = request.form['genres']
    venue = Venue(name=name, city=city, state=state, address=address, phone=phone,
                  facebook_link=facebook_link, genres=genres)
    db.session.add(venue)
    db.session.commit()

    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
    db.session.rollback()
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  finally:
    db.session.close()

  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):

  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  data = Artist.query.all()

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_str = request.form.get('search_term', '')
  filtered_artist = Artist.query.filter(Artist.name.ilike('%' + search_str + '%'))

  response = {
    "count": filtered_artist.count(),
    "data": filtered_artist
  }

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):

  past_shows = []
  upcoming_shows = []

  artist = Artist.query.get(artist_id)

  for show in artist.shows:
    tmp_show = {
      "venue_id": show.venue_id,
      "venue_name": show.Venue.name,
      "venue_image_link": show.Venue.image_link,
      "start_time": show.start_time
    }
    if show.start_time > datetime.now():
      upcoming_shows.append(tmp_show)
    else:
      past_shows.append(tmp_show)

  data = {
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows)
  }

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  target_artist = Artist.query.get(artist_id)

  artist={
    "id": target_artist.id,
    "name": target_artist.name,
    "genres": target_artist.genres,
    "city": target_artist.city,
    "state": target_artist.state,
    "phone": target_artist.phone,
    "website": target_artist.website,
    "facebook_link": target_artist.facebook_link,
    "seeking_venue": target_artist.seeking_venue,
    "seeking_description": target_artist.seeking_description,
    "image_link": target_artist.image_link
  }

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):

  try:
    target_artist = Artist.query.get(artist_id)

    target_artist.name = request.form.get('name')
    target_artist.city = request.form.get('city')
    target_artist.state = request.form.get('state')
    target_artist.phone = request.form.get('phone')
    target_artist.facebook_link = request.form.get('facebook_link')
    target_artist.genres = request.form.get('genres')

    db.session.add(target_artist)
    db.session.commit()

  except:
    db.session.rollback()

  finally:
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  target_venue = Venue.query.get(venue_id)

  venue={
    "id": target_venue.id,
    "name": target_venue.name,
    "genres": target_venue.genres,
    "address": target_venue.address,
    "city": target_venue.city,
    "state": target_venue.state,
    "phone": target_venue.phone,
    "website": target_venue.website,
    "facebook_link": target_venue.facebook_link,
    "seeking_talent": target_venue.seeking_talent,
    "seeking_description": target_venue.seeking_description,
    "image_link": target_venue.image_link
  }

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  try:
    target_venue = Venue.query.get(venue_id)

    target_venue.name = request.form.get('name')
    target_venue.city = request.form.get('city')
    target_venue.state = request.form.get('state')
    target_venue.address = request.form.get('address')
    target_venue.phone = request.form.get('phone')
    target_venue.facebook_link = request.form.get('facebook_link')
    target_venue.genres = request.form.get('genres')

    db.session.add(target_venue)
    db.session.commit()

  except:
    db.session.rollback()

  finally:
    db.session.close()
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  try:
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    phone = request.form['phone']
    facebook_link = request.form['facebook_link']
    genres = request.form['genres']
    artist = Artist(name=name, city=city, state=state, phone=phone,
                  facebook_link=facebook_link, genres=genres)
    db.session.add(artist)
    db.session.commit()

    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
    db.session.rollback()
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
  finally:
    db.session.close()

  return render_template('pages/home.html')

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  data = []
  total_shows = Shows.query.all()

  for show in total_shows:
    values = {
      "venue_id": show.Venue.id,
      "venue_name": show.Venue.name,
      "artist_id": show.Artist.id,
      "artist_name": show.Artist.name,
      "artist_image_link": show.Artist.image_link,
      "start_time": show.start_time
    }
    data.append(values)

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  try:

    artist_id = request.form['artist_id']
    venue_id = request.form['venue_id']
    start_time = request.form['start_time']

    show = Shows(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
    db.session.add(show)
    db.session.commit()
    flash('Show was successfully listed!')

  except:
    db.session.rollback()
    flash('An error occurred. Show could not be listed.')

  finally:
    db.session.close()

  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
