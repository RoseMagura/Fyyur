#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import json
import dateutil.parser
import babel
import flask
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import enum
from sqlalchemy import func, distinct, Enum
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from datetime import date
from forms import *

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
migrate = Migrate(app, db)

#Connect to a local postgresql database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rosie:password@localhost:5432/fyyur'
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Genres(enum.Enum):
    Alternative = 'Alternative'
    Blues = 'Blues'
    Classical = 'Classical'
    Country = 'Country'
    Electronic = 'Electronic'
    Folk = 'Folk'
    Funk = 'Funk'
    HipHop = 'Hip-Hop'
    Heavy_Metal = 'Heavy Metal'
    Instrumental = 'Instrumental'
    Jazz = 'Jazz'
    Musical_Theatre = 'Musical Theatre'
    Pop = 'Pop'
    Punk = 'Punk'
    RB = 'R&B'
    Reggae = 'Reggae'
    Rock_N_Roll = 'Rock N Roll'
    Soul = 'Soul'
    Other = 'Other'
    def __str__(self):
        return str(self.value)

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    genres = db.Column(db.Enum(Genres))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean(), default=False)
    seeking_description = db.Column(db.String(120))
    num_upcoming_shows = db.Column(db.Integer, default=0)
    shows = db.relationship('Show', backref = 'Venue', lazy=True)

    # def __repr__(self):
    #     return '<Show {} {}>'.format(self.id, self.name)

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(120))
    genres = db.Column(db.Enum(Genres))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean())
    seeking_description = db.Column(db.String(500))
    num_upcoming_shows = db.Column(db.Integer, default=0)
    shows = db.relationship('Show', backref='Artist', lazy=True)

    def __repr__(self):
        return '<Show {} {}>'.format(self.id, self.name)

class Show(db.Model):
    __tablename__ = 'Show'
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.String(120))
    artist_id = db.Column(db.Integer, db.ForeignKey(Artist.id))
    artist_name = db.Column(db.String(120))
    artist_image_link = db.Column(db.String(500))
    venue_id = db.Column(db.Integer, db.ForeignKey(Venue.id))
    venue_name = db.Column(db.String(120))
    venue_image_link = db.Column(db.String(500))

    # def __repr__(self):
    #     return '<Show {} {}>'.format(self.artist_id, self.venue_id)

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

