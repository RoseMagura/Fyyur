from datetime import datetime
from Fyyur.models.artist import Artist
from Fyyur.models.venue import Venue
from Fyyur.models.show import Show


def format_genres(genres):
    return genres.replace('{', '').replace('}', '').replace('"', '')


def setup_show_form(form, default_artist='', default_venue=''):
    form.artist_id.choices = [(a.id) for a in Artist.query.all()]
    if default_artist != '':
      form.artist_id.default = default_artist
      form.artist_id.data = default_artist
      form.artist_id.process([])

    form.venue_id.choices = [(v.id) for v in Venue.query.all()]
    if default_venue != '':
      form.venue_id.default = default_venue
      form.venue_id.data = default_venue
      form.venue_id.process([])
    return form


def setup_artist_form():
    return


def setup_venue_form():
    return
