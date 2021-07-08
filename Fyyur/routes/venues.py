from flask import Blueprint, render_template, url_for, request, flash, redirect
from Fyyur.models.artist import Artist
from Fyyur.models.venue import Venue
from Fyyur.models.show import Show
from datetime import datetime
from Fyyur.extensions import db
from forms import *

bp = Blueprint("venues", __name__)


@bp.route('/venues', methods=['GET', 'POST'])
def venues():
    # num_shows should be aggregated based on number of upcoming shows per venue.
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

@bp.route('/venues/search', methods=['POST', 'GET'])
def search_venues():
    # implement search on artists with partial string search. Ensure it is case-insensitive.
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

@bp.route('/venues/<int:venue_id>')
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
        "genres": venue.genres.split(','),
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

@bp.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@bp.route('/venues/create', methods=['POST'])
def create_venue_submission():
    #  insert form data as a new Venue record in the db, instead
    #  modify data to be the data object returned from db insertion
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
        db.session.add(venue)
        db.session.commit()
        # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except:
        # on unsuccessful db insert, flash an error instead.
        db.session.rollback()
        flash('An error occurred. Venue could not be listed.')
    finally:
        db.session.close()
    return render_template('pages/home.html')

@bp.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # Complete this endpoint for taking a venue_id, and using
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

@bp.route('/venues/<int:venue_id>/edit', methods=['GET'])
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
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@bp.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))