from flask import Blueprint, render_template
from model import Person

personBluePrint = Blueprint('personer', __name__,
                        template_folder='templates')

@personBluePrint.route('/personer')
def personlista():
    personer = Person.query.all()
    return render_template('personer/index.html',Items=personer)

@personBluePrint.route('/personer/edit/<id>')
def personEdit(id):
    personer = Person.query.all()
    return render_template('personer/index.html',Items=personer)


@personBluePrint.route('/personer/new')
def personNew():
    personer = Person.query.all()
    return render_template('personer/index.html',Items=personer)

