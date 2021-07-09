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
from flask import render_template
import logging
from logging import Formatter, FileHandler
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
def index():
    return render_template('pages/home.html')


# apply the blueprints to the app
app.register_blueprint(artists.bp)
app.register_blueprint(venues.bp)
app.register_blueprint(shows.bp)


@app.errorhandler(404)
def not_found_error(error):
    # return render_template('errors/404.html'), 404
    return '404 Page Not Found'


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')


#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#


# Default port:
if __name__ == '__main__':
    app.run()
