from flask import Blueprint, render_template, request

from src.models.attendance.attendance import Attendance

__author__ = 'hooper-p'

attendance_blueprint = Blueprint('attendance', __name__)


@attendance_blueprint.route('/<string:game_id>', methods=['GET', 'POST'])
def view_game(game_id):
    if request.method == 'POST':
        attendance = Attendance.get_attendance_by_game(game_id)
        for a in attendance:
            a.attendance = request.form['attendance' + str(a._id)]
            a.save_to_mongo()

    attendance = Attendance.get_attendance_by_game(game_id)
    how_many = Attendance.yes_attendance_by_game(game_id)
    return render_template("attendance/game_attendance.html", attendance=attendance, how_many=len(how_many))