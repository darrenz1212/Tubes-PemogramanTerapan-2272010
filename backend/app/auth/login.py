from flask import Blueprint, request, jsonify, session
from app.Model import User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dbConfig import DATABASE_URL
import hashlib

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

loginBp = Blueprint('login', __name__)

@loginBp.route('/login', methods=['POST','OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return '', 200
    data = request.get_json()
    data = request.get_json()
    session_db = SessionLocal()
    username = data.get('username')
    password = data.get('password')
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    user = session_db.query(User).filter(User.username == username, User.password == hashed_password).first()

    if user:
        session['user_id'] = user.user_id
        session['username'] = user.username
        session['role'] = user.role
        session_db.close()
        return jsonify({
            'message': 'Login successful',
            'user_id': user.user_id,   
            'username': user.username,
            'role' : user.role
            })
    else:
        session_db.close()
        return jsonify({'message': 'Invalid username or password'}), 401

@loginBp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'})
