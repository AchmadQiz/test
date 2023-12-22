from app.main.model.user import Users
from app.main.view import response
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, jsonify
from app import db

def getUsers():
    try:
        users = Users.query.all()
        data = collectUserData(users)
        return response.ok(data, "Success Get User lists")
    except Exception as e:
        print(f"Error: {e}") 
        return response.badRequest([], 'Error : {e}')


def collectUserData(users):
    array = []
    for user in users:
        array.append(formatUserData(user))
    return array

def formatUserData(user):
    data = {
        'id': user.id,
        'name': user.name,
        'email': user.email
    }
    return data

def getUserById(id):
    try:
        users = Users.query.filter_by(id=id).first()
        if not users:
            return response.badRequest([], 'User Not Found')

        data = formatUserData(users)
        return response.ok(data, "Success get user by id")
    except Exception as e:
        print(f"Error: {e}")  
        return response.badRequest([], 'Error : {e}')

def createUser():
    try:
        name = request.json['name']
        email = request.json['email']
        password = request.json['password']

        hashed_password = generate_password_hash(password)

        new_user = Users(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'Successfully create user!'}), 200

    except Exception as e:
        print(e)
        return response.badRequest([], 'Error : {e}')


def updateUser(id):
    try:
        print("test")
        name = request.json['name']
        email = request.json['email']
        password = request.json['password']
        hashed_password = generate_password_hash(password)

        user = Users.query.filter_by(id=id).first()
        if not user:
            return response.badRequest([], 'User Not Found')

        user.email = email
        user.name = name
        user.password = hashed_password

        db.session.commit()
        return response.ok('', 'Successfully update data!')

    except Exception as e:
        print(f"Error: {e}")  # Log the error for debugging
        return response.badRequest([], 'Error : {e}')


def deleteUser(id):
    try:
        user = Users.query.filter_by(id=id).first()
        if not user:
            return response.badRequest([], 'User Not Found')

        db.session.delete(user)
        db.session.commit()

        return response.ok('', 'Successfully delete data!')
    except Exception as e:
        return response.badRequest([], 'Error : {e}')

