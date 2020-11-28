import dash_bootstrap_components as dbc
import flask
from flask import request, send_file, jsonify
import dash
from flask import send_file
from sqlalchemy import create_engine, ForeignKey
from flask_sqlalchemy import SQLAlchemy
import cv2
import os
import numpy as np


server = flask.Flask(__name__)

# начальная страница
@server.route('/')
def index():
    return 'Hello Flask app'


# подключаем dash
app = dash.Dash(
    __name__,
    server=server,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    # meta_tags для отображения на разных размерах экранов
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ], suppress_callback_exceptions=True
)

