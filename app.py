import os
from flask import Flask, jsonify
from flask_restful import Api
# from flask_jwt import JWT
from flask_jwt_extended import JWTManager
# from security import authenticate, identity
from resources.user import UserRegister, User, UserLogin
from resources.store import Store, StoreList
from resources.item import Item, ItemList
from db import db
from blacklist import BLACKLIST


app = Flask(__name__)

# app.config['SQLACHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL2', 'sqlite:///data.db')
app.config['SQLACHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLACHEMY_TRACK_MODIFICATIONS'] = False
# show error details
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
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


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'The token has expired.',
        'error': 'token_expired'
    }), 401
    
@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'description': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401
    
# @jwt.unauthorized_loader

# @jwt.needs_fresh_token_loader

# @jwt.revoked_token_loader 
 

@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['identity'] in BLACKLIST

    
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