@app.route('/venues', methods=['GET', 'POST'])
def venues():
    # TODO: num_shows should be aggregated based on number of upcoming shows per venue.
    db_venues = Venue.query.all()
    data = []
    distinct_places = db.session.query(Venue.city, Venue.state).\
    group_by(Venue.city, Venue.state).all()

    for place in distinct_places:
        venue = {}
        entry = {
                "city": place.city,
                "state": place.state,
                "venues": []
            }
        each = Venue.query.filter(Venue.city == place.city, Venue.state == place.state).all()
        for y in each:
            shows = y.shows
            upcoming_shows = 0
            for show in shows:
                if (show.start_time > datetime.now()):
                    upcoming_shows += 1
            venue = {
                "id": y.id,
                "name": y.name,
                "num_upcoming_shows": upcoming_shows
            }
            entry['venues'].append(venue)
        data.append(entry)
    return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST', 'GET'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    search_str = request.args.get('search_term')
    venue_query = Venue.query.filter(Venue.name.ilike('%{}%'.format(search_str)))
    venue_list = venue_query.all()
    results_list = []
    for venue in venue_list:
        data = {
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": venue.num_upcoming_shows
        }
        results_list.append(data)

    response={
    "count": len(venue_list),
    "data": results_list
    }
    return render_template('pages/search_venues.html', results=response, search_term=search_str)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    venue = Venue.query.get(venue_id)
    past_list = []
    upcoming_list = []
    past_shows = 0
    upcoming_shows = 0
    shows = venue.shows
    for show in shows:
        if (show.start_time > datetime.now()):
            upcoming_shows += 1
            entry =     {
                "artist_id": show.artist_id,
                "artist_name": show.artist_name,
                "artist_image_link": show.artist_image_link,
                "start_time": show.start_time.strftime('%m/%d/%Y, %H:%M')
              }
            upcoming_list.append(entry)
        else:
            past_shows += 1
            entry =     {
                "artist_id": show.artist_id,
                "artist_name": show.artist_name,
                "artist_image_link": show.artist_image_link,
                "start_time": show.start_time.strftime('%m/%d/%Y, %H:%M')
              }
            past_list.append(entry)
    data={
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
        "past_shows": past_list,
        "upcoming_shows": upcoming_list,
        "past_shows_count": past_shows,
        "upcoming_shows_count": upcoming_shows,
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
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    form = VenueForm(request.form)
    num_venues = Venue.query.count()
    try:
        venue = Venue(
            id = num_venues + 1,
            name = form.name.data,
            genres = form.genres.data,
            city = form.city.data,
            state = form.state.data,
            address = form.address.data,
            phone = form.phone.data,
            facebook_link = form.facebook_link.data,
            #show a generic image for new venues
            image_link = 'https://i.guim.co.uk/img/media/ad98f2dc808f18131e35e59c05ba6212671e8227/94_0_3061_1838/master/3061.jpg?width=1920&quality=85&auto=format&fit=max&s=c515d483b75926f0d68512f263c2c26f'
        )
        if not form.validate():
            flash(form.errors)
            return redirect(url_for('create_venue_form'))
        db.session.add(venue)
        db.session.commit()
        # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except:
        # TODO: on unsuccessful db insert, flash an error instead.
        db.session.rollback()
        flash('An error occurred. Venue could not be listed.')
    finally:
        db.session.close()
    return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session
    #commit could fail.
    venue = Venue.query.get(venue_id)
    try:
        db.session.delete(venue)
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
  # TODO: replace with real data returned from querying the database
  data = Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['GET'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    search_str = request.args.get('search_term')
    artist_query = Artist.query.filter(Artist.name.ilike('%{}%'.format(search_str)))
    artist_list = artist_query.all()
    results_list = []
    for artist in artist_list:
        data = {
            'id': artist.id,
            'name':  artist.name,
            'num_upcoming_shows': artist.num_upcoming_shows
        }
        results_list.append(data)

    response={
    'count': len(artist_list),
    'data': results_list
    }
    return render_template('pages/search_artists.html', results=response, search_term=search_str)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
    artist = Artist.query.get(artist_id)
    past_list = []
    upcoming_list = []
    up_entry ={}
    entry ={}
    past_shows = 0
    upcoming_shows = 0
    shows = artist.shows
    for show in shows:
      if (show.start_time > datetime.now()):
          upcoming_shows += 1
          up_entry =     {
              "venue_id": show.venue_id,
              "venue_name": show.venue_name,
              "venue_image_link": show.venue_image_link,
              "start_time": show.start_time.strftime('%m/%d/%Y, %H:%M')
            }
          upcoming_list.append(up_entry)
      elif (show.start_time < datetime.now()):
          past_shows += 1
          entry =     {
              "venue_id": show.venue_id,
              "venue_name": show.venue_name,
              "venue_image_link": show.venue_image_link,
              "start_time": show.start_time.strftime('%m/%d/%Y, %H:%M')
            }
          past_list.append(entry)
    data={
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
        "past_shows": past_list,
        "upcoming_shows": upcoming_list,
        "past_shows_count": past_shows,
        "upcoming_shows_count": upcoming_shows,
    }
    return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    artist = Artist.query.get(artist_id)
    form = ArtistForm(request.form)
    artist.name = form.name.data
    artist.genres = form.genres.data
    artist.city = form.city.data

    # artist= Artist(
    #     "id": artist_id,
    #     "name": form.name.data,
    #     "genres": form.genres.data,
    #     "city": form.city.data,
    #     "state": form.state.data,
    #     "phone": form.phone.data,
    #     "facebook_link": form.facebook_link.data,
    #     "image_link":'https://i.guim.co.uk/img/media/ad98f2dc808f18131e35e59c05ba6212671e8227/94_0_3061_1838/master/3061.jpg?width=1920&quality=85&auto=format&fit=max&s=c515d483b75926f0d68512f263c2c26f',
    # )
    # try:
    db.session.add(artist)
    db.session.commit()
    flash('Updated artist information')
    # except:
    #     db.session.rollback()
    #     flash('Error. Could not update artist information')
    # finally:
    #     db.session.close()
    return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    form = ArtistForm(request.form)
    artist = Artist.query.get(artist_id)
    artist = {
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
            # "past_shows": past_list,
            # "upcoming_shows": upcoming_list,
            # "past_shows_count": past_shows,
            # "upcoming_shows_count": upcoming_shows
    }
    return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm(request.form)
  v = Venue.query.get(venue_id)
  venue={
    "id": v.id,
    "name": v.name,
    "genres": v.genres,
    "address": v.address,
    "city": v.city,
    "state": v.state,
    "phone": v.phone,
    "website": v.website,
    "facebook_link": v.facebook_link,
    "seeking_talent": v.seeking_talent,
    "seeking_description": v.seeking_description,
    "image_link": v.image_link
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    form = ArtistForm(request.form)
    num_artists = Artist.query.count()
    artist = Artist(
        id = num_artists + 4,
        name = form.name.data,
        genres = form.name.data,
        city = form.city.data,
        state = form.state.data,
        phone = form.phone.data,
        facebook_link = form.facebook_link.data,
        website = form.website.data,
        seeking_venue = form.seeking_venue.data,
        seeking_description = form.seeking_description.data,
        image_link = form.image_link.data
)
    if not form.validate():
        flash(form.errors)
        return redirect(url_for('create_artist_form'))
    try:
        db.session.add(artist)
        db.session.commit()
        # on successful db insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    # TODO: on unsuccessful db insert, flash an error instead.
    except:
        flash('An error occurred. Artist ' + form.name + ' could not be listed.')
        db.rollback()
    finally:
        db.session.commit()
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  # num_shows should be aggregated based on number of upcoming shows per venue.
    data = []
    shows = Show.query.all()
    for show in shows:
      data.append({
      "venue_id": show.venue_id,
      "venue_name": show.venue_name,
      "artist_id": show.artist_id,
      "artist_name": show.artist_name,
      "artist_image_link": show.artist_image_link,
      "start_time": show.start_time.strftime('%m/%d/%Y, %H:%M')})

    return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    form = ShowForm(request.form)
    num_shows = Show.query.count()
    artist = Artist.query.get(form.artist_id.data)
    venue = Venue.query.get(form.venue_id.data)
    try:
        show = Show(
        id = num_shows + 1,
        artist_id = form.artist_id.data,
        artist_name = artist.name,
        artist_image_link = artist.image_link,
        venue_id = form.venue_id.data,
        venue_name = venue.name,
        start_time = form.start_time.data
        )
        if (form.start_time.data > datetime.now()):
            artist.num_upcoming_shows += 1
            venue.num_upcoming_shows +=1
            db.session.add(artist, venue)
            db.session.commit()
        db.session.add(show)
        db.session.commit()
        # on successful db insert, flash success
        flash('Show was successfully listed!')
    except:
        db.session.rollback()
      # TODO: on unsuccessful db insert, flash an error instead.
        flash('An error occurred. Show could not be listed.')
    finally:
        db.session.close()
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
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
