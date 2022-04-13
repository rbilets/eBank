from functools import wraps
import json

from flask import request, g, render_template, make_response, url_for
from flask_httpauth import HTTPBasicAuth
from flask_login import current_user, login_required
from flask_restful import Resource
from marshmallow import ValidationError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import redirect

from src import db
from src.database.models import Wallet, User
from src.resources.auth import auth
from src.schemas.wallets import WalletSchema
headers = {'Content-Type': 'text/html'}


class WalletListApiGet(Resource):
    wallet_schema = WalletSchema()

    @login_required
    def get(self, uid=None):
        if current_user.is_admin:
            if not uid:
                wallets = db.session.query(Wallet).all()
                return make_response(render_template('wallets.html', wallets=wallets), 200, headers)
                # return [wallet.to_dict() for wallet in wallets], 200
            wallet = db.session.query(Wallet).filter_by(uid=uid).first()
            if not wallet:
                return {'message': 'Wallet not found'}, 404
            # return wallet.to_dict(), 200
            return make_response(render_template('wallets.html', wallets=[wallet]), 200, headers)

        elif not current_user.is_admin:
            if not uid:
                wallets = db.session.query(Wallet).filter_by(owner_id=current_user.uid).all()
                # return [wallet.to_dict() for wallet in wallets], 200
                return make_response(render_template('wallets.html', wallets=wallets), 200, headers)
            wallet = db.session.query(Wallet).filter_by(uid=uid).first()
            if not wallet:
                return {'message': 'Wallet not found'}, 404
            if wallet.owner_id != current_user.uid:
                return {'message': 'Access denied'}, 409
            # return wallet.to_dict(), 200
            return make_response(render_template('wallets.html', wallets=[wallet]), 200, headers)


class WalletListApiPost(Resource):
    wallet_schema = WalletSchema()

    @login_required
    def get(self):
        return make_response(render_template('walletCreate.html'), 200, headers)

    @login_required
    def post(self):
        d = json.loads(json.dumps(request.get_json()))
        print(d)
        try:
            wallet = Wallet(
                name=d['name'],
                funds=d['funds'],
                owner_id=d['owner_id']
            )
            if not db.session.query(User).filter_by(uid=wallet.owner_id).first():
                return {'message': 'Wrong data, User(owner_id) not found'}, 400
            elif not current_user.is_admin and (current_user.uid != wallet.owner_id or wallet.funds != 0):
                return {'message': 'Access denied'}, 409
        except ValidationError as e:
            return {'message': str(e)}, 400
        user_wallets = db.session.query(Wallet).filter_by(owner_id=wallet.owner_id).all()
        for w in user_wallets:
            if wallet.name == w.to_dict()['name']:
                return {'message': f'Wallet {wallet.name} exists for user {wallet.owner_id}'}, 409
        db.session.add(wallet)
        db.session.commit()
        wallet_uid = db.session.query(Wallet).filter_by(owner_id=wallet.owner_id).filter_by(name=wallet.name).filter_by(
            funds=wallet.funds).first().uid
        created_wallet = self.wallet_schema.dump(wallet)
        created_wallet['uid'] = wallet_uid
        return redirect(url_for('walletlistapiget'))
        # return created_wallet, 201


class WalletListApiEdit(Resource):
    wallet_schema = WalletSchema()

    @login_required
    def put(self, uid):
        wallet = db.session.query(Wallet).filter_by(uid=uid).first()
        if not wallet:
            return {'message': 'Wallet not found'}, 404
        try:
            if not current_user.is_admin and wallet.owner_id != current_user.uid:
                return {'message': 'Access denied'}, 409
            wallet_money = wallet.funds
            wallet = self.wallet_schema.load(request.json, instance=wallet, session=db.session)
            if not db.session.query(User).filter_by(uid=wallet.owner_id).first():
                return {'message': 'Wrong data, User(owner_id) not found'}, 400
            elif not current_user.is_admin and (wallet.owner_id != current_user.uid or wallet.funds != wallet_money):
                return {'message': 'Access denied'}, 409
        except ValidationError as e:
            return {'message': str(e)}, 400
        db.session.add(wallet)
        db.session.commit()
        return self.wallet_schema.dump(wallet), 200

    @login_required
    def patch(self, uid):
        wallet = db.session.query(Wallet).filter_by(uid=uid).first()
        if not wallet:
            return {'message': 'Wallet not found'}, 404
        try:
            wallet_money = wallet.funds
            wallet = self.wallet_schema.load(request.json, instance=wallet, session=db.session, partial=True)
            if not db.session.query(User).filter_by(uid=wallet.owner_id).first():
                return {'message': 'Wrong data, User(owner_id) not found'}, 400
            elif not current_user.is_admin and (wallet.owner_id != current_user.uid or wallet.funds != wallet_money):
                return {'message': 'Access denied'}, 409
        except ValidationError as e:
            return {'message': str(e)}, 400

        db.session.add(wallet)
        db.session.commit()
        return self.wallet_schema.dump(wallet), 200


class WalletListApiDelete(Resource):
    wallet_schema = WalletSchema()

    @login_required
    def post(self, uid):
        wallet = db.session.query(Wallet).filter_by(uid=uid).first()
        if not wallet:
            return {'message': 'Wallet not found'}, 404
        # wallet_deleted_owner = wallet.owner_id
        # user_wallets_num = len(db.session.query(Wallet).filter_by(owner_id=wallet_deleted_owner).all())
        # if user_wallets_num <= 1 and wallet.funds > 0:
        #     return {'message': 'Action restricted, cash out money'}, 409

        if not current_user.is_admin and wallet.owner_id != current_user.uid:
            return {'message': 'Access denied'}, 409

        # money_left = wallet.funds
        db.session.delete(wallet)
        db.session.commit()

        # if user_wallets_num <= 1 and wallet.funds > 0:
        #     moved_wallet = db.session.query(Wallet).filter_by(owner_id=wallet_deleted_owner).first()
        #     moved_wallet.funds += money_left
        #     db.session.add(moved_wallet)
        #     db.session.commit()
        return redirect(url_for('walletlistapiget'))
