from src.models.attendance.attendance import Attendance

__author__ = 'hooper-p'

from flask import Flask, render_template
from src.common.database import Database

from src.models.players.player import Player
from src.models.games.game import Game

from src.models.attendance.views import attendance_blueprint

app = Flask(__name__)
app.config.from_object('src.config')
app.secret_key = '123'

app.register_blueprint(attendance_blueprint, url_prefix='/attendance')


@app.before_first_request
def init_db():
    Database.initialize()


@app.route('/')
def home():
    Game.update_games()
    # Player.update_players()
    # Attendance.build_first()
    # return render_template('base.html')
    games = Game.get_games()
    attendance = Attendance.get_all_attendance()
    for a in attendance:
        a.save_to_mongo()

    return render_template('home.html', games=games)


