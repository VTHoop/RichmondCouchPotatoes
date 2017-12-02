from src.app import app

__author__ = 'hooper-p'

app.run(debug=app.config['DEBUG'], port=4990)