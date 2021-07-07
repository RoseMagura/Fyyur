import os
from dotenv import load_dotenv
from os.path import join, dirname
from flask import Flask
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Enable debug mode.
DEBUG = True

# Connect to the database
SQLALCHEMY_DATABASE_URI = f"postgresql://{os.environ.get('PG_USER')}:{os.environ.get('PG_PASSWORD')}@{os.environ.get('PG_HOST')}:5432/{os.environ.get('PG_DATABASE')}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
