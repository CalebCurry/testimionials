from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

DB_NAME = os.environ.get('RDS_DB_NAME')
DB_USER = os.environ.get('RDS_USERNAME')
DB_PASSWORD = os.environ.get('RDS_PASSWORD')
DB_HOSTNAME = os.environ.get('RDS_HOSTNAME')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOSTNAME}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
from testimonials.models import Testimonial
db.create_all()

# testimonials
# NExB43BMwWBHqRDgiING

import testimonials.routes
