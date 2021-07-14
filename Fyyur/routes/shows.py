from flask import Blueprint, render_template, request, flash
from Fyyur.models.artist import Artist
from Fyyur.models.venue import Venue
from Fyyur.models.show import Show
from datetime import datetime
from Fyyur.extensions import db
from forms import *

bp = Blueprint("shows", __name__)

# Create Show: Display form
@bp.route('/shows/create')
def create_shows():
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


# Create Show: Posting form
@bp.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    form = ShowForm(request.form)
    num_shows = Show.query.count()
    artist = Artist.query.get(form.artist_id.data)
    venue = Venue.query.get(form.venue_id.data)
    try:
        show = Show(
            id=num_shows + 1,
            artist_id=form.artist_id.data,
            artist_name=artist.name,
            artist_image_link=artist.image_link,
            venue_id=form.venue_id.data,
            venue_name=venue.name,
            start_time=form.start_time.data
        )
        if (form.start_time.data > datetime.now()):
            artist.num_upcoming_shows += 1
            venue.num_upcoming_shows += 1
            db.session.add(artist, venue)
            db.session.commit()
        db.session.add(show)
        db.session.commit()
        # on successful db insert, flash success
        flash('Show was successfully listed!')
    except:
        db.session.rollback()
        # on unsuccessful db insert, flash an error instead.
        flash('An error occurred. Show could not be listed.')
    finally:
        db.session.close()
    return render_template('pages/home.html')


# Read All Shows
@bp.route('/shows')
def shows():
  # displays list of shows at /shows
  # num_shows should be aggregated based on number of upcoming shows per venue.
    shows = Show.query.all()
    return render_template('pages/shows.html', shows=shows)

# Read Individual Show
@bp.route('/shows/<int:id>')
def display_individual_show(id):
    show = Show.query.get(id)
    return render_template('pages/show_details.html', show=show)


#TODO: Update Show
# Render form for editing show
@bp.route('/shows/<int:id>/edit', methods=['GET'])
def edit_show(id):
    form = ShowForm(request.form)
    show = Show.query.get(id)
    return render_template('forms/edit_show.html', form=form, show=show)
# @bp.route('/shows/<int:id>/edit', methods=['POST'])

# Delete Show
@bp.route('/shows/<int:id>', methods=['DELETE'])
def delete_show(id):
    show = Show.query.get(id)
    flash(show) # TODO: debug flash
    print(show)
    try:
        db.session.delete(show)
        print('Show was successfully deleted!')
        flash('Show was successfully deleted!')
    except:
        print("Show could not be deleted.")
        flash('Show could not deleted.')
        db.session.rollback()
    finally:
        db.session.commit()
    return render_template('pages/shows.html')


