from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
from models.user import UserModel



_parser = reqparse.RequestParser()
_parser.add_argument('username',
                    type=str,
                    required=True,
                    help="This field cannot be left blank!"
                    )
_parser.add_argument('password',
                    type=str,
                    required=True,
                    help="This field cannot be left blank!"
                    )

class UserRegister(Resource):


    def post(self):
        data = _parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {'message': 'A user with that username already exists'}, 400

        # user = UserModel(data['username'], data['password'])
        user = UserModel(**data)
        user.save_to_db()

        return {'message': 'User created successfully.'}, 201

class User(Resource):

    @classmethod
    def get(cls,user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json()

    @classmethod
    def delete(cls,user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        user.delete_from_db()
        return {'message': 'User deleted.'}, 200

class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = _parser.parse_args()
        user = UserModel.find_by_username((data['username']))
        if user and user.password == data['password']:
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        return {'message': 'Invalid credentials'}, 401
