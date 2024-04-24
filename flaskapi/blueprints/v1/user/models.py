"""Define auth models."""

from werkzeug.exceptions import BadRequest

from flaskapi.blueprints.v1.base_model import Base
from flaskapi.blueprints.v1.user.util import (CPU_FACTOR, ITERATIONS, REPEAT,
                                              hash_password)
from flaskapi.core.extensions import db


class Security(Base, db.Model):
    __tablename__ = 'securities'
    password = db.Column(db.String())
    salt = db.Column(db.String())
    n = db.Column(db.Integer, default=ITERATIONS)
    r = db.Column(db.Integer, default=CPU_FACTOR)
    p = db.Column(db.Integer, default=REPEAT)
    # Relationships
    user = db.relationship('User', uselist=False, back_populates='security')

    def __repr__(self):
        return f'Security for id={self.user_id}'
    
    
class User(Base, db.Model):
    """Define user model."""
    __tablename__ = "users"
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    username = db.Column(db.String())
    email = db.Column(db.String())
    phone_number = db.Column(db.String())
    address = db.Column(db.String())
    lastlogin_at = db.Column(db.DateTime)
    security_id = db.Column(db.Integer, db.ForeignKey(
        'securities.id', name='user_security_id_fk1'))
    # Relationships
    security = db.relationship('Security', uselist=False, 
                               back_populates='user')

    def save(self, **kwargs):
        # Hash user password
        try:
            password = kwargs.pop('password')
        except KeyError:
            raise BadRequest("No password specified!.")
        # Create User security
        security = Security()
        hashed_pass, salt = hash_password(password=password,
                                          n=security.n, r=security.r, 
                                          p=security.p)
        security.password = hashed_pass
        security.salt = salt
        # Create User
        for key, val in kwargs:
            if val is not None:
                setattr(self, key, val)
                
        db.session.add(self)
        db.session.add(security)
        db.session.commit()
        return self

    def __repr__(self):
        return f'{self.username}'
    