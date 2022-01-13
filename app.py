from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
from model import db, seedData
from configDebug import ConfigDebug
from personer.personpages import personBluePrint

 
app = Flask(__name__)
app.config.from_object(__name__ + '.ConfigDebug')

db.app = app
db.init_app(app)
migrate = Migrate(app,db)


app.register_blueprint(personBluePrint)

@app.route('/')
def index() -> str:
    return render_template('index.html')





if __name__  == "__main__":
    with app.app_context():
        upgrade()
        seedData()
    app.run()