from flask import Blueprint, render_template, url_for, request, flash, redirect
from Fyyur.models.artist import Artist
from datetime import datetime
from Fyyur.extensions import db
from forms import *
from Fyyur.utilities.helper_func import delete, format_genres, insert, update

bp = Blueprint("artists", __name__)


# Create Artists: Display Form
@bp.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


# Create Show: Posting form
@bp.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    form = ArtistForm(request.form)
    artist = Artist(
        name=form.name.data,
        genres=form.genres.data,
        city=form.city.data,
        state=form.state.data,
        phone=form.phone.data,
        facebook_link=form.facebook_link.data,
        website=form.website.data,
        seeking_venue=form.seeking_venue.data,
        seeking_description=form.seeking_description.data,
        image_link=form.image_link.data
    )
    result = insert(db, artist, f'Artist {artist.name} was successfully listed!',
                    f'An error occurred. Artist {artist.name} could not be listed.')
    flash(result)
    return render_template('pages/home.html')


# Read all artists
@bp.route('/artists')
def artists():
    data = Artist.query.all()
    return render_template('pages/artists.html', artists=data)


# Search artists
@bp.route('/artists/search', methods=['GET', 'POST'])
def search_artists():
    # Search on artists with partial string search. Ensure it is case-insensitive.
    search_str = request.args.get('search_term')
    artist_query = Artist.query.filter(
        Artist.name.ilike('%{}%'.format(search_str)))
    artist_list = artist_query.all()
    results_list = []
    for artist in artist_list:
        data = {
            'id': artist.id,
            'name':  artist.name,
            'num_upcoming_shows': artist.num_upcoming_shows
        }
        results_list.append(data)

    response = {
        'count': len(artist_list),
        'data': results_list
    }
    return render_template('pages/search_artists.html', results=response, search_term=search_str)


# Read individual artist
@bp.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
    artist = Artist.query.get(artist_id)
    past_list = []
    upcoming_list = []
    up_entry = {}
    entry = {}
    past_shows = 0
    upcoming_shows = 0
    shows = artist.shows
    for show in shows:
        if (show.start_time > datetime.now()):
            upcoming_shows += 1
            up_entry = {
                "venue_id": show.venue_id,
                "venue_name": show.venue_name,
                "venue_image_link": show.venue_image_link,
                "start_time": show.start_time.strftime('%m/%d/%Y, %H:%M')
            }
            upcoming_list.append(up_entry)
        elif (show.start_time < datetime.now()):
            past_shows += 1
            entry = {
                "venue_id": show.venue_id,
                "venue_name": show.venue_name,
                "venue_image_link": show.venue_image_link,
                "start_time": show.start_time.strftime('%m/%d/%Y, %H:%M')
            }
            past_list.append(entry)
    # string formatting
    artist.genres = format_genres(artist.genres)
    data = {
        "id": artist.id,
        "name": artist.name,
        "genres": artist.genres.split(','),
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


# Update Artists: Display Form
@bp.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    artist = Artist.query.get(artist_id)
    form = ArtistForm(request.form)
    return render_template('forms/edit_artist.html', form=form, artist=artist)


# Update Artists: Posting form
@bp.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    form = ArtistForm(request.form)
    print(form.image_link.data)
    result = update(db, Artist, artist_id, {
        "name": form.name.data,
        "genres": form.genres.data,
        "city": form.city.data,
        "state": form.state.data,
        "phone": form.phone.data,
        "facebook_link": form.facebook_link.data,
        "website": form.website.data,
        "seeking_venue": form.seeking_venue.data,
        "seeking_description": form.seeking_description.data,
        "image_link": form.image_link.data

    }, 'Successfully updated artist information!',
        'Error. Could not update artist information.')
    flash(result)
    return redirect(url_for('artists.show_artist', artist_id=artist_id))


# Delete Artist
@ bp.route('/artists/<int:id>', methods=['DELETE'])
def delete_artist(id):
    artist = Artist.query.get(id)
    flash('deleting', artist)  # TODO: debug flash
    print('deleting', artist)
    name = artist.name
    result = delete(db, artist, f'Artist {name} was successfully deleted!',
                    f'Artist {name} could not deleted')
    flash(result)
    return render_template('pages/artists.html')
