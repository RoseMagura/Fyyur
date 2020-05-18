import os
from flask import Flask
SECRET_KEY = os.urandom(32)
from flask_sqlalchemy import SQLAlchemy
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))
from flask_sqlalchemy import SQLAlchemy


# Enable debug mode.
DEBUG = True

# Connect to the database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rosie:password@localhost:5432/fyyur'

# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgresql://rosie:password@localhost:5432/fyyur'
