from flask import Blueprint, render_template, url_for, request, flash, redirect
from Fyyur.models.artist import Artist
from Fyyur.models.venue import Venue
from Fyyur.models.show import Show
from datetime import datetime
from Fyyur.extensions import db
from forms import *
from Fyyur.utilities.helper_func import format_genres

bp = Blueprint("artists", __name__)


# Read artists
@bp.route('/artists')
def artists():
    data = Artist.query.all()
    return render_template('pages/artists.html', artists=data)


@bp.route('/artists/search', methods=['GET', 'POST'])
def search_artists():
    # Search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
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


#  Update Artists
@bp.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    artist = Artist.query.get(artist_id)
    form = ArtistForm(request.form)
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@bp.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    form = ArtistForm(request.form)
    try:
        db.session.query(Artist).filter(Artist.id == artist_id).\
            update({
                "name": form.name.data,
                "genres": form.genres.data,
                "city": form.city.data,
                "state": form.state.data,
                "phone": form.phone.data,
                "facebook_link": form.facebook_link.data,
            }, synchronize_session="fetch")
        db.session.commit()
        flash('Updated artist information')
    except:
        db.session.rollback()
        flash('Error. Could not update artist information')
    finally:
        db.session.close()
    return redirect(url_for('artists.show_artist', artist_id=artist_id))


# Create Artists
@bp.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@bp.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # insert form data as a new Venue record in the db, instead
    # modify data to be the data object returned from db insertion
    form = ArtistForm(request.form)
    print(form.genres.data, form.image_link.data)
    num_artists = Artist.query.count()
    artist = Artist(
        id=num_artists + 4,
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

    try:
        db.session.add(artist)
        # on successful db insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    except:
        # on unsuccessful db insert, flash an error
        flash('An error occurred. Artist ' +
              form.name + ' could not be listed.')
        db.session.rollback()
    finally:
        db.session.commit()
    return render_template('pages/home.html')


# Delete Artist
@bp.route('/artists/<int:id>', methods=['DELETE'])
def delete_artist(id):
    artist = Artist.query.get(id)
    flash('deleting', artist) # TODO: debug flash
    print('deleting', artist)
    name = artist.name
    try:
        db.session.delete(artist)
        print(f'Artist {name} was successfully deleted!')
        flash(f'Artist {name} was successfully deleted!')
    except:
        print(f"Artist {name} could not be deleted.")
        flash(f'Artist {name} could not deleted')
        db.session.rollback()
    finally:
        db.session.commit()
    return render_template('pages/artists.html')
