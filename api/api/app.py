from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_api import status
import os

DB_NAME = 'cohereQA'

app = Flask(__name__, static_folder='static')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'images')

db = SQLAlchemy(app)


@app.before_first_request
def create_tables():
  db.create_all()


@app.route('/')
def home():
  return "Welcome to cohereQA", status.HTTP_200_OK


from views import *

if __name__ == '__main__':
  app.run(host='0.0.0.0')
