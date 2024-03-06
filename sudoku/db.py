# import sqlite3
import mariadb

import click
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = mariadb.connect(
            host=current_app.config['HOST'],
            port=current_app.config['PORT'],
            user=current_app.config['USER'],
            password=current_app.config['PASSWORD'],
            database=current_app.config['DATABASE'],
            autocommit=True
        )
        # g.db.row_factory = mariadb.Row
        g.db = g.db.cursor(dictionary=True)
        
        
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    
    with current_app.open_resource('schemas/schema.sql') as f:
        db.execute(f.read().decode('utf8'))

@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Utworzono bazę danych')

def init_app(app):
    # jak aplikacja zakonczy odpowiedz zamyka baze danych
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)