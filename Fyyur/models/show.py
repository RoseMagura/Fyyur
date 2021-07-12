from Fyyur.models.artist import Artist
from Fyyur.models.venue import Venue
from Fyyur.extensions import db


class Show(db.Model):
    __tablename__ = 'Show'
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime)
    artist_id = db.Column(db.Integer, db.ForeignKey(Artist.id))
    artist_name = db.Column(db.String(120))
    artist_image_link = db.Column(db.String(500))
    venue_id = db.Column(db.Integer, db.ForeignKey(Venue.id))
    venue_name = db.Column(db.String(120))
    venue_image_link = db.Column(db.String(500))

    def __repr__(self):
        return '<Show {} {}>'.format(self.artist_id, self.venue_id)
