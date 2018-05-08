import uuid
from bs4 import BeautifulSoup
import requests

from src.common.database import Database
import src.models.players.constants as PlayerConstants

__author__ = 'hooper-p'


class Player(object):
    def __init__(self, name, number=None, _id=None):
        self.name = name
        self.number = number
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "{} has number {}".format(self.name, self.number)

    def save_to_mongo(self):
        Database.update(PlayerConstants.COLLECTION, {"_id": self._id}, self.json())

    def json(self):
        return {
            "name": self.name,
            "number": self.number,
            "_id": self._id
        }

    @staticmethod
    def update_players():
        link = "https://richmondskating.ezleagues.ezfacility.com/teams/2200008/Coach-Potatoes.aspx"
        request = requests.get(link)
        content = request.content

        soup = BeautifulSoup(content, "html.parser")

        roster = soup.find("table", {"id": "ctl00_C_gridRoster"})

        roster_rows = roster.find_all("tr", {"class": ["RowStyle", "AlternateRowStyle"]})

        for rr in roster_rows:
            player_info = rr.findChildren()
            name = player_info[1].text
            number = player_info[2].text
            Player(name, number).save_to_mongo()

    @classmethod
    def get_player_by_id(cls, _id):
        return cls(**Database.find_one(PlayerConstants.COLLECTION, {"_id": _id}))

    @classmethod
    def get_players(cls):
        return [cls(**elem) for elem in Database.find(PlayerConstants.COLLECTION, {})]