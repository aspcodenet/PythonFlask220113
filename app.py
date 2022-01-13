from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
from model import db, seedData
from configDebug import ConfigDebug
from personer.personpages import personBluePrint
from model import User, user_manager
from flask_user import login_required, roles_required, current_user

 
app = Flask(__name__)
app.config.from_object(__name__ + '.ConfigDebug')

db.app = app
db.init_app(app)
migrate = Migrate(app,db)
user_manager.app = app
user_manager.init_app(app,db,User)

app.register_blueprint(personBluePrint)

@app.route('/')
def index() -> str:
    return render_template('index.html')


@app.route('/tjena')
@login_required
def index3() -> str:
    return "Tjena" + current_user.email


@app.route('/secret')
@roles_required("Admin")
def index2() -> str:
    return "secret"



if __name__  == "__main__":
    with app.app_context():
        upgrade()
        seedData()
    app.run()