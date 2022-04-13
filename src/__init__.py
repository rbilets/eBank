from flask import Flask, render_template, request
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

import config

app = Flask(__name__)
app.config.from_object(config.Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     return render_template('index.html')
#
#
# @app.route('/greeting', methods=['POST'])
# def greeting():
#     name = request.form.get('name')
#     if not name:
#         return 'Please enter a value', 400
#     return render_template('greeting.html', name=name)


from src import routes
from src.database import models
