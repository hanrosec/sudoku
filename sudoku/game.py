# Plik zawierający blueprinty związane z grą: game, add_to_leaderbaord

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from hashlib import sha512

from .auth import login_required
from .db import get_db
from .sudoku import generate_puzzle, parse_board, DIFFICULTIES
import numpy as np

bp = Blueprint('game', __name__, url_prefix="/game")

@bp.route("", methods=('GET', 'POST'))
@login_required
def game():
    """
    funkcja tworzaca endpoint /game
    parametr diff przyjmuje wartosci typu int (0, 1, 2, 3) i ustawia na jego podstawie poziom trudnosci gry
    funkcja wysyla do uzytkownika hash rozwiazanego sudoku i nierozwiazane sudoku (list[list[int]])
    """
    diff = request.args.get('diff', type=int, default=1)
    print(diff is int)
    if request.method == 'GET':
        try:
            assert diff in DIFFICULTIES
        except AssertionError:
            diff = 1
        solution, puzzle = generate_puzzle(difficulty=diff)
        
        puzzle_arr = np.array(puzzle)
        puzzle_arr_splitted = []

        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                puzzle_arr_splitted.append(puzzle_arr[i:i+3, j:j+3])
                
        solution_hash = sha512(parse_board(solution).encode()).hexdigest()
        parsed_puzzle = parse_board(puzzle)
        g.solution_hash = solution_hash
        g.parsed_puzzle = parsed_puzzle
        # g.puzzle = puzzle
        g.puzzle_arr = puzzle_arr_splitted
    
    return render_template('game.html')


@bp.route("/add_to_leaderboard", methods=('GET', 'POST'))
@login_required
def add_to_leaderboard():
    """
    przyjmuje w zapytaniu POST:
      - czas w milisekundach
      - hash rozwiązania użytkownika
      - hash rozwiązania wygenerowanego przez serwer
      - suma kontrolna jak: sha512(czas + hash rozwiazania użytkownika + hash rozwiązania wygenerowanego przez serwer)
    funkcja porównuje hash rozwiązania użytkownika z rozwiązaniem serwera
    jeśli hashe się zgadzają to generowany jest hash kontrolny i jest porównywany z hashem wygenerowanym przez użytkownika
    jeśli te hashe się zgadzają to zapis wynik do bazy
    gdzie score = czas w milisekundach
    """
    if request.method == 'POST':
        data = request.form
        print(data)
        if data['time'] is None or \
            data['user_hash'] is None or \
            data['system_hash'] is None or \
            data['control_hash'] is None:
                flash("Serwer nie może przetworzyć zapytania")
        else:
            time = data['time']
            user_hash = data['user_hash']
            system_hash = data['system_hash']
            if user_hash != system_hash:
                flash("Rozwiązanie nie jest prawidłowe")
            else:
                db = get_db()
                user_control_hash = data['control_hash']
                system_control_hash = sha512((str(time) + user_hash + system_hash).encode()).hexdigest()
                if user_control_hash == system_control_hash:
                    db.execute(
                        'INSERT INTO leaderboard (user_id, score) VALUES (?, ?);',
                        (g.user['id'], time)
                    )
                    db.commit()
                    flash("Zapisano wynik!")
                else:
                    flash("Suma kontrolna gry się nie zgadza. Zapytanie prawdopodobnie zostało zmienione")
        return redirect(url_for("game.leaderboard"))

@bp.route("/leaderboard", methods=('GET', 'POST'))
def leaderboard():
    if request.method == 'GET':
        db = get_db()
        leaderboard_data = db.execute(
            'SELECT users.username, leaderboard.score FROM leaderboard JOIN users ON leaderboard.user_id = users.id ORDER BY score ASC'
        ).fetchall()
        g.leaderboard = [{"username": x['username'], "score": x['score']} for x in leaderboard_data]
        
        return render_template('leaderboard.html')