from flask import Blueprint, request, jsonify
from app.Model import User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dbConfig import DATABASE_URL
import hashlib

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

userBp = Blueprint('user', __name__)

@userBp.route('/', methods=['GET'])
def getUser():
    session = SessionLocal()
    user_list = session.query(User).all()
    result = [
        {
            'user_id': u.user_id,
            'username': u.username,
            'password': u.password,
            'role': u.role,
            'program_studi_id': u.program_studi_id,
            'fakultas_id': u.fakultas_id
        }
        for u in user_list
    ]
    session.close()
    return jsonify({'user': result})

@userBp.route('/<userId>', methods=['GET'])
def getUserById(userId):
    session = SessionLocal()
    user = session.query(User).filter(User.user_id == userId).first()

    if user:
        result = {
            'user_id': user.user_id,
            'username': user.username, 
            'role': user.role,
            'program_studi_id': user.program_studi_id,
            'fakultas_id': user.fakultas_id
        }
    else:
        result = None
    
    session.close()
    return jsonify({'user': result})

@userBp.route('/', methods=['POST'])
def addUser():
    data = request.get_json()
    session = SessionLocal()
    password = data.get('password')
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    new_user = User(
        user_id = data.get('user_id'),
        username = data.get('username'),
        password = hashed_password,
        role = data.get('role'),
        program_studi_id = data.get('program_studi_id'),
        fakultas_id = data.get('fakultas_id')       
    )

    session.add(new_user)
    session.commit()
    session.close()
    return jsonify({'message': 'User added successfully'})

@userBp.route('/<userId>', methods=['PUT'])
def updateUser(userId):
    data = request.get_json()
    session = SessionLocal()

    user = session.query(User).filter(User.user_id == userId).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    user.username = data.get('username', user.username)
    user.password = hashlib.sha256(data.get('password', user.password).encode()).hexdigest()
    user.role = data.get('role', user.role)
    user.program_studi_id = data.get('program_studi_id', user.program_studi_id)
    user.fakultas_id = data.get('fakultas_id', user.fakultas_id)

    session.commit()
    session.close()
    return jsonify({'message': 'User updated successfully'})

@userBp.route('/<userId>', methods=['DELETE'])
def deleteUser(userId):
    session = SessionLocal()

    user = session.query(User).filter(User.user_id == userId).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    session.delete(user)
    session.commit()
    session.close()
    return jsonify({'message': 'User deleted successfully'})
