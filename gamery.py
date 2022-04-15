from flask import Flask
import psycopg2

app = Flask(__name__)
app.config.from_pyfile('config.py')

connection = psycopg2.connect(
host=app.config['DB_HOST'],
database=app.config['DB_NAME'],
user=app.config['DB_USERNAME'],
password=app.config['DB_PASSWORD'])

from controllers.games_controller import *
from controllers.users_controller import *
from controllers.images_controller import *

if __name__ == '__main__':
    app.run(debug=True)
