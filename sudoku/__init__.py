import os

from flask import Flask, render_template

def create_app(test_config=None):
    # Utworzenie i konfiguracja aplikacji
    app = Flask(__name__)
    # app.config.from_mapping(
    #     SECRET_KEY='dev',
    #     DATABASE=os.path.join(app.instance_path, 'sudoku.sqlite'),
    # )
    
    if test_config is None:
        app.config.from_pyfile('config.py', silent=False)
    else:
        app.config.from_mapping(test_config)
    print(app.config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    print(app.config['HOST'])
    
    from . import db
    db.init_app(app)
    
    from . import auth
    from . import game
    app.register_blueprint(auth.bp)
    app.register_blueprint(game.bp)
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app

