from flask import Flask
from flask_moment import Moment
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route('/')
def hello():
    return 'Hello, World!'

from Fyyur.routes import artists, venues, shows
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
