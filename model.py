from flask_sqlalchemy import SQLAlchemy
from flask_security import current_user, Security, SQLAlchemySessionUserDatastore, auth_required, hash_password, roles_required, login_required, verify_password, login_user, UserMixin, RoleMixin, auth_token_required

db=SQLAlchemy()


role_user = db.Table('role_user',
    db.Column('UserID', db.Integer, db.ForeignKey('user.ID')),
    db.Column('roleID', db.Integer, db.ForeignKey('role.ID')))

class role(db.Model,RoleMixin):
    __tablename__ = ('role')
    ID = db.Column(db.Integer, autoincrement = True, primary_key = True)
    name = db.Column(db.String, unique = True, nullable = False)
    description = db.Column(db.String)
    
class user(db.Model,UserMixin):
    __tablename__ = ("user")
    ID = db.Column(db.Integer, autoincrement=True, primary_key=True)
    Name = db.Column(db.String, nullable = False)
    Email = db.Column(db.String, unique= True, nullable=False)
    Password = db.Column(db.String, nullable = False)
    active = db.Column(db.Boolean)
    fs_uniquifier = db.Column(db.String, unique = True, nullable = False)
    roles = db.relationship("role", secondary = role_user ,backref = db.backref('users'))
    
class section(db.Model):
    __tablename__ = ("section")
    ID = db.Column(db.Integer, autoincrement=True, primary_key=True)
    Title = db.Column(db.String, nullable = False, unique = True)
    Date = db.Column(db.String, nullable = False)
    Description = db.Column(db.String)

class book(db.Model):
    __tablename__ = ("book")
    ID = db.Column(db.Integer, autoincrement=True, primary_key=True)
    Title = db.Column(db.String, nullable = False, unique = True)
    Author = db.Column(db.String, nullable = False)
    Section = db.Column(db.String, db.ForeignKey('section.ID'))


class issuebook(db.Model):
    __tablename__ = ("issuebook")
    ID = db.Column(db.Integer, autoincrement=True, primary_key=True)
    bid=db.Column(db.Integer,db.ForeignKey(book.ID),nullable=False)
    uid=db.Column(db.Integer,db.ForeignKey(user.ID),nullable=False)
    doi=db.Column(db.String,default = None)
    dor=db.Column(db.String, default = None)
    cstatus=db.Column(db.String,nullable=False)
    books = db.relationship("book",backref="issues")
    

class review(db.Model):
    __tablename__ = ("review")
    ID = db.Column(db.Integer,autoincrement = True, primary_key=True)
    uid = db.Column(db.Integer,  db.ForeignKey('user.ID') )
    bid = db.Column(db.Integer, db.ForeignKey('book.ID'))
    Review = db.Column(db.Integer)





def createdata(user_datastore):
    user_datastore.find_or_create_role(name="admin",description="Handles the Library")
    user_datastore.find_or_create_role(name="user",description="Uses the Library")
    if not user_datastore.find_user(Email="drashti@gmail.com"):
        user_datastore.create_user(Name="Drashti",Email="drashti@gmail.com",Password="drashti",roles=["user","admin"])
    db.session.commit()