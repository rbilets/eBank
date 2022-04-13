from flask import make_response, render_template
from flask_login import current_user
from flask_restful import Resource

from src import db
from src.database.models import User, Wallet

headers = {'Content-Type': 'text/html'}


class Smoke(Resource):
    def get(self):
        if current_user.is_authenticated:
            wallets = db.session.query(Wallet).filter_by(owner_id=current_user.uid).all()
            return make_response(
                render_template('index.html', wallets=wallets), 200, headers)
        else:
            return make_response(
                render_template('login.html'), 200, headers)
        # return {'message': 'OK'}, 200
