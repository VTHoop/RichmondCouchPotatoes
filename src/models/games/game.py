from src.common.database import Database


__author__ = 'hooper-p'

import uuid

import src.models.games.constants as GameConstants


class Game(object):
    def __init__(self, date, time, venue, home_team, away_team, _id=None):
        self.date = date
        self.time = time
        self.venue = venue
        self.home_team = home_team
        self.away_team = away_team
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "{} plays {} on {} at {} at {}".format(self.home_team, self.away_team, self.date, self.time, self.venue)

    def save_to_mongo(self):
        Database.update(GameConstants.COLLECTION, {"_id": self._id}, self.json())

    def json(self):
        return {
            "date": self.date,
            "time": self.time,
            "venue": self.venue,
            "home_team": self.home_team,
            "away_team": self.away_team,
            "_id": self._id
        }

    @classmethod
    def get_game_by_id(cls, _id):
        return cls(**Database.find_one(GameConstants.COLLECTION, {"_id": _id}))

    @classmethod
    def get_games(cls):
        return [cls(**elem) for elem in Database.find(GameConstants.COLLECTION, {})]
