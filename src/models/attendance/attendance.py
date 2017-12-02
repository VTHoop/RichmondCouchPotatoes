from src.common.database import Database
from src.models.games.game import Game
from src.models.players.player import Player

__author__ = 'hooper-p'

import uuid

import src.models.attendance.constants as AttendanceCosntants


class Attendance(object):
    def __init__(self, game, player, attendance='No', _id=None):
        self.game = Game.get_game_by_id(game)
        self.player = Player.get_player_by_id(player)
        self.attendance = attendance
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "{} says {} to game on {}".format(self.player.name, self.attendance, self.game.date)

    def save_to_mongo(self):
        Database.update(AttendanceCosntants.COLLECTION, {"_id": self._id}, self.json())

    def json(self):
        return {
            "game": self.game._id,
            "player": self.player._id,
            "attendance": self.attendance,
            "_id": self._id
        }

    @classmethod
    def get_attendance_by_game(cls, game):
        return [cls(**elem) for elem in Database.find(AttendanceCosntants.COLLECTION, {"game": game})]

    @classmethod
    def yes_attendance_by_game(cls, game):
        return [cls(**elem) for elem in
                Database.find(AttendanceCosntants.COLLECTION, {"game": game, "attendance": "Yes"})]

    @staticmethod
    def build_first():
        players = Player.get_players()
        games = Game.get_games()
        for game in games:
            for player in players:
                Attendance(game._id, player._id).save_to_mongo()
