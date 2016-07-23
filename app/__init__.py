from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object('config')
db = SQLAlchemy(app)

from app.controllers import controllers as controllers

db.create_all()
