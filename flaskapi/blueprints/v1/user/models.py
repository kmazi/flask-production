"""Define auth models."""

from flaskapi.blueprints.v1.base_model import Base
from flaskapi.blueprints.v1.user.util import CPU_FACTOR, ITERATIONS, REPEAT, hash_password
from flaskapi.core.extensions import db


class User(Base, db.Model):
    """Define user model."""
    __tablename__ = "users"
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    username = db.Column(db.String(100))
    email = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(100))
    address = db.Column(db.String(200))
    lastlogin_at = db.Column(db.DateTime)
    # Relationships
    security = db.relationship('Security', uselist=False, 
                               back_populates='user')

    def save(self, **kwargs):
        # Hash user password
        security: Security = kwargs.get('security')
        if security.password:
            hashed_pass, salt = hash_password(password=security.password,
                                              n=security.n, r=security.r, 
                                              p=security.p)

        self.password = hashed_pass
        self.salt = salt

        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return f'{self.username}'


class Security(Base, db.Model):
    __table_name__ = 'securities'
    
    user_email = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    salt = db.Column(db.String(), nullable=False)
    n = db.Column(db.Integer, nullable=False, default=ITERATIONS)
    r = db.Column(db.Integer, nullable=False, default=CPU_FACTOR)
    p = db.Column(db.Integer, nullable=False, default=REPEAT)
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.id', name='users_securities_user_idfk1'))
    # Relationships
    user = db.relationship('User', uselist=False, back_populates='security')

    def __repr__(self):
        return f'Security for id={self.user_id}'
    