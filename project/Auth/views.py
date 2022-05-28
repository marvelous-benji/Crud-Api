'''
This module contains all the endpoints
neccessary for user authentication
'''


from flask import request, jsonify
from marshmallow import ValidationError
from flask_jwt_extended import create_access_token

from project import db, jwt
from . import auth
from ..models import User, UserSchema


@jwt.user_identity_loader
def user_identity_lookup(user):
    '''
    Automatically fetch authenticated
    user id from the database
    '''

    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_payload):
    '''
    Automatically load authenticated user object
    from database, making current_user available
    for route wrapped with the @jwt_required() decorator
    '''

    identity = jwt_payload["sub"]
    return User.objects(id=identity).first()


@auth.route("/register", methods=["POST"])
def signup():
    '''
    User registration route
    '''

    data = request.get_json()
    try:
        '''
        Taking the EAFP(Easier to Ask Forgiveness than Permission)
        than the LBYL(Look Before You Leap) approach
        '''

        serializer = UserSchema().load(data)
        print(serializer)
    except ValidationError as err:
        return (
            jsonify(
                {
                    "status": "failed",
                    "msg": "Your inputs are invalid",
                    "error": err.messages,
                }
            ),
            400,
        )
    if User.objects(email=serializer["email"]).first():
        return jsonify({"status": "failed", "msg": "You cannot use this email"}), 400
    user = User(email=serializer["email"], first_name=serializer["first_name"], last_name=serializer["last_name"])
    user.password = User.hash_password(serializer["password"])
    print("I GOT HERE SUCCESSFULLY", user.password)
    user.save()
    return jsonify({"status": "success", "msg": "Signup was successful"}), 201




@auth.route("/login", methods=["POST"])
def signin():
    '''
    User signin route
    '''
    
    data = request.get_json()

    try:
        '''
        Taking the EAFP(Easier to Ask Forgiveness than Permission)
        than the LBYL(Look Before You Leap) approach
        '''

        serializer = UserSchema(exclude=("first_name","last_name",)).load(data)
    except ValidationError as err:
        return (
            jsonify(
                {
                    "status": "failed",
                    "msg": "Your inputs are invalid",
                    "error": err.messages,
                }
            ),
            400,
        )
    user = User.objects(email=serializer["email"]).first()
    if user is None:
        return jsonify({"status": "failed", "msg": "Account not found"}), 404
    elif User.verify_password_hash(user.password, serializer["password"]):
        access_token = create_access_token(identity=user)
        return (
            jsonify(
                {
                    "status": "success",
                    "msg": "Login was successful",
                    "token": access_token,
                }
            ),
            200,
        )
    else:
        return jsonify({"status": "failed", "msg": "Incorrect login credentials"}), 401