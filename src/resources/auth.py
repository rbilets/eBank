import datetime
import json

from flask import request, jsonify, g, make_response, render_template, url_for
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from flask_restful import Resource
from flask_httpauth import HTTPBasicAuth
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import redirect

from src import db, app
from src.database.models import User, Wallet
from src.schemas.users import UserSchema

auth = HTTPBasicAuth()
headers = {'Content-Type': 'text/html'}

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'authlogin'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(uid):
    return User.query.get(uid)


class AuthRegister(Resource):
    user_schema = UserSchema()

    def get(self):
        return make_response(render_template('register.html'), 200, headers)

    def post(self):
        try:
            d = json.loads(json.dumps(request.get_json()))
            user = User(
                username=d['username'],
                first_name=d['first_name'],
                last_name=d['last_name'],
                email=d['email'],
                password=d['password']
            )
            print(user)
        except ValidationError as e:
            return {'message': str(e)}, 400
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {'message': 'Such user exists'}, 409
        return make_response(render_template('login.html'), 200, headers)


class AuthLogin(Resource):
    def get(self):
        return make_response(render_template('login.html'), 200, headers)

    def post(self):
        d = json.loads(json.dumps(request.get_json()))
        username = d['username']
        password = d['password']
        user = db.session.query(User).filter_by(username=username).first()
        print(user)
        wallets = db.session.query(Wallet).filter_by(owner_id=user.uid).all()

        if verify_password(username, password):
            login_user(user)
            if not wallets:
                return make_response(render_template('profile.html', user=current_user, wallets=[]), 200, headers)

            return make_response(render_template('profile.html', user=current_user, wallets=wallets), 200, headers)
        else:
            return make_response(render_template('login.html'), 401, headers)


class Profile(Resource):
    def get(self):
        wallets = db.session.query(Wallet).filter_by(owner_id=current_user.uid).all()
        return make_response(render_template('profile.html', user=current_user, wallets=wallets), 200, headers)

class AuthLogout(Resource):
    @login_required
    def get(self):
        logout_user()
        return redirect(url_for('smoke'))


@auth.verify_password
def verify_password(username, password):
    user = db.session.query(User).filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return False
    g.user = user
    return True
