from flask_sqlalchemy import SQLAlchemy
from flask_user import  UserMixin, UserManager
from datetime import datetime
db = SQLAlchemy()

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    namn = db.Column(db.String(80), unique=False, nullable=False)
    city = db.Column(db.String(80), unique=False, nullable=False)
    postalcode = db.Column(db.String(10), unique=False, nullable=False)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

    # User authentication information. The collation='NOCASE' is required
    # to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.
    email = db.Column(db.String(255), nullable=False, unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False, server_default='')

    # User information
    first_name = db.Column(db.String(100), nullable=False, server_default='')
    last_name = db.Column(db.String(100), nullable=False, server_default='')

    # Define the relationship to Role via UserRoles
    roles = db.relationship('Role', secondary='user_roles')

# Define the Role data-model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

# Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


user_manager = UserManager(None, db, User)  


def seedData():
    AddPersonIfNotExists("Stefan Holmberg", "13245", "Saltsjö-Boo")
    AddRoleIfNotExists("Admin")
    AddRoleIfNotExists("Customer")
    AddLoginIfNotExists("admin@example.com", "Hejsan123#",["Admin"])
    AddLoginIfNotExists("customer@example.com", "Hejsan123#",["Customer"])

def AddRoleIfNotExists(namn:str):
    if Role.query.filter(Role.name == namn).first():
        return
    role = Role()
    role.name = namn
    db.session.add(role)
    db.session.commit()


def AddLoginIfNotExists(email:str, passwd:str, roles:list[str]):
    if User.query.filter(User.email == email).first():
        return
    user = User()
    user.email=email
    user.email_confirmed_at=datetime.utcnow()
    user.password=user_manager.hash_password(passwd)    
    for roleName in roles:
        role = Role.query.filter(Role.name == roleName).first()
        user.roles.append(role)

    db.session.add(user)
    db.session.commit()



def AddPersonIfNotExists(namn:str, postal:str, city:str):
    if Person.query.filter(Person.namn == namn).first():
        return 
    person = Person()
    person.namn = namn
    person.postalcode = postal
    person.city = city
    db.session.add(person)
    db.session.commit()


  