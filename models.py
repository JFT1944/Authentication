"""Models for Cupcake app."""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, UniqueConstraint, Index
from flask_bcrypt import Bcrypt
db = SQLAlchemy()
bcrypt = Bcrypt
def connect_db(app):

    db.app = app
    db.init_app(app)

class User(db.Model):
    '''User'''

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True,)
                    
    username = db.Column(db.String(20), nullable=False, unique=True)

    password = db.Column(db.String(), nullable=False, unique=False)
    
    email = db.Column(db.String(50), nullable=False, unique=False)

    first_name = db.Column(db.String(30), nullable=False)
    
    last_name = db.Column(db.String(30), nullable=False)


class Feedback(db.Model):
    '''Feedback'''

    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True,)
                    
    title = db.Column(db.String(100), nullable=False)

    content = db.Column(db.String(), nullable=False)
    
    username = db.Column(db.String(), db.ForeignKey('user.username'))
# ==========================================================================================

    # @classmethod
    # def register(cls, username, pwd):
    #     """Register user w/hashed password & return user."""
    #     print(cls)
    #     hashed = bcrypt.generate_password_hash(bcrypt, f"b'{pwd}")
    #     # turn bytestring into normal (unicode utf8) string
    #     hashed_utf8 = hashed.decode("utf8")

    #     # return instance of user w/username and hashed pwd
    #     return cls(username=username, password=hashed_utf8)
   
# ==========================================================================================

    # @classmethod
    # def authenticate(cls, username, pwd):
    #     """Validate that user exists & password is correct.

    #     Return user if valid; else return False.
    #     """
    #     print(pwd)
    #     u = User.query.filter_by(username=username).first()
    #     #  print(bcrypt.check_password_hash( u.password, pwd))

    #     if u and bcrypt.check_password_hash(u.password, pwd):
    #         # return user instance
    #         return u
    #     else:
    #        return False