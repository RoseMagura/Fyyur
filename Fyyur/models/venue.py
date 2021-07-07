from app import db

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(120))
    genres = db.Column(db.String(120))
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

    def __repr__(self):
        return '<Show {} {}>'.format(self.id, self.name)