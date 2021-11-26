import os
from flask import Flask
from flask_restful import Api
# from flask_jwt import JWT
from flask_jwt_extended import JWTManager
# from security import authenticate, identity
from resources.user import UserRegister, User, UserLogin
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from db import db


app = Flask(__name__)

# app.config['SQLACHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL2', 'sqlite:///data.db')
app.config['SQLACHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = False
# show error details
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = "Edward"
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

# app.config['JWT_AUTH_URL_RULE'] = '/others'
# config JWT to expire within half an hour
# app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
# config JWT auth key name to be 'email' instead of default 'username'
# app.config['JWT_AUTH_USERNAME_KEY'] = 'email'

# jwt = JWT(app, authenticate, identity)
jwt = JWTManager(app)


@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1: # Instead of hard cording, replace to read from a config file or a database
        return {'is_admin': True}
    return {'is_admin': False}

# customize JWT auth response, include user_id in response body
# @jwt.auth_response_handler
# def customized_response_handler(access_token, identity):
#     return jsonify({
#         'access_token': access_token.decode('utf-8'),
#         'user_id': identity.id
#     })


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')

if __name__ == '__main__':

    db.init_app(app)
    app.run(port=1234, debug=True)

