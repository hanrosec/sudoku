import os

HOST = os.environ.get('DB_HOST')
PORT = 3306
USER = 'root'
# PASSWORD = 'eyFg6nch*MGo^pD&8C7R'
PASSWORD = os.environ.get('DB_PASSWORD')
DATABASE = 'sudoku'
SECRET_KEY = 'dev'