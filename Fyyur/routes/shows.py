from Fyyur.utilities.helper_func import delete, insert, setup_show_form, update
from flask import Blueprint, render_template, request, flash
from Fyyur.models.artist import Artist
from Fyyur.models.venue import Venue
from Fyyur.models.show import Show
from datetime import datetime
from Fyyur.extensions import db
from forms import ShowForm


bp = Blueprint("shows", __name__)


# Create Show: Display form
@bp.route('/shows/create')
def create_shows():
    form = setup_show_form(ShowForm())
    return render_template('forms/new_show.html', form=form)


# Create Show: Posting form
@bp.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    form = ShowForm()
    num_shows = Show.query.count()
    artist = Artist.query.get(form.artist_id.data)
    venue = Venue.query.get(form.venue_id.data)
    show = Show(
        id=num_shows + 1,
        artist_id=form.artist_id.data,
        artist_name=artist.name,
        artist_image_link=artist.image_link,
        venue_id=form.venue_id.data,
        venue_name=venue.name,
        venue_image_link=venue.image_link,
        start_time=form.start_time.data
    )
    if (form.start_time.data > datetime.now()):
        artist.num_upcoming_shows += 1
        venue.num_upcoming_shows += 1
        insert(db, artist)
        insert(db, venue)
    result = insert(db, show)
    flash(result)
    return render_template('pages/home.html')


# Read All Shows
@bp.route('/shows')
def shows():
  # displays list of all shows at /shows
    shows = Show.query.all()
    return render_template('pages/shows.html', shows=shows)


# Read Individual Show
@bp.route('/shows/<int:id>')
def display_individual_show(id):
    show = Show.query.get(id)
    return render_template('pages/show_details.html', show=show)


# Render form for editing show
@bp.route('/shows/<int:id>/edit', methods=['GET'])
def edit_show(id):
    show = Show.query.get(id)
    form = setup_show_form(ShowForm(), show.artist_id, show.venue_id)
    return render_template('forms/edit_show.html', form=form, show=show)


# Update Show
@bp.route('/shows/<int:id>/edit', methods=['POST'])
def edit_show_submission(id):
    form = ShowForm(request.form)
    artist = Artist.query.get(form.artist_id.data)
    venue = Venue.query.get(form.venue_id.data)
    result = update(db, Show, id, {
        "artist_id": form.artist_id.data,
        "artist_name": artist.name,
        "artist_image_link": artist.image_link,
        "venue_id": form.venue_id.data,
        "venue_name": venue.name,
        "venue_image_link": venue.image_link,
        "start_time": form.start_time.data
    }, 'Successfully updated show!', 'Error with updating show.')
    flash(result)
    return render_template('pages/home.html')


# Delete Show
@bp.route('/shows/<int:id>', methods=['DELETE'])
def delete_show(id):
    show = Show.query.get(id)
    flash(show)  # TODO: debug flash
    print(show)
    delete(db, show, 'Show was successfully deleted!', 'Show could not deleted.')
    return render_template('pages/shows.html')
