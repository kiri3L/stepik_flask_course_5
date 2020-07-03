import os
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from src.models import db
from src.cli_commands import create

app = Flask(__name__, template_folder='templates')
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'hui'
db.init_app(app)
migrate = Migrate(app, db)
app.cli.add_command(create)

from src.admin import admin
admin.init_app(app)
from src.views import *

if __name__ == '__main__':
    app.run()
