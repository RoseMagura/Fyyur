from flask import Blueprint, render_template, url_for, request, flash, redirect
from Fyyur.models.venue import Venue
from datetime import datetime
from Fyyur.extensions import db
from forms import *
from Fyyur.utilities.helper_func import delete, format_genres, insert, update

bp = Blueprint("venues", __name__)


# Create Venue: Display Form
@bp.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


# Create Venue: Posting form
@bp.route('/venues/create', methods=['POST'])
def create_venue_submission():
    #  insert form data as a new Venue record in the db
    form = VenueForm(request.form)
    venue = Venue(
        name=form.name.data,
        genres=form.genres.data,
        city=form.city.data,
        state=form.state.data,
        address=form.address.data,
        phone=form.phone.data,
        facebook_link=form.facebook_link.data,
        image_link=form.image_link.data,
        website=form.website.data,
        seeking_talent=form.seeking_talent.data,
        seeking_description=form.seeking_description.data
    )
    res = insert(db, venue, f'Venue {venue.name} was successfully listed!',
           f'Venue {venue.name} could not be listed.')
    flash(res)
    return render_template('pages/home.html')


# Read All Venues
@bp.route('/venues', methods=['GET'])
def venues():
    # num_shows should be aggregated based on number of upcoming shows per venue.
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
        each = Venue.query.filter(
            Venue.city == place.city, Venue.state == place.state).all()
        for loc in each:
            shows = loc.shows
            upcoming_shows = 0
            for show in shows:
                if (show.start_time > datetime.now()):
                    upcoming_shows += 1
            venue = {
                "id": loc.id,
                "name": loc.name,
                "num_upcoming_shows": upcoming_shows
            }
            entry['venues'].append(venue)
        data.append(entry)
    return render_template('pages/venues.html', areas=data)


# Search Venues
@bp.route('/venues/search', methods=['POST', 'GET'])
def search_venues():
    # implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    search_str = request.args.get('search_term')
    venue_query = Venue.query.filter(
        Venue.name.ilike('%{}%'.format(search_str)))
    venue_list = venue_query.all()
    results_list = []
    for venue in venue_list:
        data = {
            "id": venue.id,
            "name": venue.name,
            "num_upcoming_shows": venue.num_upcoming_shows
        }
        results_list.append(data)
    response = {
        "count": len(venue_list),
        "data": results_list
    }
    return render_template('pages/search_venues.html', results=response, search_term=search_str)


# Read Individual Venue
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
            entry = {
                "artist_id": show.artist_id,
                "artist_name": show.artist_name,
                "artist_image_link": show.artist_image_link,
                "start_time": show.start_time
            }
            upcoming_list.append(entry)
        else:
            past_shows += 1
            entry = {
                "artist_id": show.artist_id,
                "artist_name": show.artist_name,
                "artist_image_link": show.artist_image_link,
                "start_time": show.start_time
            }
            past_list.append(entry)
    venue.genres = format_genres(venue.genres)
    data = {
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


# Update Venue: Display Form
@bp.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm(request.form)
    v = Venue.query.get(venue_id)
    return render_template('forms/edit_venue.html', form=form, venue=v)


# Update Venue: Post Form
@bp.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    form = VenueForm(request.form)
    result = update(db, Venue, venue_id, {
        "name": form.name.data,
        "genres": form.genres.data,
        "city": form.city.data,
        "state": form.state.data,
        "phone": form.phone.data,
        "facebook_link": form.facebook_link.data,
        "image_link": form.image_link.data,
        "website": form.website.data,
        "seeking_talent": form.seeking_talent.data,
        "seeking_description": form.seeking_description.data
    }, 'Successfully updated venue information!',
        'Error. Could not update venue information.')
    flash(result)
    return redirect(url_for('venues.show_venue', venue_id=venue_id))


# Delete Venue
@bp.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    venue = Venue.query.get(venue_id)
    result = delete(db, venue, f'Venue {venue.name} was successfully deleted',
                    f'Venue {venue.name} could not be deleted')
    flash(result)
    return redirect('/venues')
