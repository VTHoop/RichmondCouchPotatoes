from src.common.database import Database
from src.models.games.game import Game
from src.models.players.player import Player

import src.models.players.constants as PlayerConstants

__author__ = 'hooper-p'

import uuid

import src.models.attendance.constants as AttendanceConstants


class Attendance(object):
    def __init__(self, game, player, attendance='No', beverages='No', _id=None):
        self.game = Game.get_game_by_id(game)
        self.player = Player.get_player_by_id(player['_id'])
        self.attendance = attendance
        self.beverages = beverages
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "{} says {} to game on {}".format(self.player.name, self.attendance, self.game.date)

    def save_to_mongo(self):
        Database.update(AttendanceConstants.COLLECTION, {"_id": self._id}, self.json())

    def json(self):
        return {
            "game": self.game._id,
            "player": self.player.json(),
            "attendance": self.attendance,
            "beverages": self.beverages,
            "_id": self._id
        }

    @classmethod
    def get_all_attendance(cls):
        return [cls(**elem) for elem in Database.find(AttendanceConstants.COLLECTION, {})]

    @classmethod
    def get_attendance_by_game(cls, game):
        all_players = [cls(**elem) for elem in Database.find_and_sort(AttendanceConstants.COLLECTION, {"game": game},
                                                                      [("attendance", -1), ("player.number", 1),
                                                                       ("player.name", 1)])]
        for player in all_players[:]:
            if player.player.name in PlayerConstants.players_to_remove:
                all_players.remove(player)
        return all_players

    @classmethod
    def yes_attendance_by_game(cls, game):
        return [cls(**elem) for elem in
                Database.find(AttendanceConstants.COLLECTION, {"game": game, "attendance": "Yes"})]

    @staticmethod
    def build_first():
        players = Player.get_players()
        games = Game.get_games()
        for game in games:
            for player in players:
                Attendance(game._id, player._id).save_to_mongo()
