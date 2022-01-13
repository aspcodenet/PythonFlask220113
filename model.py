from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    namn = db.Column(db.String(80), unique=False, nullable=False)
    city = db.Column(db.String(80), unique=False, nullable=False)
    postalcode = db.Column(db.String(10), unique=False, nullable=False)


def seedData():
    AddPersonIfNotExists("Stefan Holmberg", "13245", "Saltsjö-Boo")

def AddPersonIfNotExists(namn:str, postal:str, city:str):
    if Person.query.filter(Person.namn == namn).first():
        return 
    person = Person()
    person.namn = namn
    person.postalcode = postal
    person.city = city
    db.session.add(person)
    db.session.commit()