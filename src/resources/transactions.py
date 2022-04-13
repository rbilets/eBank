from flask import request, g, make_response, render_template, url_for
from flask_login import login_required, current_user
from flask_restful import Resource
from marshmallow import ValidationError
from werkzeug.utils import redirect

from src import db
from src.database.models import Transaction, Wallet
from src.resources.auth import auth
from src.schemas.transactions import TransactionSchema
from sqlalchemy import or_

headers = {'Content-Type': 'text/html'}


class TransactionListApiGet(Resource):
    transaction_schema = TransactionSchema()

    @staticmethod
    def get_transactions(user_uid):
        wallets = db.session.query(Wallet).filter_by(owner_id=user_uid).all()
        if not wallets:
            return {"message": "Wallets not found for the user"}, 404
        user_wallets = [w.uid for w in wallets]
        user_transactions = db.session.query(Transaction).filter(
            or_(Transaction.to_wallet_id.in_(user_wallets), Transaction.from_wallet_id.in_(user_wallets))).all()
        return [t.to_dict() for t in user_transactions]

    @login_required
    def get(self, uid_username=None):
        print(uid_username)
        if current_user.is_admin:
            if not uid_username:
                transactions = db.session.query(Transaction).all()
                return make_response(
                    render_template('transactions.html', transactions=[t.to_dict() for t in transactions]), 401,
                    headers)
                # return [t.to_dict() for t in transactions], 200
            elif str(uid_username).isnumeric():
                print("herree")
                transaction = db.session.query(Transaction).filter_by(uid=uid_username).first()
                if not transaction:
                    return {'message': 'Transaction not found'}, 404
                return make_response(
                    render_template('transactions.html', transactions=[transaction]), 401,
                    headers)
                # return transaction.to_dict(), 200
            else:
                return make_response(
                    render_template('transactions.html', transactions=self.get_transactions(uid_username)), 401,
                    headers)
                # return self.get_transactions(uid_username)

        else:
            print("big else")
            if not uid_username:
                transaction = db.session.query(Transaction).filter_by(uid=uid_username).first()
                if not transaction:
                    return {'message': 'Transaction not found'}, 404
                return make_response(
                    render_template('transactions.html', transactions=self.get_transactions(current_user.uid)), 401,
                    headers)
            elif str(uid_username).isnumeric():
                transaction = db.session.query(Transaction).filter_by(uid=uid_username).first()
                if not transaction:
                    return {'message': 'Transaction not found'}, 404
                wallets = db.session.query(Wallet).filter_by(owner_id=current_user.uid).all()
                user_wallets = [w.uid for w in wallets]
                if transaction.from_wallet_id not in user_wallets and transaction.to_wallet_id not in user_wallets:
                    return {'message': 'Access denied'}, 409
                return make_response(
                    render_template('transactions.html', transactions=[transaction]), 401,
                    headers)
                # return transaction.to_dict(), 200
            else:
                if current_user.uid != uid_username:
                    return {'message': 'Access denied'}, 409
                return self.get_transactions(uid_username)


class TransactionListApiPost(Resource):
    transaction_schema = TransactionSchema()

    def get(self):
        return make_response(
            render_template('transactionPost.html'), 400,
            headers)

    @login_required
    def post(self):
        try:
            transaction = Transaction(
                from_wallet_id=request.form['from_wallet_id'],
                to_wallet_id=request.form['to_wallet_id'],
                amount=float(request.form['amount']))
            # transaction = self.transaction_schema.load(request.json, session=db.session)
            if (transaction.amount <= 0):
                return {'message': 'Wrong operation'}, 400
            transaction.status = 0
            user_wallets = [w.uid for w in db.session.query(Wallet).filter_by(owner_id=current_user.uid)]
            if not current_user.is_admin and transaction.from_wallet_id not in user_wallets:
                return {'message': 'Access denied'}, 409
            elif not db.session.query(Wallet).filter_by(uid=transaction.from_wallet_id).first():
                db.session.add(transaction)
                db.session.commit()
                return {'message': 'Wrong data for from_wallet_id'}, 400
            elif not db.session.query(Wallet).filter_by(uid=transaction.to_wallet_id).first():
                db.session.add(transaction)
                db.session.commit()
                return {'message': 'Wrong data for to_wallet_id'}, 400
            elif db.session.query(Wallet).filter_by(uid=transaction.from_wallet_id).first().funds < transaction.amount:
                db.session.add(transaction)
                db.session.commit()
                return {'message': f'No enough funds for wallet {transaction.from_wallet_id}'}, 400
        except ValidationError as e:
            return {'message': str(e)}, 400

        wallet_from = db.session.query(Wallet).filter_by(uid=transaction.from_wallet_id).first()
        wallet_to = db.session.query(Wallet).filter_by(uid=transaction.to_wallet_id).first()
        wallet_from.funds -= transaction.amount
        wallet_to.funds += transaction.amount

        transaction.status = 1
        db.session.add(transaction)
        db.session.add(wallet_from)
        db.session.add(wallet_to)
        db.session.commit()
        return make_response(
            render_template('notifications.html', message="Successful operation "
                                                          "Your balance is: " + str(wallet_from.funds)), 401,
            headers)
        # return self.transaction_schema.dump(transaction), 201
