from flask import current_app, g
import psycopg2
from config import DB_NAME, DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT

def get_db():
    if 'db' not in g:
        print("Opening new DB connection")
        g.db = psycopg2.connect(current_app.config['DATABASE_URL'])
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        print("Closing connection")
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)

