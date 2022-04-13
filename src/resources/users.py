from flask import request, g, make_response, render_template, url_for
from flask_login import login_required, current_user
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect

from src import db
from src.database.models import User
from src.resources.auth import auth
from src.schemas.users import UserSchema

headers = {'Content-Type': 'text/html'}


class UserListApiGet(Resource):
    user_schema = UserSchema()

    @login_required
    def get(self, username=None):
        if not username and current_user.is_admin:
            users = db.session.query(User).all()
            return make_response(render_template('users.html', users=users), 200, headers)
        if (username != current_user.username and username is not None) and not current_user.is_admin:
            return {'message': 'Access denied'}, 409
        if current_user.is_admin:
            user = db.session.query(User).filter_by(username=username).first()
        else:
            user = db.session.query(User).filter_by(username=current_user.username).first()
        if not user:
            return {'message': 'User not found'}, 404
        return make_response(render_template('user.html', user=user), 200, headers)
        # return self.user_schema.dump(user), 200


class UserListApiPost(Resource):
    user_schema = UserSchema()

    @login_required
    def get(self):
        return make_response(render_template('addUser.html'), 200, headers)

    @login_required
    def post(self):
        if current_user.is_admin:
            try:
                user = User(
                    username=request.form['username'],
                    first_name=request.form['first_name'],
                    last_name=request.form['last_name'],
                    email=request.form['email'],
                    password=request.form['password']
                )
            except ValidationError as e:
                return {'message': str(e)}, 400
            try:
                db.session.add(user)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                return {'message': 'Such user exists'}, 409
            return redirect(url_for('userlistapiget'))
            # return self.user_schema.dump(user)
        else:
            return {'message': 'Access denied, use /register'}, 409


class UserListApiUpdate(Resource):
    user_schema = UserSchema()

    @login_required
    def get(self, username):
        if not current_user.is_admin and current_user.username != username:
            return {'message': 'Access denied'}, 409
        if not username:
            users = db.session.query(User).all()
            return make_response(render_template('users.html', users=users), 200, headers)
        user = db.session.query(User).filter_by(username=username).first()
        if not user:
            return {'message': 'User not found'}, 404
        return make_response(render_template('update.html', user=user), 200, headers)

    @login_required
    def post(self, username):
        if not current_user.is_admin and current_user.username != username:
            return {'message': 'Access denied'}, 409
        user = db.session.query(User).filter_by(username=username).first()
        old_password = user.password
        if not user:
            return {'message': 'User not found'}, 404
        try:
            user.username = request.form['username']
            user.first_name = request.form['first_name']
            user.last_name = request.form['last_name']
            user.email = request.form['email']

        except ValidationError as e:
            return {'message': str(e)}, 400
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {'message': 'Such user exists'}, 409
        return redirect(url_for('userlistapiget'))


class UserListApiDelete(Resource):
    user_schema = UserSchema()

    @login_required
    def post(self, username):
        if not current_user.is_admin and current_user.username != username:
            return {'message': 'Access denied'}, 409
        user = db.session.query(User).filter_by(username=username).first()
        if not user:
            return {'message': 'User not found'}, 404
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('userlistapiget'))
