from src.common.database import Database

__author__ = 'hooper-p'

import uuid
from bs4 import BeautifulSoup
import requests

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

    @staticmethod
    def update_games():
        # this is used to find the id within the href of the time element on the schedule
        find_str = 'games'

        link = "https://richmondskating.ezleagues.ezfacility.com/teams/2079371/Coach-Potatoes.aspx"
        request = requests.get(link)
        content = request.content

        soup = BeautifulSoup(content, "html.parser")

        schedule = soup.find("table", {"id": "ctl00_C_Schedule1_GridView1"})

        schedule_rows = schedule.find_all("tr", {"class": ["RowStyle", "AlternateRowStyle"]})

        for sr in schedule_rows:
            game_info = sr.find_all("td")
            date = game_info[0].a.text
            home_team = game_info[1].a.text
            away_team = game_info[3].a.text
            time = game_info[4].a.text
            venue = game_info[5].a.text
            id = game_info[4].a['href']

            # 8 digit number after "games/" is used as id for game
            slice_id = id[id.find(find_str)+6:id.find(find_str)+14]
            game = Database.find_one(GameConstants.COLLECTION, {"_id": slice_id})
            if game is None:
                Game(date, time, venue, home_team, away_team, slice_id).save_to_mongo()
            else:
                game.date = date
                game.home_team = home_team
                game.away_team = away_team
                game.time = time
                game.venue = venue
                game.save_to_mongo()

    @classmethod
    def get_game_by_id(cls, _id):
        return cls(**Database.find_one(GameConstants.COLLECTION, {"_id": _id}))

    @classmethod
    def get_games(cls):
        return [cls(**elem) for elem in Database.find(GameConstants.COLLECTION, {})]
