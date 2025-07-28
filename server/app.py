#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import app, db, api
from models import *

class Signup(Resource):
    def post(self):
        request_json = request.get_json()
        username = request_json.get('username')
        password = request_json.get('password')

        user = User(username=username)
        user.password_hash = password

        try:
            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.id
            return UserSchema().dump(user), 201
        except IntegrityError:
            return {'error': '422 Unprocessable Entity'}, 422

api.add_resource(Signup, '/signup', endpoint='signup')

if __name__ == '__main__':
    app.run(port=5555, debug=True)