import os
import random
from string import hexdigits

HOST = os.environ.get('DB_HOST')
PORT = 3306
USER = 'root'
PASSWORD = os.environ.get('DB_PASSWORD')
DATABASE = 'sudoku'
SECRET_KEY = ''.join(random.choice(hexdigits) for _ in range(32))