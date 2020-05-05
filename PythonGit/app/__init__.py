import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_login import LoginManager

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///storage.db'

app.config.from_object('config')
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['UPLOAD_PATH'] = os.path.dirname(os.path.abspath(__file__)) + '/templates/uploads/'
#app.config['SERVER_NAME'] = "http://127.0.0.1:5000"
SERVER_NAME = "http://127.0.0.1:5000"


db = SQLAlchemy(app)
migrate = Migrate(app,db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

login_manager = LoginManager()
login_manager.init_app(app)

from app.models import tables
from app.controllers import default