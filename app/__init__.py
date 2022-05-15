from flask import Flask, session
from flask_session import Session
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)
Session(app)

from app import routes