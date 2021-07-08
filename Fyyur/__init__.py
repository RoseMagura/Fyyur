from Fyyur.models.artist import Artist
from Fyyur.models.venue import Venue
from Fyyur.models.show import Show
from Fyyur.routes import artists, venues, shows
from flask import Flask
from flask_moment import Moment
from flask_migrate import Migrate
from Fyyur.extensions import db
import dateutil.parser
import babel
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')

db.init_app(app)

migrate = Migrate(app, db)


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime


@app.route('/')
def hello():
    return 'Hello, World! App is running'


# apply the blueprints to the app
app.register_blueprint(artists.bp)
app.register_blueprint(venues.bp)
app.register_blueprint(shows.bp)


#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#


# Default port:
if __name__ == '__main__':
    app.run()
