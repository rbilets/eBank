import random
import uuid

# import bcrypt
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

from src import db
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata
Base.query = db.session.query_property()

class User(Base, UserMixin):
    __tablename__ = 'users'

    uid = db.Column(db.String, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    wallets = db.relationship('Wallet', backref='owner')

    def __init__(self, email, username, password, first_name, last_name, is_admin=False):
        self.uid = str(uuid.uuid4())
        self.email = email
        self.username = username
        self.password = generate_password_hash(password)
        self.first_name = first_name
        self.last_name = last_name
        self.is_admin = is_admin

    def get_id(self):
        return self.uid

    def __repr__(self):
        return f"User({self.email}, {self.username}, {self.first_name}, {self.last_name})"


class Wallet(Base):
    __tablename__ = 'wallets'

    uid = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    funds = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String, db.ForeignKey('users.uid'))

    def __init__(self, name, funds, owner_id):
        card_num = str(random.randint(1000000000000000, 9999999999999999))
        self.uid = card_num[0:4] + '-' + card_num[4:8] + '-' + card_num[8:12] + '-' + card_num[12:16]
        self.name = name
        self.funds = funds
        self.owner_id = owner_id

    def __str__(self):
        return f"Wallet ID    : {self.uid}\n" \
               f"Name         : {self.name}\n" \
               f"Funds        : {self.funds}\n" \
               f"Owner        : {self.owner_id}\n"

    def to_dict(self):
        return {
            'uid': self.uid,
            'name': self.name,
            'funds': self.funds,
            'owner_id': self.owner_id
        }


class Transaction(Base):
    __tablename__ = 'transactions'

    uid = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    from_wallet_id = db.Column(db.String, ForeignKey('wallets.uid'))
    to_wallet_id = db.Column(db.String, ForeignKey('wallets.uid'))
    status = db.Column(db.Boolean, nullable=False)

    def __init__(self, amount, from_wallet_id, to_wallet_id):
        self.amount = amount
        self.from_wallet_id = from_wallet_id
        self.to_wallet_id = to_wallet_id

    def __str__(self):
        return f"Transaction ID  : {self.uid}\n" \
               f"From wallet     : {self.from_wallet_id}\n" \
               f"To wallet       : {self.to_wallet_id}\n" \
               f"Amount          : {self.amount}\n" \
               f"Status          : {self.status}\n"

    def to_dict(self):
        return {
            'uid': self.uid,
            'amount': self.amount,
            'from_wallet_id': self.from_wallet_id,
            'to_wallet_id': self.to_wallet_id,
            'status': self.status
        }
