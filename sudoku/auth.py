# Plik zawierający blueprinty do autoryzacji: logowanie, rejestracja

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import mariadb

from werkzeug.security import check_password_hash, generate_password_hash
from .db import get_db
import re


bp = Blueprint('auth', __name__, url_prefix="/auth")

def validate_username(username) -> bool:
    """
    Nazwa użytkownika musi spełniać regex [A-Za-z0-9] i mieć mniej niż 50 znaków. Przeciwdziałanie sql injection
    """
    return bool(re.match(r"^\w+$", username)) and len(username) < 50

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        # pobranie nazwy uzytkownika i hasla z formularza do rejestracji
        username = request.form['username']
        password = request.form['password']

        # inicjalizacja bazy danych
        db = get_db()
        error = None
        
        if not username:
            error = "Podaj nazwę użytkownika"
        elif not password:
            error = "Podaj hasło"
        
        if not validate_username(username):
            error = "Nazwa użytkownika nie może zawierać tylko duże i małe litery oraz znak _ oraz musi mieć długość mniejszą niż 50 znaków"
        else:
            if error is None:
                try:
                    db.execute(
                        "INSERT INTO users (username, password) VALUES (?, ?)",
                        (username, generate_password_hash(password))
                    )
                except mariadb.IntegrityError:
                    error = f"Użytkownik o nazwie {username} już istnieje"
                else:
                    # w przypadku poprawnego zarejestrowania uzytkownik jest przekierowywany na strone logowania
                    return redirect(url_for("auth.login"))
    
        flash(error)
        
    return render_template("auth/register.html")

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = None

        if not validate_username(username):
            error = "Nazwa użytkownika nie może zawierać tylko duże i małe litery oraz znak _ oraz musi mieć długość mniejszą niż 50 znaków"
        else:
            if error is None:
                db.execute(
                    'SELECT * FROM users WHERE username = ?', (username, )
                )
                result = db.fetchone()
                
                if result is None:
                    user = None
                else:
                    user = result
                
            if user is None:
                error = 'Niepoprawna nazwa użytkownika'
            elif not check_password_hash(user['password'], password):
                error = 'Niepoprawne hasło'
            
            if error is None:
                print(f"{user['id']} logged in")
                session.clear()
                session['user_id'] = user['id']
                return redirect(url_for('game.game'))
        
        flash(error)
        
    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    
    if user_id is None:
        g.user = None
    else:
        get_db().execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        )
        result = get_db().fetchone()
        if result is None:
            g.user = None
        else:
            g.user = result

# funkcja ktora zapewnia, ze uzytkownik bedzie zalogowany przed dostepem do innych widokow
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
